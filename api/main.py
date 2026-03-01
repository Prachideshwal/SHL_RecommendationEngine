from fastapi import FastAPI
from pydantic import BaseModel
from retriever.recommender import recommend
import os

app = FastAPI(
    title="SHL Assessment Recommendation Engine",
    version="1.0"
)


class RequestModel(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "SHL Recommendation Engine Running"}


@app.post("/recommend")
def recommend_api(request: RequestModel):

    results = recommend(request.query, top_k=5)

    return {
        "input_query": request.query,
        "recommendations": results
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api.main:app", host="0.0.0.0", port=port)