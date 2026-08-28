# Owner-pradhansaikat123@gmail.com

from fastapi import APIRouter, Depends, HTTPException, status
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.db.session import getDb
from serviceEngine.models import (
    ServiceCategory,
    Service,
    BookingRule,
    ServiceAvailability,
)
from serviceEngine.schemas import (
    ServiceCategoryCreate,
    ServiceCategoryUpdate,
    ServiceCategoryResponse,
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse,
    BookingRuleCreate,
    BookingRuleResponse,
    ServiceAvailabilityCreate,
    ServiceAvailabilityUpdate,
    ServiceAvailabilityResponse,
    BookingValidationRequest,
)
from app.db.models.tenant import Tenant
from app.db.models.tenantPlanMapping import TenantPlanMapping

serviceEngineRouter = APIRouter(prefix="/service-engine", tags=["Service Engine"])

@serviceEngineRouter.post("/categories", response_model=ServiceCategoryResponse)
async def createCategory(categoryData: ServiceCategoryCreate, dbSession: AsyncSession = Depends(getDb)) -> ServiceCategory:
    """
    Create a new Service Category with duplicate validation.
    """
    duplicateQuery = select(ServiceCategory).where(
        ServiceCategory.tenantId == categoryData.tenantId,
        ServiceCategory.isActive == True,
        (ServiceCategory.categoryName == categoryData.categoryName) |
        (ServiceCategory.categorySlug == categoryData.categorySlug)
    )
    duplicateResult = await dbSession.execute(duplicateQuery)
    existingCategory = duplicateResult.scalar_one_or_none()
    
    if existingCategory:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name or slug already exists for the tenant"
        )
        
    from app.core.config import getSettings
    settings = getSettings()
    newCategory = ServiceCategory(
        tenantId=categoryData.tenantId,
        categoryName=categoryData.categoryName,
        categorySlug=categoryData.categorySlug,
        categoryType=categoryData.categoryType or "SERVICE",
        isActive=True,
        createdBy=UUID(settings.defaultUserId),
        approvalStatus="APPROVED"
    )
    dbSession.add(newCategory)
    await dbSession.flush()
    await dbSession.refresh(newCategory)
    return newCategory

@serviceEngineRouter.get("/categories", response_model=list[ServiceCategoryResponse])
async def listCategories(tenantId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Retrieve all active categories for a specific tenant.
    """
    listQuery = select(ServiceCategory).where(
        ServiceCategory.tenantId == tenantId,
        ServiceCategory.isActive == True
    )
    queryResult = await dbSession.execute(listQuery)
    return queryResult.scalars().all()

@serviceEngineRouter.get("/categories/{categoryId}", response_model=ServiceCategoryResponse)
async def getCategory(categoryId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Retrieve details of a single category.
    """
    categoryQuery = select(ServiceCategory).where(
        ServiceCategory.id == categoryId,
        ServiceCategory.isActive == True
    )
    queryResult = await dbSession.execute(categoryQuery)
    categoryObj = queryResult.scalar_one_or_none()
    if not categoryObj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return categoryObj

@serviceEngineRouter.put("/categories/{categoryId}", response_model=ServiceCategoryResponse)
async def updateCategory(categoryId: UUID, updateData: ServiceCategoryUpdate, dbSession: AsyncSession = Depends(getDb)):
    """
    Update a service category's attributes with duplicate validation.
    """
    categoryQuery = select(ServiceCategory).where(
        ServiceCategory.id == categoryId,
        ServiceCategory.isActive == True
    )
    queryResult = await dbSession.execute(categoryQuery)
    categoryObj = queryResult.scalar_one_or_none()
    if not categoryObj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
        
    if updateData.categoryName or updateData.categorySlug:
        newName = updateData.categoryName or categoryObj.categoryName
        newSlug = updateData.categorySlug or categoryObj.categorySlug
        duplicateQuery = select(ServiceCategory).where(
            ServiceCategory.tenantId == categoryObj.tenantId,
            ServiceCategory.id != categoryId,
            ServiceCategory.isActive == True,
            (ServiceCategory.categoryName == newName) | (ServiceCategory.categorySlug == newSlug)
        )
        duplicateResult = await dbSession.execute(duplicateQuery)
        existingCategory = duplicateResult.scalar_one_or_none()
        if existingCategory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name or slug already exists for the tenant"
            )

    if updateData.categoryName is not None:
        categoryObj.categoryName = updateData.categoryName
    if updateData.categorySlug is not None:
        categoryObj.categorySlug = updateData.categorySlug
    if updateData.categoryType is not None:
        categoryObj.categoryType = updateData.categoryType
    if updateData.isActive is not None:
        categoryObj.isActive = updateData.isActive
        
    await dbSession.flush()
    await dbSession.refresh(categoryObj)
    return categoryObj

@serviceEngineRouter.delete("/categories/{categoryId}")
async def deleteCategory(categoryId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Soft delete a service category.
    """
    categoryQuery = select(ServiceCategory).where(
        ServiceCategory.id == categoryId,
        ServiceCategory.isActive == True
    )
    queryResult = await dbSession.execute(categoryQuery)
    categoryObj = queryResult.scalar_one_or_none()
    if not categoryObj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    categoryObj.isActive = False
    await dbSession.flush()
    return {"message": "Category deleted successfully"}

@serviceEngineRouter.post("/services", response_model=ServiceResponse)
async def createService(serviceData: ServiceCreate, dbSession: AsyncSession = Depends(getDb)):
    """
    Create a new Service.
    """
    from app.core.planGuard import PlanGuard
    guard = PlanGuard(dbSession)
    await guard.check_service_limit(serviceData.tenantId)

    if serviceData.serviceType not in {"PHYSICAL", "ONLINE"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service type must be either PHYSICAL or ONLINE"
        )
        
    categoryQuery = select(ServiceCategory).where(
        ServiceCategory.id == serviceData.categoryId,
        ServiceCategory.isActive == True
    )
    categoryResult = await dbSession.execute(categoryQuery)
    categoryObj = categoryResult.scalar_one_or_none()
    if not categoryObj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Valid active category required"
        )
        
    newService = Service(
        tenantId=serviceData.tenantId,
        categoryId=serviceData.categoryId,
        serviceName=serviceData.serviceName,
        serviceSlug=serviceData.serviceSlug,
        serviceType=serviceData.serviceType,
        description=serviceData.description,
        pricing=serviceData.pricing,
        duration=serviceData.duration,
        media=serviceData.media,
        metaTitle=serviceData.metaTitle,
        metaDescription=serviceData.metaDescription,
        metaSlug=serviceData.metaSlug,
        approvalStatus=serviceData.approvalStatus or "PENDING",
        isActive=True
    )
    dbSession.add(newService)
    await dbSession.flush()
    await dbSession.refresh(newService)
    return newService

@serviceEngineRouter.get("/services", response_model=list[ServiceResponse])
async def listServices(tenantId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Retrieve all active services for a tenant.
    """
    listQuery = select(Service).where(
        Service.tenantId == tenantId,
        Service.isActive == True
    )
    queryResult = await dbSession.execute(listQuery)
    return queryResult.scalars().all()

@serviceEngineRouter.get("/services/{serviceId}", response_model=ServiceResponse)
async def getService(serviceId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Retrieve details of a single service.
    """
    serviceQuery = select(Service).where(
        Service.id == serviceId,
        Service.isActive == True
    )
    queryResult = await dbSession.execute(serviceQuery)
    serviceObj = queryResult.scalar_one_or_none()
    if not serviceObj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    return serviceObj

@serviceEngineRouter.put("/services/{serviceId}", response_model=ServiceResponse)
async def updateService(serviceId: UUID, updateData: ServiceUpdate, dbSession: AsyncSession = Depends(getDb)):
    """
    Update service details with optional category validation.
    """
    serviceQuery = select(Service).where(
        Service.id == serviceId,
        Service.isActive == True
    )
    queryResult = await dbSession.execute(serviceQuery)
    serviceObj = queryResult.scalar_one_or_none()
    if not serviceObj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
        
    if updateData.serviceType is not None and updateData.serviceType not in {"PHYSICAL", "ONLINE"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service type must be either PHYSICAL or ONLINE"
        )
        
    if updateData.categoryId is not None:
        categoryQuery = select(ServiceCategory).where(
            ServiceCategory.id == updateData.categoryId,
            ServiceCategory.isActive == True
        )
        categoryResult = await dbSession.execute(categoryQuery)
        categoryObj = categoryResult.scalar_one_or_none()
        if not categoryObj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valid active category required"
            )
        serviceObj.categoryId = updateData.categoryId

    if updateData.serviceName is not None:
        serviceObj.serviceName = updateData.serviceName
    if updateData.serviceSlug is not None:
        serviceObj.serviceSlug = updateData.serviceSlug
    if updateData.serviceType is not None:
        serviceObj.serviceType = updateData.serviceType
    if updateData.description is not None:
        serviceObj.description = updateData.description
    if updateData.pricing is not None:
        serviceObj.pricing = updateData.pricing
    if updateData.duration is not None:
        serviceObj.duration = updateData.duration
    if updateData.media is not None:
        serviceObj.media = updateData.media
    if updateData.metaTitle is not None:
        serviceObj.metaTitle = updateData.metaTitle
    if updateData.metaDescription is not None:
        serviceObj.metaDescription = updateData.metaDescription
    if updateData.metaSlug is not None:
        serviceObj.metaSlug = updateData.metaSlug
    if updateData.approvalStatus is not None:
        serviceObj.approvalStatus = updateData.approvalStatus
    if updateData.isActive is not None:
        serviceObj.isActive = updateData.isActive
        
    await dbSession.flush()
    await dbSession.refresh(serviceObj)
    return serviceObj

@serviceEngineRouter.delete("/services/{serviceId}")
async def deleteService(serviceId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Soft delete a service.
    """
    serviceQuery = select(Service).where(
        Service.id == serviceId,
        Service.isActive == True
    )
    queryResult = await dbSession.execute(serviceQuery)
    serviceObj = queryResult.scalar_one_or_none()
    if not serviceObj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    serviceObj.isActive = False
    await dbSession.flush()
    return {"message": "Service deleted successfully"}

@serviceEngineRouter.post("/services/{serviceId}/submit-approval", response_model=ServiceResponse)
async def submitApproval(serviceId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Submit service details for approval workflow.
    """
    serviceQuery = select(Service).where(
        Service.id == serviceId,
        Service.isActive == True
    )
    queryResult = await dbSession.execute(serviceQuery)
    serviceObj = queryResult.scalar_one_or_none()
    if not serviceObj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    serviceObj.approvalStatus = "PENDING"
    await dbSession.flush()
    await dbSession.refresh(serviceObj)
    return serviceObj

@serviceEngineRouter.post("/booking-rules", response_model=BookingRuleResponse)
async def createBookingRule(ruleData: BookingRuleCreate, dbSession: AsyncSession = Depends(getDb)):
    """
    Configure booking modes and rules for a service.
    """
    if ruleData.bookingMode not in {"BOOKING_ONLY", "BOOKING_AND_PAYMENT"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking mode must be either BOOKING_ONLY or BOOKING_AND_PAYMENT"
        )
        
    serviceQuery = select(Service).where(
        Service.id == ruleData.serviceId,
        Service.isActive == True
    )
    serviceResult = await dbSession.execute(serviceQuery)
    serviceObj = serviceResult.scalar_one_or_none()
    if not serviceObj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Valid active service required"
        )
        
    existingQuery = select(BookingRule).where(
        BookingRule.serviceId == ruleData.serviceId,
        BookingRule.isActive == True
    )
    existingResult = await dbSession.execute(existingQuery)
    existingRule = existingResult.scalar_one_or_none()
    
    if existingRule:
        existingRule.bookingMode = ruleData.bookingMode
        existingRule.requiresApproval = ruleData.requiresApproval
        await dbSession.flush()
        await dbSession.refresh(existingRule)
        return existingRule
        
    newRule = BookingRule(
        tenantId=ruleData.tenantId,
        serviceId=ruleData.serviceId,
        bookingMode=ruleData.bookingMode,
        requiresApproval=ruleData.requiresApproval,
        isActive=True
    )
    dbSession.add(newRule)
    await dbSession.flush()
    await dbSession.refresh(newRule)
    return newRule

@serviceEngineRouter.get("/booking-rules/service/{serviceId}", response_model=BookingRuleResponse)
async def getBookingRule(serviceId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Retrieve active booking rules for a service.
    """
    ruleQuery = select(BookingRule).where(
        BookingRule.serviceId == serviceId,
        BookingRule.isActive == True
    )
    queryResult = await dbSession.execute(ruleQuery)
    ruleObj = queryResult.scalar_one_or_none()
    if not ruleObj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking rules not found for this service"
        )
    return ruleObj

@serviceEngineRouter.post("/booking-rules/validate-booking")
async def validateBooking(validationData: BookingValidationRequest, dbSession: AsyncSession = Depends(getDb)):
    """
    Validate booking rules and provider's active subscription status.
    """
    tenantQuery = select(Tenant).where(Tenant.id == validationData.tenantId)
    tenantResult = await dbSession.execute(tenantQuery)
    tenantObj = tenantResult.scalar_one_or_none()
    if not tenantObj or tenantObj.statusId != 1 or not tenantObj.isActive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service provider (tenant) is inactive, suspended, or unpaid"
        )
        
    planQuery = select(TenantPlanMapping).where(
        TenantPlanMapping.tenantId == validationData.tenantId,
        TenantPlanMapping.statusId == 1
    )
    planResult = await dbSession.execute(planQuery)
    planObj = planResult.scalar_one_or_none()
    if not planObj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking blocked: Service provider has no active plan"
        )

    serviceQuery = select(Service).where(
        Service.id == validationData.serviceId,
        Service.isActive == True
    )
    serviceResult = await dbSession.execute(serviceQuery)
    serviceObj = serviceResult.scalar_one_or_none()
    if not serviceObj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service does not exist or is inactive"
        )
        
    ruleQuery = select(BookingRule).where(
        BookingRule.serviceId == validationData.serviceId,
        BookingRule.isActive == True
    )
    ruleResult = await dbSession.execute(ruleQuery)
    ruleObj = ruleResult.scalar_one_or_none()
    
    if ruleObj and ruleObj.bookingMode == "BOOKING_AND_PAYMENT":
        if not validationData.isPaid or not validationData.paymentReferenceId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking requires payment verification before confirmation"
            )
            
    return {
        "status": "VALID",
        "requiresApproval": ruleObj.requiresApproval if ruleObj else False
    }

@serviceEngineRouter.post("/availabilities", response_model=ServiceAvailabilityResponse)
async def createAvailability(availabilityData: ServiceAvailabilityCreate, dbSession: AsyncSession = Depends(getDb)):
    """
    Configure availability timing with overlap validation.
    """
    if availabilityData.dayOfWeek < 0 or availabilityData.dayOfWeek > 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Day of week must be between 0 (Monday) and 6 (Sunday)"
        )
        
    timePattern = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    if not timePattern.match(availabilityData.startTime) or not timePattern.match(availabilityData.endTime):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time and end time must be in HH:MM format (24-hour)"
        )
        
    if availabilityData.startTime >= availabilityData.endTime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time"
        )
        
    serviceQuery = select(Service).where(
        Service.id == availabilityData.serviceId,
        Service.isActive == True
    )
    serviceResult = await dbSession.execute(serviceQuery)
    serviceObj = serviceResult.scalar_one_or_none()
    if not serviceObj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Valid active service required"
        )

    overlapQuery = select(ServiceAvailability).where(
        ServiceAvailability.serviceId == availabilityData.serviceId,
        ServiceAvailability.dayOfWeek == availabilityData.dayOfWeek,
        ServiceAvailability.isActive == True
    )
    overlapResult = await dbSession.execute(overlapQuery)
    existingSlots = overlapResult.scalars().all()
    
    for slot in existingSlots:
        if availabilityData.startTime < slot.endTime and slot.startTime < availabilityData.endTime:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Overlap detected with existing schedule slot"
            )
            
    newAvailability = ServiceAvailability(
        tenantId=availabilityData.tenantId,
        serviceId=availabilityData.serviceId,
        dayOfWeek=availabilityData.dayOfWeek,
        startTime=availabilityData.startTime,
        endTime=availabilityData.endTime,
        isActive=True
    )
    dbSession.add(newAvailability)
    await dbSession.flush()
    await dbSession.refresh(newAvailability)
    return newAvailability

@serviceEngineRouter.get("/availabilities/service/{serviceId}", response_model=list[ServiceAvailabilityResponse])
async def listAvailabilities(serviceId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Retrieve all active availability slots for a service.
    """
    listQuery = select(ServiceAvailability).where(
        ServiceAvailability.serviceId == serviceId,
        ServiceAvailability.isActive == True
    )
    queryResult = await dbSession.execute(listQuery)
    return queryResult.scalars().all()

@serviceEngineRouter.put("/availabilities/{availabilityId}", response_model=ServiceAvailabilityResponse)
async def updateAvailability(availabilityId: UUID, updateData: ServiceAvailabilityUpdate, dbSession: AsyncSession = Depends(getDb)):
    """
    Update details of an availability slot with overlap validation.
    """
    availQuery = select(ServiceAvailability).where(
        ServiceAvailability.id == availabilityId,
        ServiceAvailability.isActive == True
    )
    queryResult = await dbSession.execute(availQuery)
    availObj = queryResult.scalar_one_or_none()
    if not availObj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found"
        )
        
    newDay = updateData.dayOfWeek if updateData.dayOfWeek is not None else availObj.dayOfWeek
    newStart = updateData.startTime if updateData.startTime is not None else availObj.startTime
    newEnd = updateData.endTime if updateData.endTime is not None else availObj.endTime
    
    if updateData.startTime is not None or updateData.endTime is not None or updateData.dayOfWeek is not None:
        timePattern = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
        if not timePattern.match(newStart) or not timePattern.match(newEnd):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start time and end time must be in HH:MM format (24-hour)"
            )
            
        if newStart >= newEnd:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start time must be before end time"
            )

        overlapQuery = select(ServiceAvailability).where(
            ServiceAvailability.serviceId == availObj.serviceId,
            ServiceAvailability.dayOfWeek == newDay,
            ServiceAvailability.id != availabilityId,
            ServiceAvailability.isActive == True
        )
        overlapResult = await dbSession.execute(overlapQuery)
        existingSlots = overlapResult.scalars().all()
        
        for slot in existingSlots:
            if newStart < slot.endTime and slot.startTime < newEnd:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Overlap detected with existing schedule slot"
                )

    if updateData.dayOfWeek is not None:
        availObj.dayOfWeek = updateData.dayOfWeek
    if updateData.startTime is not None:
        availObj.startTime = updateData.startTime
    if updateData.endTime is not None:
        availObj.endTime = updateData.endTime
    if updateData.isActive is not None:
        availObj.isActive = updateData.isActive
        
    await dbSession.flush()
    await dbSession.refresh(availObj)
    return availObj

@serviceEngineRouter.delete("/availabilities/{availabilityId}")
async def deleteAvailability(availabilityId: UUID, dbSession: AsyncSession = Depends(getDb)):
    """
    Soft delete or deactivate an availability slot.
    """
    availQuery = select(ServiceAvailability).where(
        ServiceAvailability.id == availabilityId,
        ServiceAvailability.isActive == True
    )
    queryResult = await dbSession.execute(availQuery)
    availObj = queryResult.scalar_one_or_none()
    if not availObj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found"
        )
    availObj.isActive = False
    await dbSession.flush()
    return {"message": "Availability slot deactivated successfully"}
