# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/services/notificationService.py
# Purpose: Event-Driven Notification Service
# Last updated: 2026-07-31
# ================================================================================
"""
Notification service for sending alerts to users on key events.

Handles notification dispatch for:
  - Approval/rejection of submitted content
  - Plan limit warnings
  - Account security alerts (lockout, password changes)
  - Tenant status changes

Currently implements in-app notification storage. Email/SMS integrations
can be added as provider plugins.
"""

import uuid
from datetime import datetime, timezone
from enum import Enum

import structlog

logger = structlog.get_logger(__name__)


class NotificationType(str, Enum):
    """Notification category classifications."""
    APPROVAL_APPROVED = "approval_approved"
    APPROVAL_REJECTED = "approval_rejected"
    PLAN_LIMIT_WARNING = "plan_limit_warning"
    PLAN_UPGRADED = "plan_upgraded"
    PLAN_DOWNGRADED = "plan_downgraded"
    ACCOUNT_LOCKED = "account_locked"
    PASSWORD_CHANGED = "password_changed"
    TENANT_SUSPENDED = "tenant_suspended"
    TENANT_REACTIVATED = "tenant_reactivated"


class NotificationService:
    """
    Service for creating and dispatching notifications to users.

    In the current implementation, notifications are logged and can be
    extended with email, SMS, push notification, or webhook providers.
    """

    @staticmethod
    async def notify(
        recipient_id: uuid.UUID,
        notification_type: NotificationType,
        title: str,
        message: str,
        metadata: dict | None = None,
    ) -> None:
        """
        Queue a notification for a user.

        Parameters:
            recipient_id: UUID of the user to notify.
            notification_type: Category of the notification.
            title: Short notification title.
            message: Detailed notification message body.
            metadata: Optional additional context (entity ID, approval ID, etc.).
        """
        logger.info(
            "Notification dispatched",
            recipientId=str(recipient_id),
            type=notification_type.value,
            title=title,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {},
        )
        # TODO: Persist to notifications table for in-app notification center
        # TODO: Dispatch via email provider (SendGrid, SES, etc.)
        # TODO: Push notification via FCM/APNs for mobile apps

    @staticmethod
    async def notify_approval_result(
        store_owner_id: uuid.UUID,
        entity_type: str,
        entity_name: str,
        approved: bool,
        reviewer_notes: str | None = None,
    ) -> None:
        """
        Send notification to store owner about approval/rejection of their submitted content.

        Parameters:
            store_owner_id: UUID of the store owner to notify.
            entity_type: Type of entity (product, section, service, etc.).
            entity_name: Human-readable name/title of the entity.
            approved: True if approved, False if rejected.
            reviewer_notes: Optional notes from the reviewer explaining the decision.
        """
        if approved:
            await NotificationService.notify(
                recipient_id=store_owner_id,
                notification_type=NotificationType.APPROVAL_APPROVED,
                title=f"Your {entity_type} has been approved",
                message=f"'{entity_name}' has been approved and is now live on your store.",
                metadata={"entityType": entity_type, "entityName": entity_name},
            )
        else:
            rejection_reason = f" Reason: {reviewer_notes}" if reviewer_notes else ""
            await NotificationService.notify(
                recipient_id=store_owner_id,
                notification_type=NotificationType.APPROVAL_REJECTED,
                title=f"Your {entity_type} was not approved",
                message=f"'{entity_name}' was not approved.{rejection_reason} "
                f"Please review and resubmit.",
                metadata={
                    "entityType": entity_type,
                    "entityName": entity_name,
                    "reviewerNotes": reviewer_notes,
                },
            )

    @staticmethod
    async def notify_plan_limit_warning(
        store_owner_id: uuid.UUID,
        resource: str,
        current_count: int,
        limit: int,
    ) -> None:
        """
        Warn store owner they are approaching or have hit a plan limit.

        Parameters:
            store_owner_id: UUID of the store owner.
            resource: Resource type (products, services, images).
            current_count: Current count of the resource.
            limit: Maximum allowed on current plan.
        """
        await NotificationService.notify(
            recipient_id=store_owner_id,
            notification_type=NotificationType.PLAN_LIMIT_WARNING,
            title=f"You've reached your {resource} limit",
            message=f"You have {current_count}/{limit} {resource} on your current plan. "
            f"Upgrade to add more.",
            metadata={
                "resource": resource,
                "currentCount": current_count,
                "limit": limit,
            },
        )
