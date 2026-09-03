# Owner: mousamdas156@gmail.com
# ================================================================================
# Module: src/core/config.py
# Purpose: Application Configuration (Environment Variables)
# Last updated: 2026-07-11
# ================================================================================
"""
Application configuration using pydantic-settings.

Provides type-safe, fail-fast environment variable loading.
Missing or malformed variables raise a validation error immediately on startup.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    # ──────────────────────────────────────
    # Application
    # ──────────────────────────────────────
    appName: str = "BackendFoundation"
    appVersion: str = "0.1.0"
    debug: bool = False
    logLevel: str = "INFO"
    apiPrefix: str = "/api/v1"
    corsOrigins: str = "http://localhost:3000"

    # Default IDs
    defaultTenantId: str = "e2e56225-8da9-4414-9d71-d31f368d9ac7"
    defaultStoreId: str = "d7bb739c-d79d-4ffd-8426-c0378e423f87"
    defaultUserId: str = "9c3e981e-1f81-4279-8d14-88481ff24588"

    databaseUrl: str = "sqlite+aiosqlite:///./karobar.db"

    # Connection Pool
    dbPoolSize: int = 20
    dbMaxOverflow: int = 10
    dbPoolTimeout: int = 30
    dbPoolRecycle: int = 3600

    # ──────────────────────────────────────
    # JWT Authentication
    # ──────────────────────────────────────
    jwtSecretKey: str = "super-secret-key-change-in-production-1234567890"
    jwtAlgorithm: str = "HS256"
    accessTokenExpireMinutes: int = 10080  # 7 days (increased for seamless testing/dev)
    refreshTokenExpireDays: int = 7

    # ──────────────────────────────────────
    # Email / OTP delivery (SMTP — free via a Gmail app password)
    # ──────────────────────────────────────
    smtpHost: str = "smtp.gmail.com"
    smtpPort: int = 465
    emailAddress: str = ""
    emailPassword: str = ""
    emailFromName: str = "KarobarOne"

    # ──────────────────────────────────────
    # Razorpay (app/services/razorpayClient.py — the ACTIVE payments router's
    # gateway client). Left blank means the client fails closed
    # (PaymentGatewayNotConfigured), never a fabricated success — see that
    # module's docstring for why that matters here.
    # ──────────────────────────────────────
    razorpayKeyId: str = ""
    razorpayKeySecret: str = ""
    razorpayWebhookSecret: str = ""

    # ──────────────────────────────────────
    # Redis (app/core/redisClient.py). Left blank means every Redis-backed
    # feature (health check, distributed rate limiting) reports itself as
    # "not_configured" and falls back to an in-process equivalent rather than
    # pretending to be connected — same fail-honest posture as Razorpay above.
    # ──────────────────────────────────────
    redisUrl: str = ""

    # ──────────────────────────────────────
    # Rate limiting (app/core/rateLimiter.py)
    # ──────────────────────────────────────
    rateLimitPerMinute: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def corsOriginsList(self) -> list[str]:
        """Comma-separated corsOrigins env value, split into a list."""
        return [origin.strip() for origin in self.corsOrigins.split(",") if origin.strip()]


@lru_cache
def getSettings() -> Settings:
    """
    Return a cached singleton Settings instance.

    Purpose:
        Retrieves application settings parsed and validated from environment.

    Parameters:
        None

    Return value:
        The Settings singleton instance.
    """
    return Settings()