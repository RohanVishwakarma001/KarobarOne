# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: db/modelsRegistry.py — Central Model Registry (Alembic)
# ================================================================================
# Why this file is used:
#   - It imports all database schemas to register metadata parameters. Alembic
#     uses this registry to safely auto-detect and generate database migration scripts.
# ================================================================================
from app.db.base import Base

# Import all models to register them on Base.metadata for Alembic/SQLAlchemy
from app.db.models.brands import Brand, BrandApproval
from app.db.models.categories import Category
from app.db.models.tags import Tag, TagMapping
from app.db.models.customers import (
    Customer, CustomerAddress, CustomerSession, CustomerActivityLog,
    CustomerGroup, CustomerGroupMember, CustomerNote, CustomerConsentLog,
    CustomerPasswordResetToken, GuestCheckoutLog, EntityVerification
)
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.permission import Permission
from app.db.models.userRoleMapping import UserRoleMapping
from app.db.models.rolePermissionMapping import RolePermissionMapping
from app.db.models.storeStaffPermission import StoreStaffPermission
from app.db.models.userSession import UserSession
from app.db.models.userSecuritySetting import UserSecuritySetting
from app.db.models.refreshToken import RefreshToken
from app.db.models.passwordResetToken import PasswordResetToken
from app.db.models.otpVerification import OtpVerification
from app.db.models.loginHistory import LoginHistory

from app.db.models.tenant import Tenant
from app.db.models.subscriptionPlan import SubscriptionPlan
from app.db.models.planFeature import PlanFeature
from app.db.models.tenantPlanMapping import TenantPlanMapping
from app.db.models.tenantPlanHistory import TenantPlanHistory
from app.db.models.tenantDomainMapping import TenantDomainMapping
from app.db.models.tenantStatus import TenantStatus
from app.db.models.tenantSettings import TenantSettings
from app.db.models.billingRule import BillingRule

from app.db.models.mediaFile import MediaFile
from app.db.models.mediaMetadata import MediaMetadata
from app.db.models.mediaUploadLog import MediaUploadLog
from app.db.models.mediaVariant import MediaVariant
from app.db.models.seoMetadata import SeoMetadata

from app.db.models.store import Store
from app.db.models.storeBankAccount import StoreBankAccount
from app.db.models.section import Section
from app.db.models.socialLink import SocialLink
from app.db.models.socialPlatform import SocialPlatform
from app.db.models.websiteTheme import WebsiteTheme

from app.db.models.approvals import (
    ApprovalRequest, ApprovalRequestVersion, EntityVersion, AuditLog, StatusHistory, ReviewQueue
)

from app.db.models.chatUser import ChatUser
from app.db.models.conversation import Conversation
from app.db.models.message import Message

# Import service engine models (Owner - pradhansaikat123@gmail.com)
from serviceEngine.models import ServiceCategory, Service, BookingRule, ServiceAvailability

# Import customer engine models (Owner - pradhansaikat123@gmail.com)
from customerEngine.models import EngineCustomer, EngineCustomerAddress, EngineCustomerOrder
# Website module models
from app.db.models.websiteSetting import WebsiteSetting
from app.db.models.websiteDeployment import WebsiteDeployment
from app.db.models.websitePublishLog import WebsitePublishLog
from app.db.models.websiteAIContent import WebsiteAIContent
