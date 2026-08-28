# Owner: mousamdas156@gmail.com
"""
================================================================================
SCHEMAS: Domain Mapping Validations (FastAPI / Pydantic)
================================================================================
This file is used to define Pydantic schemas (data models) for tenant subdomains 
and custom domains. It handles validation of input data from incoming HTTP requests 
and structures the response data sent back to the client.
"""

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class DomainCreate(BaseModel):
    """
    Schema used when registering or creating a new domain mapping for a tenant.
    It defines and validates the fields required from the request body.
    """
    # The routing type: 'SUBDOMAIN' or 'CUSTOM'
    domainType: str = Field(..., max_length=20, description="Type of domain mapping: SUBDOMAIN or CUSTOM")
    
    # Platform subdomain name (e.g. 'tenantname' for tenantname.karobar.com)
    subDomain: str | None = Field(None, max_length=100, description="Platform subdomain name, must be globally unique")
    
    # Custom external domain URL (e.g. 'www.tenantbusiness.in')
    customDomain: str | None = Field(None, max_length=255, description="Full external custom domain URL, must be globally unique")
    
    # True if this is the primary entry point/URL for the tenant's app
    isPrimary: bool = Field(False, description="Flags this domain as the primary entry point for the tenant")
    
    # Date when the Let's Encrypt / custom certificate expires
    sslExpiry: datetime | None = Field(None, description="SSL certificate expiration timestamp")
    dnsVerified: bool = Field(False, description="Whether DNS verification has completed")


class DomainUpdate(BaseModel):
    """
    Schema used when updating an existing domain mapping's configuration.
    All fields are optional because the client can send partial updates (PATCH).
    """
    domainType: str | None = Field(None, max_length=20, description="Updated domain type (SUBDOMAIN/CUSTOM)")
    subDomain: str | None = Field(None, max_length=100, description="Updated platform subdomain")
    customDomain: str | None = Field(None, max_length=255, description="Updated custom domain URL")
    isPrimary: bool | None = Field(None, description="Change primary routing status")
    sslExpiry: datetime | None = Field(None, description="Updated SSL expiry timestamp")


class DomainRead(BaseModel):
    """
    Schema used to serialize and return the domain mapping details from the database.
    It guarantees the output response contains standard structured fields.
    """
    # Database PK ID for the domain mapping record
    id: uuid.UUID
    
    # The owner tenant's UUID
    tenantId: uuid.UUID
    
    domainType: str
    subDomain: str | None = None
    customDomain: str | None = None
    isPrimary: bool
    sslExpiry: datetime | None = None
    
    # Audit log when this routing was first registered
    createdAt: datetime

    # Enable ORM attribute reading compatibility
    model_config = {"from_attributes": True}
