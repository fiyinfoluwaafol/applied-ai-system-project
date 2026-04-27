from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent import MusicCuratorAgent


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
        raise HTTPException(status_code=400, detail=str(error)) from error
