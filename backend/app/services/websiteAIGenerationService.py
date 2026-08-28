import uuid

from fastapi import HTTPException
from google import genai
from google.genai import types
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import getSettings
from app.core.exceptionsCompat import NotFoundError
from app.db.models.websiteAIContent import WebsiteAIContent
from app.db.models.store import Store
from app.repositories.websiteAIContentRepository import (
    WebsiteAIContentRepository,
)


ALLOWED_CONTENT_TYPES = {
    "ABOUT",
    "FAQ",
    "SEO",
    "PRIVACY",
    "BLOG",
}


class WebsiteAIGenerationService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = WebsiteAIContentRepository(session)
        self.settings = getSettings()

    async def _getStore(
        self,
        storeId: uuid.UUID,
    ) -> Store:

        from sqlalchemy import select

        result = await self.session.execute(
            select(Store).where(
                Store.id == storeId
            )
        )

        store = result.scalar_one_or_none()

        if not store:
            raise NotFoundError(
                "Store",
                str(storeId),
            )

        return store

    def _buildPrompt(
        self,
        contentType: str,
        store: Store,
        instructions: str | None = None,
    ) -> str:

        businessName = (
            getattr(store, "name", None)
            or getattr(store, "storeName", None)
            or "the business"
        )

        businessType = (
            getattr(store, "businessType", None)
            or "business"
        )

        base = f"""
You are generating website content for a business.

Business name: {businessName}
Business type: {businessType}

Write professional, clear, original website content.
Do not invent specific claims such as certifications,
awards, statistics, addresses, phone numbers, or guarantees
unless they are provided in the input.

"""

        prompts = {
            "ABOUT": """
Generate an About Us section.
Include:
- who the business is
- what it offers
- its value proposition
- a professional closing
Keep it suitable for a business website.
""",
            "FAQ": """
Generate useful frequently asked questions and answers
for this business.
Return 6-10 practical FAQs.
""",
            "SEO": """
Generate SEO metadata for the business website.
Return:
- meta title
- meta description
- keywords
- suggested page title
""",
            "PRIVACY": """
Generate a website Privacy Policy draft.
Keep it clearly marked as a draft/template and avoid
claiming legal compliance with a specific jurisdiction.
""",
            "BLOG": """
Generate one useful business blog post.
Include:
- title
- short introduction
- 3-5 sections
- conclusion
- SEO-friendly meta description
""",
        }

        prompt = base + prompts[contentType]

        if instructions:
            prompt += f"""

Additional instructions:
{instructions}
"""

        return prompt

    async def generate(
        self,
        storeId: uuid.UUID,
        contentType: str,
        instructions: str | None = None,
    ) -> WebsiteAIContent:

        contentType = contentType.upper().strip()

        if contentType not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_CONTENT_TYPE",
                    "message": (
                        f"Unsupported content type "
                        f"'{contentType}'. "
                        f"Allowed types: "
                        f"{sorted(ALLOWED_CONTENT_TYPES)}"
                    ),
                },
            )

        store = await self._getStore(storeId)

        apiKey = self.settings.geminiApiKey

        if not apiKey:
            raise HTTPException(
                status_code=503,
                detail={
                    "code": "AI_NOT_CONFIGURED",
                    "message": (
                        "Gemini AI is not configured. "
                        "Set GEMINI_API_KEY in the environment."
                    ),
                },
            )

        prompt = self._buildPrompt(
            contentType,
            store,
            instructions,
        )

        try:
            client = genai.Client(
                api_key=apiKey
            )

            response = await client.aio.models.generate_content(
                model=self.settings.geminiModel,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                ),
            )

            generatedText = (
                response.text
                if response.text
                else None
            )

            if not generatedText:
                raise HTTPException(
                    status_code=502,
                    detail={
                        "code": "AI_EMPTY_RESPONSE",
                        "message": (
                            "AI provider returned "
                            "an empty response."
                        ),
                    },
                )

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail={
                    "code": "AI_PROVIDER_ERROR",
                    "message": (
                        "AI provider request failed."
                    ),
                    "error": str(exc),
                },
            ) from exc

        content = WebsiteAIContent(
            storeId=storeId,
            contentType=contentType,
            content=generatedText,
            contentMetadata={
                "provider": self.settings.aiProvider,
                "model": self.settings.geminiModel,
            },
            status="GENERATED",
        )

        result = await self.repo.create(
            content
        )

        await self.session.commit()
        await self.session.refresh(result)

        return result
