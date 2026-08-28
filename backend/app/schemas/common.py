"""
================================================================================
SCHEMAS: Shared Common Pydantic Models (FastAPI / Pydantic)
================================================================================
This file is used to define generic, reusable Pydantic schemas (such as pagination 
wrappers and general success messages) that are shared across different API routes.
"""

from typing import Generic, TypeVar
from pydantic import BaseModel, Field

# Generic Type variable to represent any response data model within pagination wrappers
T = TypeVar("T")


class PaginationParams(BaseModel):
    """
    Schema used to parse and validate incoming query parameters for list endpoints 
    that require server-side pagination.
    """
    # Number of database records to skip/offset
    skip: int = Field(default=0, ge=0, description="Records to skip for pagination offset")
    
    # Maximum number of database records to return in a single request
    limit: int = Field(default=20, ge=1, le=100, description="Max records to return in pagination limit")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Schema wrapper used to structure paginated responses sent back to the client.
    It encapsulates the actual records list along with count metadata.
    """
    # Paginated data items list
    items: list[T] = Field(..., description="List of actual data records matching the query")
    
    # Total count of all matching records in the database (unpaginated count)
    total: int = Field(..., description="Total count of available matching items in database")
    
    # Pagination skip offset used for this query
    skip: int = Field(..., description="Pagination offset applied")
    
    # Pagination limit size used for this query
    limit: int = Field(..., description="Pagination limit size applied")


class MessageResponse(BaseModel):
    """
    Generic message container schema.
    Used to send simple status updates or success confirmations (e.g. 'Delete successful').
    """
    # Response detail string
    detail: str = Field(..., description="Descriptive status update message content")
