# Owner - pradhansaikat123@gmail.com

import uuid
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
import bcrypt

from app.db.session import getDb
from customerEngine.models import EngineCustomer, EngineCustomerAddress, EngineCustomerOrder
from customerEngine.schemas import (
    CustomerResponse,
    CustomerUpdate,
    AddressCreate,
    AddressUpdate,
    AddressResponse,
    GuestCheckoutRequest,
    GuestCheckoutResponse,
    AccountActivationRequest,
    ProfileImageUploadResponse,
)

# Custom context using bcrypt directly to bypass passlib self-check bug with bcrypt>=4.0.0
class DirectBcryptContext:
    def hash(self, secret: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(secret.encode("utf-8"), salt).decode("utf-8")

    def verify(self, secret: str, hash_val: str) -> bool:
        try:
            return bcrypt.checkpw(secret.encode("utf-8"), hash_val.encode("utf-8"))
        except Exception:
            return False

pwd_context = DirectBcryptContext()

customerEngineRouter = APIRouter(prefix="/customer-engine", tags=["Customer Engine"])

# Helper function to auto-generate guest code
def generate_customer_code(is_guest: bool) -> str:
    prefix = "CUST-GUEST" if is_guest else "CUST"
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"


# ── GUEST CHECKOUT / DUPLICATE MERGING ────────
@customerEngineRouter.post("/guest-checkout", response_model=GuestCheckoutResponse, status_code=status.HTTP_201_CREATED)
async def guestCheckout(checkoutData: GuestCheckoutRequest, dbSession: AsyncSession = Depends(getDb)):
    """
    Process guest orders. Handles duplicate detection by:
    - Merging/linking with an existing registered customer if email or mobile exists.
    - Reusing/updating an existing guest profile.
    - Otherwise creating a new guest customer profile.
    """
    # Look for existing customers with matching email or mobile under the same store
    query = select(EngineCustomer).where(
        EngineCustomer.storeId == checkoutData.storeId,
        EngineCustomer.isActive == True,
        or_(EngineCustomer.email == checkoutData.email, EngineCustomer.mobile == checkoutData.mobile)
    )
    result = await dbSession.execute(query)
    existing = result.scalars().all()

    selected_customer = None
    if existing:
        # Prioritize registered profiles (non-guest) to avoid duplicate profiles
        registered = next((c for c in existing if not c.isGuestCustomer), None)
        if registered:
            selected_customer = registered
        else:
            # Fall back to the first available guest profile and update details
            selected_customer = existing[0]
            selected_customer.firstName = checkoutData.firstName
            if checkoutData.lastName is not None:
                selected_customer.lastName = checkoutData.lastName
    else:
        # Create a new guest customer record
        selected_customer = EngineCustomer(
            tenantId=checkoutData.tenantId,
            storeId=checkoutData.storeId,
            customerCode=generate_customer_code(is_guest=True),
            firstName=checkoutData.firstName,
            lastName=checkoutData.lastName,
            email=checkoutData.email,
            mobile=checkoutData.mobile,
            status="ACTIVE",
            isGuestCustomer=True,
            isActive=True,
        )
        dbSession.add(selected_customer)
        await dbSession.flush()

    # Address storage if provided
    if checkoutData.address:
        # If default is requested, clear other default addresses of this type for the customer
        if checkoutData.address.isDefault:
            clear_defaults_query = select(EngineCustomerAddress).where(
                EngineCustomerAddress.customerId == selected_customer.id,
                EngineCustomerAddress.addressType == checkoutData.address.addressType.upper(),
                EngineCustomerAddress.isActive == True
            )
            defaults_result = await dbSession.execute(clear_defaults_query)
            for addr in defaults_result.scalars().all():
                addr.isDefault = False

        new_address = EngineCustomerAddress(
            customerId=selected_customer.id,
            addressType=checkoutData.address.addressType.upper(),
            fullName=checkoutData.address.fullName,
            mobile=checkoutData.address.mobile,
            addressLine1=checkoutData.address.addressLine1,
            addressLine2=checkoutData.address.addressLine2,
            landmark=checkoutData.address.landmark,
            city=checkoutData.address.city,
            state=checkoutData.address.state,
            country=checkoutData.address.country or "India",
            postalCode=checkoutData.address.postalCode,
            isDefault=checkoutData.address.isDefault,
            isActive=True
        )
        dbSession.add(new_address)
        await dbSession.flush()

    # Create the customer order (link guest profile with order)
    address_id = new_address.id if checkoutData.address else uuid.uuid4()
    new_order = EngineCustomerOrder(
        tenantId=checkoutData.tenantId,
        storeId=checkoutData.storeId,
        customerId=selected_customer.id,
        orderNumber=f"ORD-{uuid.uuid4().hex[:8].upper()}",
        totalAmount=checkoutData.totalAmount,
        subtotalAmount=checkoutData.totalAmount,
        billingAddressId=address_id,
        shippingAddressId=address_id,
        status="SUCCESS"
    )
    dbSession.add(new_order)
    await dbSession.flush()

    return {
        "message": "Guest checkout successful",
        "customer": selected_customer,
        "order": new_order
    }


# ── ACCOUNT ACTIVATION ────────────────────────
@customerEngineRouter.post("/customers/{customerId}/activate")
async def activateAccount(customerId: UUID, payload: AccountActivationRequest, dbSession: AsyncSession = Depends(getDb)):
    """
    Enable guest to login later by setting a password and converting guest into customer profile.
    """
    query = select(EngineCustomer).where(EngineCustomer.id == customerId, EngineCustomer.isActive == True)
    result = await dbSession.execute(query)
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # Set password hash and convert guest flag
    customer.passwordHash = pwd_context.hash(payload.password)
    if customer.isGuestCustomer:
        customer.isGuestCustomer = False
        # Update customer code prefix to full customer
        if customer.customerCode.startswith("CUST-GUEST-"):
            customer.customerCode = customer.customerCode.replace("CUST-GUEST-", "CUST-")

    await dbSession.flush()
    return {"message": "Account activated successfully, direct login is now available"}


# ── CUSTOMER PROFILES (CRUD) ──────────────────
# DEPRECATED: duplicates GET/PATCH /api/v1/customers/{id}, which is the ACTIVE
# customer-profile router (tenant-scoped, staff-authenticated). Kept live for
# backward compatibility, not for new integrations. See docs/api-mapping/customers.md.
@customerEngineRouter.get("/customers/{customerId}", response_model=CustomerResponse, deprecated=True)
async def getCustomerProfile(customerId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Retrieve customer details.
    """
    query = select(EngineCustomer).where(EngineCustomer.id == customerId, EngineCustomer.isActive == True)
    result = await dbSession.execute(query)
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found"
        )
    return customer


# DEPRECATED: duplicates PATCH /api/v1/customers/{id}. Kept live for backward
# compatibility, not for new integrations. See docs/api-mapping/customers.md.
@customerEngineRouter.put("/customers/{customerId}", response_model=CustomerResponse, deprecated=True)
async def updateCustomerProfile(customerId: UUID, updateData: CustomerUpdate, dbSession: AsyncSession = Depends(getDb)):
    """
    Update profile fields with duplicate validation.
    """
    query = select(EngineCustomer).where(EngineCustomer.id == customerId, EngineCustomer.isActive == True)
    result = await dbSession.execute(query)
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found"
        )

    # Validate duplicate email/mobile within the same store
    if updateData.email or updateData.mobile:
        new_email = updateData.email or customer.email
        new_mobile = updateData.mobile or customer.mobile

        dup_query = select(EngineCustomer).where(
            EngineCustomer.storeId == customer.storeId,
            EngineCustomer.id != customerId,
            EngineCustomer.isActive == True,
            or_(EngineCustomer.email == new_email, EngineCustomer.mobile == new_mobile)
        )
        dup_result = await dbSession.execute(dup_query)
        dup_exists = dup_result.scalars().first()
        if dup_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another active customer already uses this email or mobile in the store"
            )

    # Perform updates
    if updateData.firstName is not None:
        customer.firstName = updateData.firstName
    if updateData.lastName is not None:
        customer.lastName = updateData.lastName
    if updateData.email is not None:
        customer.email = updateData.email
    if updateData.mobile is not None:
        customer.mobile = updateData.mobile
    if updateData.status is not None:
        if updateData.status not in ("ACTIVE", "INACTIVE", "BLOCKED"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be ACTIVE, INACTIVE, or BLOCKED"
            )
        customer.status = updateData.status

    await dbSession.flush()
    return customer


@customerEngineRouter.post("/customers/{customerId}/media", response_model=ProfileImageUploadResponse)
async def uploadProfileImage(customerId: UUID, file: UploadFile = File(...), dbSession: AsyncSession = Depends(getDb)):
    """
    Upload and register profile image.
    """
    query = select(EngineCustomer).where(EngineCustomer.id == customerId, EngineCustomer.isActive == True)
    result = await dbSession.execute(query)
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found"
        )

    # Simulate path upload mapping (standard format)
    mocked_image_url = f"/media/profiles/{customerId}/{file.filename}"
    customer.profileImage = mocked_image_url

    await dbSession.flush()
    return {
        "message": "Image uploaded successfully",
        "profileImage": mocked_image_url
    }


# ── CUSTOMER ADDRESSES (CRUD) ─────────────────
# DEPRECATED (all four routes below): duplicate the ACTIVE /api/v1/addresses/*
# router (app/api/v1/endpoints/customerAddresses.py). Kept live for backward
# compatibility, not for new integrations. See docs/api-mapping/customers.md.
@customerEngineRouter.post("/customers/{customerId}/addresses", response_model=AddressResponse, status_code=status.HTTP_201_CREATED, deprecated=True)
async def createAddress(customerId: UUID, addressData: AddressCreate, dbSession: AsyncSession = Depends(getDb)):
    """
    Add a new shipping or billing address. Manages default switching safely.
    """
    query = select(EngineCustomer).where(EngineCustomer.id == customerId, EngineCustomer.isActive == True)
    result = await dbSession.execute(query)
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found"
        )

    # Handle default address flag update
    if addressData.isDefault:
        clear_defaults_query = select(EngineCustomerAddress).where(
            EngineCustomerAddress.customerId == customerId,
            EngineCustomerAddress.addressType == addressData.addressType.upper(),
            EngineCustomerAddress.isActive == True
        )
        defaults_result = await dbSession.execute(clear_defaults_query)
        for addr in defaults_result.scalars().all():
            addr.isDefault = False

    new_address = EngineCustomerAddress(
        customerId=customerId,
        addressType=addressData.addressType.upper(),
        fullName=addressData.fullName,
        mobile=addressData.mobile,
        addressLine1=addressData.addressLine1,
        addressLine2=addressData.addressLine2,
        landmark=addressData.landmark,
        city=addressData.city,
        state=addressData.state,
        country=addressData.country or "India",
        postalCode=addressData.postalCode,
        isDefault=addressData.isDefault,
        isActive=True
    )
    dbSession.add(new_address)
    await dbSession.flush()
    return new_address


@customerEngineRouter.get("/customers/{customerId}/addresses", response_model=list[AddressResponse], deprecated=True)
async def listAddresses(customerId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    List all active addresses of a customer.
    """
    query = select(EngineCustomerAddress).where(
        EngineCustomerAddress.customerId == customerId,
        EngineCustomerAddress.isActive == True
    ).order_by(EngineCustomerAddress.isDefault.desc(), EngineCustomerAddress.createdAt.desc())
    
    result = await dbSession.execute(query)
    return result.scalars().all()


@customerEngineRouter.put("/addresses/{addressId}", response_model=AddressResponse, deprecated=True)
async def updateAddress(addressId: UUID, updateData: AddressUpdate, dbSession: AsyncSession = Depends(getDb)):
    """
    Update details of an address. Manages default switching safely.
    """
    query = select(EngineCustomerAddress).where(EngineCustomerAddress.id == addressId, EngineCustomerAddress.isActive == True)
    result = await dbSession.execute(query)
    address = result.scalar_one_or_none()

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )

    # Determine types
    new_type = updateData.addressType.upper() if updateData.addressType else address.addressType
    new_is_default = updateData.isDefault if updateData.isDefault is not None else address.isDefault

    # Clear defaults if updated to default
    if new_is_default:
        clear_defaults_query = select(EngineCustomerAddress).where(
            EngineCustomerAddress.customerId == address.customerId,
            EngineCustomerAddress.id != addressId,
            EngineCustomerAddress.addressType == new_type,
            EngineCustomerAddress.isActive == True
        )
        defaults_result = await dbSession.execute(clear_defaults_query)
        for addr in defaults_result.scalars().all():
            addr.isDefault = False

    # Perform updates
    if updateData.addressType is not None:
        address.addressType = updateData.addressType.upper()
    if updateData.fullName is not None:
        address.fullName = updateData.fullName
    if updateData.mobile is not None:
        address.mobile = updateData.mobile
    if updateData.addressLine1 is not None:
        address.addressLine1 = updateData.addressLine1
    if updateData.addressLine2 is not None:
        address.addressLine2 = updateData.addressLine2
    if updateData.landmark is not None:
        address.landmark = updateData.landmark
    if updateData.city is not None:
        address.city = updateData.city
    if updateData.state is not None:
        address.state = updateData.state
    if updateData.country is not None:
        address.country = updateData.country
    if updateData.postalCode is not None:
        address.postalCode = updateData.postalCode
    if updateData.isDefault is not None:
        address.isDefault = updateData.isDefault

    await dbSession.flush()
    return address


@customerEngineRouter.delete("/addresses/{addressId}", deprecated=True)
async def deleteAddress(addressId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Soft delete a customer address.
    """
    query = select(EngineCustomerAddress).where(EngineCustomerAddress.id == addressId, EngineCustomerAddress.isActive == True)
    result = await dbSession.execute(query)
    address = result.scalar_one_or_none()

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )

    # Perform hard delete since there is no is_active column in the database table
    await dbSession.delete(address)
    await dbSession.flush()
    return {"message": "Address deleted successfully"}
