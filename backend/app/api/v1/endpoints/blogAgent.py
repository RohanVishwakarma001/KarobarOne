# Owner: mousamdas156@gmail.com
from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
# from app.apps.blogAgent.bwaBackend import run as run_blogAgent

router = APIRouter(prefix="/blog-agent", tags=["Blog Writer AI Agent"])

class BlogGenerationRequest(BaseModel):
    topic: str
    as_of: Optional[str] = None
    tenantId: Optional[str] = None

@router.post("/generate")
async def generate_blog(request: BlogGenerationRequest):
    if request.tenantId:
        import uuid
        from app.db.session import getSessionFactory
        from app.core.planGuard import PlanGuard
        async with getSessionFactory()() as session:
            guard = PlanGuard(session)
            await guard.check_feature_access(uuid.UUID(request.tenantId), "blog")

    try:
        from app.apps.blogAgent.bwaBackend import run as run_blogAgent
        result = run_blogAgent(request.topic, request.as_of)
        
        plan_data = None
        if result.get("plan"):
            plan_data = result["plan"].model_dump()

        return {
            "status": "success",
            "topic": result.get("topic"),
            "mode": result.get("mode"),
            "plan": plan_data,
            "final_markdown": result.get("final"),
            "image_specs": result.get("image_specs", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Agent run failed: {str(e)}")
