# Owner - pradhansaikat123@gmail.com

import io
import pytest
import pytest_asyncio
import uuid
from decimal import Decimal
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from fastapi import HTTPException, UploadFile

from app.db.base import Base
from customerEngine.models import EngineCustomer, EngineCustomerAddress, EngineCustomerOrder
from customerEngine.schemas import (
    GuestCheckoutRequest,
    AccountActivationRequest,
    CustomerUpdate,
    AddressCreate,
    AddressUpdate,
)
from customerEngine.router import (
    guestCheckout,
    activateAccount,
    getCustomerProfile,
    updateCustomerProfile,
    uploadProfileImage,
    createAddress,
    listAddresses,
    updateAddress,
    deleteAddress,
)

# Compile custom Postgres UUID as VARCHAR(36) in SQLite
@compiles(PostgresUUID, "sqlite")
def compileUuidSqlite(type_, compiler, **kw):
    """
    Compile hook to map PostgreSQL UUID types to standard VARCHAR(36) in SQLite.
    """
    return "VARCHAR(36)"


# Fixture to configure the test database session factory
@pytest_asyncio.fixture(scope="function")
async def testDb():
    """
    Sets up an in-memory SQLite database and registers all required customerEngine tables.
    """
    testEngine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with testEngine.begin() as dbConn:
        tablesToCreate = [
            EngineCustomer.__table__,
            EngineCustomerAddress.__table__,
            EngineCustomerOrder.__table__,
        ]
        await dbConn.run_sync(lambda syncConn: Base.metadata.create_all(syncConn, tables=tablesToCreate))
        
    sessionFactory = async_sessionmaker(
        bind=testEngine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    yield sessionFactory
    
    async with testEngine.begin() as dbConn:
        tablesToDrop = [
            EngineCustomer.__table__,
            EngineCustomerAddress.__table__,
            EngineCustomerOrder.__table__,
        ]
        await dbConn.run_sync(lambda syncConn: Base.metadata.drop_all(syncConn, tables=tablesToDrop))


# ── TEST GUEST CHECKOUT & DUPLICATE MERGING ──
@pytest.mark.asyncio
async def testGuestCheckoutAndDuplicateHandling(testDb):
    """
    Verify guest checkout, order mapping, and duplicate detection merging logic.
    """
    async with testDb() as dbSession:
        tenantId = uuid.uuid4()
        storeId = uuid.uuid4()

        # 1. Create a guest checkout record (first-time guest)
        req1 = GuestCheckoutRequest(
            tenantId=tenantId,
            storeId=storeId,
            firstName="John",
            lastName="Doe",
            email="john.doe@example.com",
            mobile="1234567890",
            totalAmount=Decimal("150.00"),
            address=AddressCreate(
                addressType="SHIPPING",
                fullName="John Doe",
                mobile="1234567890",
                addressLine1="123 Main St",
                city="Bengaluru",
                state="Karnataka",
                postalCode="560001",
                isDefault=True
            )
        )
        resp1 = await guestCheckout(checkoutData=req1, dbSession=dbSession)
        
        assert resp1["message"] == "Guest checkout successful"
        cust1 = resp1["customer"]
        order1 = resp1["order"]
        
        assert cust1.id is not None
        assert cust1.isGuestCustomer is True
        assert cust1.email == "john.doe@example.com"
        assert order1.customerId == cust1.id
        assert order1.totalAmount == Decimal("150.00")

        # Verify address got stored
        addresses1 = await listAddresses(customerId=cust1.id, dbSession=dbSession)
        assert len(addresses1) == 1
        assert addresses1[0].addressLine1 == "123 Main St"
        assert addresses1[0].isDefault is True

        # 2. Perform checkout again using the same guest email/mobile -> duplicate detection should reuse profile
        req2 = GuestCheckoutRequest(
            tenantId=tenantId,
            storeId=storeId,
            firstName="Johnny",
            lastName="Doe",
            email="john.doe@example.com",
            mobile="1234567890",
            totalAmount=Decimal("80.50")
        )
        resp2 = await guestCheckout(checkoutData=req2, dbSession=dbSession)
        cust2 = resp2["customer"]
        order2 = resp2["order"]
        
        assert cust2.id == cust1.id  # Same customer record reused!
        assert cust2.firstName == "Johnny"  # Details updated
        assert order2.customerId == cust1.id
        assert order2.id != order1.id

        # 3. Create a registered/active customer
        registered_cust = EngineCustomer(
            tenantId=tenantId,
            storeId=storeId,
            customerCode="CUST-1234",
            firstName="Alice",
            email="alice@example.com",
            mobile="9876543210",
            isGuestCustomer=False,
            isActive=True
        )
        dbSession.add(registered_cust)
        await dbSession.flush()

        # Perform guest checkout using registered customer's email
        req3 = GuestCheckoutRequest(
            tenantId=tenantId,
            storeId=storeId,
            firstName="Alice Guest",
            email="alice@example.com",
            mobile="9876543210",
            totalAmount=Decimal("200.00")
        )
        resp3 = await guestCheckout(checkoutData=req3, dbSession=dbSession)
        cust3 = resp3["customer"]
        order3 = resp3["order"]

        assert cust3.id == registered_cust.id  # Merged to existing registered customer!
        assert cust3.isGuestCustomer is False  # Profile remains a full customer profile
        assert order3.customerId == registered_cust.id


# ── TEST ACCOUNT ACTIVATION ──────────────────
@pytest.mark.asyncio
async def testAccountActivation(testDb):
    """
    Verify conversion of guest data into full customer profile and password setup.
    """
    async with testDb() as dbSession:
        tenantId = uuid.uuid4()
        storeId = uuid.uuid4()

        # Create guest customer
        guest = EngineCustomer(
            tenantId=tenantId,
            storeId=storeId,
            customerCode="CUST-GUEST-TEST",
            firstName="Guesty",
            email="guesty@example.com",
            mobile="1111122222",
            isGuestCustomer=True,
            isActive=True
        )
        dbSession.add(guest)
        await dbSession.flush()

        # Activate the account
        activation_req = AccountActivationRequest(password="secret123")
        resp = await activateAccount(customerId=guest.id, payload=activation_req, dbSession=dbSession)
        assert resp["message"] == "Account activated successfully, direct login is now available"

        # Fetch updated customer
        updated = await getCustomerProfile(customerId=guest.id, dbSession=dbSession)
        assert updated.isGuestCustomer is False
        assert updated.passwordHash is not None
        assert updated.passwordHash != "secret123"  # Hashed
        assert updated.customerCode.startswith("CUST-")
        assert not updated.customerCode.startswith("CUST-GUEST-")

        # Test activation on non-existent customer raises 404
        with pytest.raises(HTTPException) as excInfo:
            await activateAccount(customerId=uuid.uuid4(), payload=activation_req, dbSession=dbSession)
        assert excInfo.value.status_code == 404


# ── TEST CUSTOMER PROFILES (CRUD & MEDIA) ────
@pytest.mark.asyncio
async def testCustomerProfileCrudAndMedia(testDb):
    """
    Verify view/update customer profiles, validations, and profile image upload.
    """
    async with testDb() as dbSession:
        tenantId = uuid.uuid4()
        storeId = uuid.uuid4()

        # Create base customer
        cust = EngineCustomer(
            tenantId=tenantId,
            storeId=storeId,
            customerCode="CUST-A",
            firstName="Robert",
            lastName="P",
            email="robert@example.com",
            mobile="9090909090",
            isActive=True
        )
        dbSession.add(cust)
        
        # Create second customer for duplicate check
        cust_b = EngineCustomer(
            tenantId=tenantId,
            storeId=storeId,
            customerCode="CUST-B",
            firstName="Sarah",
            email="sarah@example.com",
            mobile="8080808080",
            isActive=True
        )
        dbSession.add(cust_b)
        await dbSession.flush()

        # 1. Fetch Profile
        fetched = await getCustomerProfile(customerId=cust.id, dbSession=dbSession)
        assert fetched.firstName == "Robert"

        # 2. Update Profile
        update_data = CustomerUpdate(firstName="Rob", lastName="Penn", email="rob.p@example.com")
        updated = await updateCustomerProfile(customerId=cust.id, updateData=update_data, dbSession=dbSession)
        assert updated.firstName == "Rob"
        assert updated.lastName == "Penn"
        assert updated.email == "rob.p@example.com"

        # 3. Test Profile Validation (Duplicate email rejection)
        invalid_update = CustomerUpdate(email="sarah@example.com")
        with pytest.raises(HTTPException) as excInfo:
            await updateCustomerProfile(customerId=cust.id, updateData=invalid_update, dbSession=dbSession)
        assert excInfo.value.status_code == 400
        assert "Another active customer already uses this email or mobile" in excInfo.value.detail

        # 4. Upload Profile Image
        mock_file = UploadFile(file=io.BytesIO(b"dummy_image_data"), filename="avatar.jpg")
        media_resp = await uploadProfileImage(customerId=cust.id, file=mock_file, dbSession=dbSession)
        assert media_resp["message"] == "Image uploaded successfully"
        assert media_resp["profileImage"].endswith("avatar.jpg")

        # Fetch profile to verify image saved
        profile = await getCustomerProfile(customerId=cust.id, dbSession=dbSession)
        assert profile.profileImage == media_resp["profileImage"]


# ── TEST CUSTOMER ADDRESSES (CRUD & DEFAULTS) ──
@pytest.mark.asyncio
async def testCustomerAddressesAndDefaultHandling(testDb):
    """
    Verify address CRUD APIs and default shipping/billing maintenance.
    """
    async with testDb() as dbSession:
        tenantId = uuid.uuid4()
        storeId = uuid.uuid4()

        # Create customer
        cust = EngineCustomer(
            tenantId=tenantId,
            storeId=storeId,
            customerCode="CUST-ADDR-TEST",
            firstName="Jack",
            email="jack@example.com",
            mobile="7070707070",
            isActive=True
        )
        dbSession.add(cust)
        await dbSession.flush()

        # 1. Create first address (SHIPPING, default=True)
        addr1_req = AddressCreate(
            addressType="SHIPPING",
            fullName="Jack Shipping 1",
            mobile="7070707070",
            addressLine1="First Shipping Line",
            city="Pune",
            state="Maharashtra",
            postalCode="411001",
            isDefault=True
        )
        addr1 = await createAddress(customerId=cust.id, addressData=addr1_req, dbSession=dbSession)
        assert addr1.id is not None
        assert addr1.isDefault is True

        # 2. Create second address (SHIPPING, default=True) -> Should clear defaults on first
        addr2_req = AddressCreate(
            addressType="SHIPPING",
            fullName="Jack Shipping 2",
            mobile="7070707070",
            addressLine1="Second Shipping Line",
            city="Pune",
            state="Maharashtra",
            postalCode="411002",
            isDefault=True
        )
        addr2 = await createAddress(customerId=cust.id, addressData=addr2_req, dbSession=dbSession)
        assert addr2.isDefault is True

        # Fetch addresses list and verify defaults
        addresses = await listAddresses(customerId=cust.id, dbSession=dbSession)
        assert len(addresses) == 2
        # Default should be sorted first
        assert addresses[0].id == addr2.id
        assert addresses[0].isDefault is True
        assert addresses[1].id == addr1.id
        assert addresses[1].isDefault is False

        # 3. Create BILLING address (isDefault=True) -> Should not affect SHIPPING defaults
        billing_req = AddressCreate(
            addressType="BILLING",
            fullName="Jack Billing",
            mobile="7070707070",
            addressLine1="Billing Address Line",
            city="Pune",
            state="Maharashtra",
            postalCode="411001",
            isDefault=True
        )
        billing = await createAddress(customerId=cust.id, addressData=billing_req, dbSession=dbSession)
        assert billing.isDefault is True

        # Re-verify shipping default remains intact
        addresses = await listAddresses(customerId=cust.id, dbSession=dbSession)
        shipping_default = next(a for a in addresses if a.addressType == "SHIPPING" and a.isDefault)
        assert shipping_default.id == addr2.id

        # 4. Update address to default (e.g. set shipping 1 back to default)
        update_req = AddressUpdate(isDefault=True)
        updated_addr1 = await updateAddress(addressId=addr1.id, updateData=update_req, dbSession=dbSession)
        assert updated_addr1.isDefault is True

        # Verify default switched back
        addresses = await listAddresses(customerId=cust.id, dbSession=dbSession)
        shipping_default_new = next(a for a in addresses if a.addressType == "SHIPPING" and a.isDefault)
        assert shipping_default_new.id == addr1.id
        
        # Verify old shipping default is now False
        old_default = next(a for a in addresses if a.id == addr2.id)
        assert old_default.isDefault is False

        # 5. Delete Address (soft delete)
        del_resp = await deleteAddress(addressId=addr2.id, dbSession=dbSession)
        assert del_resp["message"] == "Address deleted successfully"

        # Verify not returned in active list
        active_list = await listAddresses(customerId=cust.id, dbSession=dbSession)
        assert addr2.id not in [a.id for a in active_list]
        assert len(active_list) == 2
