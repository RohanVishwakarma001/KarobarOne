# Owner: mousamdas156@gmail.com
"""
Unit tests for Tenant & Subscription engine module.
"""
# Import asyncio for async tests handling
import asyncio
# Import Decimal for monetary parameters
from decimal import Decimal
# Import pytest for testing framework
import pytest
# Import pytest_asyncio for async fixtures
import pytest_asyncio
# Import uuid for entity lookup identifiers
import uuid

# Import SQLAlchemy async DB engine and session maker tools
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# Import select query builder from SQLAlchemy
from sqlalchemy import select
# Import compilation rules from SQLAlchemy extension
from sqlalchemy.ext.compiler import compiles
# Import Postgres-specific types for custom SQLite compilation overrides
from sqlalchemy.dialects.postgresql import JSONB, UUID as PostgresUUID

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"

@compiles(PostgresUUID, "sqlite")
def compile_uuid_sqlite(type_, compiler, **kw):
    return "VARCHAR(36)"

# Import declarative Base mapping
from app.db.base import Base
# Import central models registry to load ORM schemas
from app.db.modelsRegistry import *

# Import backend business logic services
from app.services.tenantService import TenantService
from app.services.tenantSettingsService import TenantSettingsService
from app.services.billingRuleService import BillingRuleService
from app.services.tenantPlanService import TenantPlanService
from app.services.planService import PlanService
from app.services.featureService import FeatureService

# Import Pydantic validation schemas
from app.schemas.tenant import TenantCreate, TenantUpdate
from app.schemas.tenantSettings import TenantSettingsUpdate
from app.schemas.billingRule import BillingRuleCreate, BillingRuleUpdate
from app.schemas.subscriptionPlan import PlanCreate
from app.schemas.planFeature import FeatureCreate
from app.schemas.tenantPlan import TenantPlanAssign

# Import feature gating logic
from app.core.featureGate import getTenantFeatureValue


@pytest_asyncio.fixture(scope="function")
async def testDb():
    # Create in-memory SQLite engine
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    # SQLite does not support JSONB natively, so we override compile rules if needed, 
    # but SQLAlchemy 2.0 has built-in compilation fallbacks.
    async with engine.begin() as conn:
        tables_to_create = [
            Tenant.__table__,
            TenantStatus.__table__,
            TenantDomainMapping.__table__,
            TenantPlanMapping.__table__,
            TenantPlanHistory.__table__,
            SubscriptionPlan.__table__,
            PlanFeature.__table__,
            TenantSettings.__table__,
            BillingRule.__table__,
        ]
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=tables_to_create))
        
    sessionFactory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with sessionFactory() as session:
        # Seed TenantStatus
        status_active = TenantStatus(id=1, statusName="ACTIVE", statusDescription="Active status")
        status_pending = TenantStatus(id=2, statusName="PENDING", statusDescription="Pending status")
        status_suspended = TenantStatus(id=3, statusName="SUSPENDED", statusDescription="Suspended status")
        
        session.add_all([status_active, status_pending, status_suspended])
        await session.commit()
        
    yield sessionFactory
    
    async with engine.begin() as conn:
        tables_to_create = [
            Tenant.__table__,
            TenantStatus.__table__,
            TenantDomainMapping.__table__,
            TenantPlanMapping.__table__,
            TenantPlanHistory.__table__,
            SubscriptionPlan.__table__,
            PlanFeature.__table__,
            TenantSettings.__table__,
            BillingRule.__table__,
        ]
        await conn.run_sync(lambda sync_conn: Base.metadata.drop_all(sync_conn, tables=tables_to_create))


@pytest.mark.asyncio
async def test_tenant_crud_and_status(testDb):
    async with testDb() as session:
        tenantService = TenantService(session)
        
        # Test Create
        tenant_in = TenantCreate(
            gstNumber="22ABCDE1234F1Z5",
            panNumber="ABCDE1234F",
            businessName="Saikat Enterprises",
            legalName="Saikat Enterprises Private Limited",
            email="owner@saikat.com",
            mobile="+919876543210",
            ownerName="Saikat Pradhan",
            businessAddressLine1="Street 1",
            city="Kolkata",
            state="West Bengal",
            postalCode="700001",
            businessType="Retail",
            employeeCount=5,
        )
        tenant = await tenantService.createTenant(tenant_in)
        assert tenant.id is not None
        assert tenant.businessName == "Saikat Enterprises"
        assert tenant.statusId == 2  # default is PENDING
        assert tenant.isActive is True
        
        # Test Get
        tenant_get = await tenantService.getTenant(tenant.id)
        assert tenant_get.email == "owner@saikat.com"
        
        # Test Update Status
        tenant_updated = await tenantService.updateStatus(tenant.id, 1)
        assert tenant_updated.statusId == 1
        
        # Test List Active (1 item)
        tenants, count = await tenantService.listTenants(limit=10)
        assert count == 1
        assert tenants[0].id == tenant.id
        
        # Test Soft Delete
        await tenantService.deleteTenant(tenant.id)
        
        # Verify get throws NotFoundError
        from app.core.exceptionsCompat import NotFoundError
        with pytest.raises(NotFoundError):
            await tenantService.getTenant(tenant.id)
            
        # Verify list active returns 0 items
        tenants, count = await tenantService.listTenants(limit=10)
        assert count == 0


@pytest.mark.asyncio
async def test_tenant_settings(testDb):
    async with testDb() as session:
        tenantService = TenantService(session)
        settingsService = TenantSettingsService(session)
        
        # Create a tenant
        tenant_in = TenantCreate(
            panNumber="ABCDE1234F",
            businessName="Saikat Enterprises",
            legalName="Saikat Enterprises Private Limited",
            email="owner@saikat.com",
            mobile="+919876543210",
            ownerName="Saikat Pradhan",
            businessAddressLine1="Street 1",
            city="Kolkata",
            state="West Bengal",
            postalCode="700001",
            businessType="Retail",
        )
        tenant = await tenantService.createTenant(tenant_in)
        
        # Get settings (should create defaults if not exists)
        settings = await settingsService.getSettings(tenant.id)
        assert settings.currency == "INR"
        assert settings.timezone == "Asia/Kolkata"
        assert settings.enableNotifications is True
        
        # Update settings
        settings_update = TenantSettingsUpdate(
            currency="USD",
            timezone="America/New_York",
            enableNotifications=False,
        )
        updated_settings = await settingsService.updateSettings(tenant.id, settings_update)
        assert updated_settings.currency == "USD"
        assert updated_settings.timezone == "America/New_York"
        assert updated_settings.enableNotifications is False


@pytest.mark.asyncio
async def test_feature_gate_and_billing_rules(testDb):
    async with testDb() as session:
        tenantService = TenantService(session)
        planService = PlanService(session)
        featureService = FeatureService(session)
        tenantPlanService = TenantPlanService(session)
        billingRuleService = BillingRuleService(session)
        
        # 1. Create Tenant
        tenant_in = TenantCreate(
            panNumber="ABCDE1234F",
            businessName="Saikat Enterprises",
            legalName="Saikat Enterprises Private Limited",
            email="owner@saikat.com",
            mobile="+919876543210",
            ownerName="Saikat Pradhan",
            businessAddressLine1="Street 1",
            city="Kolkata",
            state="West Bengal",
            postalCode="700001",
            businessType="Retail",
        )
        tenant = await tenantService.createTenant(tenant_in)
        
        # 2. Create Plan
        plan_in = PlanCreate(
            planCode="PRO_PLAN",
            planName="Pro Plan",
            monthlyPrice=Decimal("999.00"),
            transactionCommissionPercent=Decimal("2.50"),
            isActive=True,
        )
        plan = await planService.createPlan(plan_in)
        
        # 3. Add Feature
        feature_in = FeatureCreate(
            featureName="Max Products",
            featureCode="max_products",
            featureValue=100,
        )
        await featureService.addFeature(plan.id, feature_in)
        
        # 4. Assign Plan to Tenant
        from datetime import date
        plan_assign = TenantPlanAssign(
            planId=plan.id,
            planStartDate=date.today(),
            autoRenew=True,
        )
        await tenantPlanService.assignPlan(tenant.id, plan_assign)
        
        # 5. Check Feature Gate value
        feature_val = await getTenantFeatureValue(session, tenant.id, "max_products")
        assert feature_val == 100
        
        # 6. Verify default commission calculation
        commission = await billingRuleService.calculateCommission(tenant.id, Decimal("1000.00"))
        # 2.5% of 1000 = 25.00
        assert commission == Decimal("25.00")
        
        # 7. Add Billing Rule to override commission percent
        rule_in = BillingRuleCreate(
            ruleName="Special Commission Percent Override",
            ruleCode="commission_percentage",
            ruleType="PERCENTAGE",
            ruleValue=Decimal("1.50"),
            isActive=True,
            appliesTo="ORDER",
        )
        await billingRuleService.createRule(plan.id, rule_in)
        
        # Calculate commission again (should use override of 1.5%)
        commission = await billingRuleService.calculateCommission(tenant.id, Decimal("1000.00"))
        # 1.5% of 1000 = 15.00
        assert commission == Decimal("15.00")
        
        # 8. Add flat fee rule
        flat_fee_in = BillingRuleCreate(
            ruleName="Transaction Flat Fee",
            ruleCode="commission_flat_fee",
            ruleType="FLAT_FEE",
            ruleValue=Decimal("5.00"),
            isActive=True,
            appliesTo="ORDER",
        )
        await billingRuleService.createRule(plan.id, flat_fee_in)
        
        # Calculate commission again (1.5% of 1000 + 5.00 flat fee = 20.00)
        commission = await billingRuleService.calculateCommission(tenant.id, Decimal("1000.00"))
        assert commission == Decimal("20.00")
