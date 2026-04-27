import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent import MusicCuratorAgent


logger = logging.getLogger(__name__)

app = FastAPI(title="VibeMatch AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendRequest(BaseModel):
    prompt: str
    k: int = 5


agent = MusicCuratorAgent()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend(request: RecommendRequest):
    try:
        return agent.run(request.prompt, k=request.k)
    except ValueError as error:
        logger.warning("Invalid recommend request: %s", error)
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        logger.exception("Unexpected recommendation failure")
        raise HTTPException(status_code=500, detail="Internal recommendation error.") from error
