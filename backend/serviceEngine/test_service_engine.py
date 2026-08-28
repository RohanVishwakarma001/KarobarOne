# Owner-pradhansaikat123@gmail.com


import asyncio
import pytest
import pytest_asyncio
import uuid
from decimal import Decimal
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from app.db.base import Base
from app.db.models.tenant import Tenant
from app.db.models.tenantPlanMapping import TenantPlanMapping
from app.db.modelsRegistry import TenantStatus, SubscriptionPlan
from fastapi import HTTPException
from serviceEngine.models import (
    ServiceCategory,
    Service,
    ServicePricing,
    BookingRule,
    ServiceAvailability,
)
from serviceEngine.schemas import (
    ServiceCategoryCreate,
    ServiceCategoryUpdate,
    ServiceCreate,
    ServiceUpdate,
    BookingRuleCreate,
    BookingValidationRequest,
    ServiceAvailabilityCreate,
    ServiceAvailabilityUpdate,
)
from serviceEngine.router import (
    createCategory,
    listCategories,
    getCategory,
    updateCategory,
    deleteCategory,
    createService,
    listServices,
    getService,
    updateService,
    deleteService,
    submitApproval,
    createBookingRule,
    getBookingRule,
    validateBooking,
    createAvailability,
    listAvailabilities,
    updateAvailability,
    deleteAvailability,
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
    Sets up an in-memory SQLite database and registers all required model tables.
    """
    testEngine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with testEngine.begin() as dbConn:
        tablesToCreate = [
            Tenant.__table__,
            TenantStatus.__table__,
            TenantPlanMapping.__table__,
            SubscriptionPlan.__table__,
            ServiceCategory.__table__,
            ServicePricing.__table__,
            Service.__table__,
            BookingRule.__table__,
            ServiceAvailability.__table__,
        ]
        await dbConn.run_sync(lambda syncConn: Base.metadata.create_all(syncConn, tables=tablesToCreate))
        
    sessionFactory = async_sessionmaker(
        bind=testEngine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    # Pre-populate status codes and a default subscription plan for testing
    async with sessionFactory() as dbSession:
        statusActive = TenantStatus(id=1, statusName="ACTIVE", statusDescription="Active tenant status")
        statusSuspended = TenantStatus(id=2, statusName="SUSPENDED", statusDescription="Suspended tenant status")
        dbSession.add_all([statusActive, statusSuspended])
        
        defaultPlan = SubscriptionPlan(
            id=uuid.uuid4(),
            planCode="PRO_PLAN",
            planName="Pro Plan",
            monthlyPrice=Decimal("999.00"),
            transactionCommissionPercent=Decimal("2.50"),
            isActive=True,
        )
        dbSession.add(defaultPlan)
        await dbSession.commit()
        
    yield sessionFactory
    
    async with testEngine.begin() as dbConn:
        tablesToDrop = [
            Tenant.__table__,
            TenantStatus.__table__,
            TenantPlanMapping.__table__,
            SubscriptionPlan.__table__,
            ServiceCategory.__table__,
            ServicePricing.__table__,
            Service.__table__,
            BookingRule.__table__,
            ServiceAvailability.__table__,
        ]
        await dbConn.run_sync(lambda syncConn: Base.metadata.drop_all(syncConn, tables=tablesToDrop))

# Test Category CRUD and duplicate validations
@pytest.mark.asyncio
async def testCategoryCrudAndValidation(testDb):
    """
    Verifies ServiceCategory CRUD endpoints and check for duplicate category constraints.
    """
    async with testDb() as dbSession:
        tenantId = uuid.uuid4()
        
        # Test category creation
        categoryCreate = ServiceCategoryCreate(
            tenantId=tenantId,
            categoryName="Home Cleaning",
            categorySlug="home-cleaning",
            categoryType="SERVICE"
        )
        categoryObj = await createCategory(categoryData=categoryCreate, dbSession=dbSession)
        assert categoryObj.id is not None
        assert categoryObj.categoryName == "Home Cleaning"
        assert categoryObj.isActive is True
        
        # Test duplicate validation
        duplicateCreate = ServiceCategoryCreate(
            tenantId=tenantId,
            categoryName="Home Cleaning",
            categorySlug="new-cleaning",
            categoryType="SERVICE"
        )
        with pytest.raises(HTTPException) as excInfo:
            await createCategory(categoryData=duplicateCreate, dbSession=dbSession)
        assert excInfo.value.status_code == 400
        assert "Category with this name or slug already exists" in excInfo.value.detail
        
        # Test listing categories
        categoryList = await listCategories(tenantId=tenantId, dbSession=dbSession)
        assert len(categoryList) == 1
        assert categoryList[0].id == categoryObj.id
        
        # Test retrieving category by ID
        fetchedCategory = await getCategory(categoryId=categoryObj.id, dbSession=dbSession)
        assert fetchedCategory.categoryName == "Home Cleaning"
        
        # Test updating category
        updateData = ServiceCategoryUpdate(categoryName="Deep Home Cleaning")
        updatedCategory = await updateCategory(categoryId=categoryObj.id, updateData=updateData, dbSession=dbSession)
        assert updatedCategory.categoryName == "Deep Home Cleaning"
        
        # Test soft delete
        deleteResponse = await deleteCategory(categoryId=categoryObj.id, dbSession=dbSession)
        assert deleteResponse["message"] == "Category deleted successfully"
        
        # Verify it cannot be retrieved as active
        with pytest.raises(HTTPException) as excInfoNotFound:
            await getCategory(categoryId=categoryObj.id, dbSession=dbSession)
        assert excInfoNotFound.value.status_code == 404

# Test Service CRUD and approval flow
@pytest.mark.asyncio
async def testServiceCrudAndApproval(testDb):
    """
    Verifies Service CRUD operations, soft deletes, and approval states.
    """
    async with testDb() as dbSession:
        tenantId = uuid.uuid4()
        
        # Create category first
        categoryCreate = ServiceCategoryCreate(
            tenantId=tenantId,
            categoryName="Salon Services",
            categorySlug="salon-services",
            categoryType="SERVICE"
        )
        categoryObj = await createCategory(categoryData=categoryCreate, dbSession=dbSession)
        
        # Create service with valid fields
        serviceCreate = ServiceCreate(
            tenantId=tenantId,
            categoryId=categoryObj.id,
            serviceName="Hair Styling",
            serviceSlug="hair-styling",
            serviceType="PHYSICAL",
            description="Premium hair styling for men and women",
            pricing=Decimal("499.00"),
            duration=45,
            media={"images": ["url1", "url2"]},
            metaTitle="Best Hair Styling in Town",
            metaDescription="Book professional hair styling.",
            metaSlug="best-hair-styling",
            approvalStatus="PENDING"
        )
        serviceObj = await createService(serviceData=serviceCreate, dbSession=dbSession)
        assert serviceObj.id is not None
        assert serviceObj.serviceName == "Hair Styling"
        assert serviceObj.serviceType == "PHYSICAL"
        
        # Create service with invalid service type (should fail)
        invalidCreate = ServiceCreate(
            tenantId=tenantId,
            categoryId=categoryObj.id,
            serviceName="Invalid Service",
            serviceSlug="invalid-service",
            serviceType="DIGITAL",  # Must be PHYSICAL or ONLINE
            pricing=Decimal("100.00"),
            duration=30
        )
        with pytest.raises(HTTPException) as excInfoType:
            await createService(serviceData=invalidCreate, dbSession=dbSession)
        assert excInfoType.value.status_code == 400
        
        # Retrieve list of services
        serviceList = await listServices(tenantId=tenantId, dbSession=dbSession)
        assert len(serviceList) == 1
        
        # Submit service for approval
        approvedService = await submitApproval(serviceId=serviceObj.id, dbSession=dbSession)
        assert approvedService.approvalStatus == "PENDING_APPROVAL"
        
        # Test soft delete
        await deleteService(serviceId=serviceObj.id, dbSession=dbSession)
        
        # Verify it cannot be retrieved
        with pytest.raises(HTTPException) as excInfoNotFound:
            await getService(serviceId=serviceObj.id, dbSession=dbSession)
        assert excInfoNotFound.value.status_code == 404

# Test Booking Rules and Tenant restrictions
@pytest.mark.asyncio
async def testBookingRulesAndRestrictions(testDb):
    """
    Verifies booking rules config, payments validation, and inactive/unpaid provider restrictions.
    """
    async with testDb() as dbSession:
        tenantId = uuid.uuid4()
        
        # 1. Seed tenant and plan mapping for successful scenario
        activeTenant = Tenant(
            id=tenantId,
            panNumber="ABCDE1234F",
            businessName="Saikat Salon",
            legalName="Saikat Salon Pvt Ltd",
            email="salon@saikat.com",
            mobile="+919876543210",
            ownerName="Saikat Pradhan",
            businessAddressLine1="Street 1",
            city="Kolkata",
            state="West Bengal",
            postalCode="700001",
            businessType="Service",
            statusId=1,  # ACTIVE
            isActive=True
        )
        dbSession.add(activeTenant)
        
        # Fetch seeded plan
        planQuery = select(SubscriptionPlan).where(SubscriptionPlan.planCode == "PRO_PLAN")
        planResult = await dbSession.execute(planQuery)
        planObj = planResult.scalar_one()
        
        planMapping = TenantPlanMapping(
            id=uuid.uuid4(),
            tenantId=tenantId,
            planId=planObj.id,
            planStartDate=datetime.now().date(),
            autoRenew=True,
            statusId=1  # ACTIVE
        )
        dbSession.add(planMapping)
        
        # Create category and service
        categoryObj = await createCategory(
            categoryData=ServiceCategoryCreate(
                tenantId=tenantId, categoryName="Beauty", categorySlug="beauty"
            ),
            dbSession=dbSession
        )
        serviceObj = await createService(
            serviceData=ServiceCreate(
                tenantId=tenantId,
                categoryId=categoryObj.id,
                serviceName="Facial",
                serviceSlug="facial",
                serviceType="PHYSICAL",
                pricing=Decimal("999.00"),
                duration=60
            ),
            dbSession=dbSession
        )
        await dbSession.commit()
        
        # 2. Configure Booking Rule
        ruleCreate = BookingRuleCreate(
            tenantId=tenantId,
            serviceId=serviceObj.id,
            bookingMode="BOOKING_AND_PAYMENT",
            requiresApproval=True
        )
        ruleObj = await createBookingRule(ruleData=ruleCreate, dbSession=dbSession)
        assert ruleObj.bookingMode == "BOOKING_AND_PAYMENT"
        
        # 3. Validate booking rule when unpaid (missing payment confirmation) - Should fail
        validationRequest = BookingValidationRequest(
            tenantId=tenantId,
            serviceId=serviceObj.id,
            isPaid=False,
            paymentReferenceId=None
        )
        with pytest.raises(HTTPException) as excInfoPayment:
            await validateBooking(validationData=validationRequest, dbSession=dbSession)
        assert excInfoPayment.value.status_code == 400
        assert "Booking requires payment verification" in excInfoPayment.value.detail
        
        # Validate booking rule when paid - Should succeed
        validationRequest.isPaid = True
        validationRequest.paymentReferenceId = "PAY-12345"
        validationResult = await validateBooking(validationData=validationRequest, dbSession=dbSession)
        assert validationResult["status"] == "VALID"
        assert validationResult["requiresApproval"] is True
        
        # 4. Restrict inactive / unpaid provider checks
        # Change tenant status to inactive/suspended (statusId = 2)
        activeTenant.statusId = 2
        await dbSession.commit()
        
        with pytest.raises(HTTPException) as excInfoTenant:
            await validateBooking(validationData=validationRequest, dbSession=dbSession)
        assert excInfoTenant.value.status_code == 400
        assert "Service provider (tenant) is inactive" in excInfoTenant.value.detail

# Test Availability Overlaps
@pytest.mark.asyncio
async def testAvailabilityTimingsAndOverlaps(testDb):
    """
    Verifies ServiceAvailability timing slots setup and overlap check validations.
    """
    async with testDb() as dbSession:
        tenantId = uuid.uuid4()
        
        # Create category and service
        categoryObj = await createCategory(
            categoryData=ServiceCategoryCreate(
                tenantId=tenantId, categoryName="Tutoring", categorySlug="tutoring"
            ),
            dbSession=dbSession
        )
        serviceObj = await createService(
            serviceData=ServiceCreate(
                tenantId=tenantId,
                categoryId=categoryObj.id,
                serviceName="Maths Class",
                serviceSlug="maths-class",
                serviceType="ONLINE",
                pricing=Decimal("200.00"),
                duration=60
            ),
            dbSession=dbSession
        )
        await dbSession.commit()
        
        # Add a valid timing slot: Mon (0), 09:00 - 11:00
        slotCreate = ServiceAvailabilityCreate(
            tenantId=tenantId,
            serviceId=serviceObj.id,
            dayOfWeek=0,
            startTime="09:00",
            endTime="11:00"
        )
        slotObj = await createAvailability(availabilityData=slotCreate, dbSession=dbSession)
        assert slotObj.id is not None
        
        # Try adding overlapping slot: Mon (0), 10:00 - 12:00 (overlaps with 09:00 - 11:00)
        overlapCreate = ServiceAvailabilityCreate(
            tenantId=tenantId,
            serviceId=serviceObj.id,
            dayOfWeek=0,
            startTime="10:00",
            endTime="12:00"
        )
        with pytest.raises(HTTPException) as excInfoOverlap:
            await createAvailability(availabilityData=overlapCreate, dbSession=dbSession)
        assert excInfoOverlap.value.status_code == 400
        assert "Overlap detected" in excInfoOverlap.value.detail
        
        # Add non-overlapping slot on the same day: Mon (0), 11:00 - 12:00 (borders are fine)
        validCreate = ServiceAvailabilityCreate(
            tenantId=tenantId,
            serviceId=serviceObj.id,
            dayOfWeek=0,
            startTime="11:00",
            endTime="12:00"
        )
        validObj = await createAvailability(availabilityData=validCreate, dbSession=dbSession)
        assert validObj.id is not None
        
        # Test update availability slot to overlap
        updateData = ServiceAvailabilityUpdate(startTime="10:30", endTime="11:30")
        with pytest.raises(HTTPException) as excInfoUpdateOverlap:
            await updateAvailability(availabilityId=validObj.id, updateData=updateData, dbSession=dbSession)
        assert excInfoUpdateOverlap.value.status_code == 400
        assert "Overlap detected" in excInfoUpdateOverlap.value.detail

        # Test invalid time order (startTime >= endTime)
        invalidOrderCreate = ServiceAvailabilityCreate(
            tenantId=tenantId,
            serviceId=serviceObj.id,
            dayOfWeek=0,
            startTime="14:00",
            endTime="13:00"
        )
        with pytest.raises(HTTPException) as excInfoOrder:
            await createAvailability(availabilityData=invalidOrderCreate, dbSession=dbSession)
        assert excInfoOrder.value.status_code == 400
        assert "Start time must be before end time" in excInfoOrder.value.detail

        # Test invalid format (non HH:MM)
        invalidFormatCreate = ServiceAvailabilityCreate(
            tenantId=tenantId,
            serviceId=serviceObj.id,
            dayOfWeek=0,
            startTime="9:00",
            endTime="11:00"
        )
        with pytest.raises(HTTPException) as excInfoFormat:
            await createAvailability(availabilityData=invalidFormatCreate, dbSession=dbSession)
        assert excInfoFormat.value.status_code == 400
        assert "Start time and end time must be in HH:MM format" in excInfoFormat.value.detail
