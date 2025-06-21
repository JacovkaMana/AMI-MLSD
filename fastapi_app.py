from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import run
import uvicorn

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/generate")
async def generate_adventure(request: QueryRequest):
    try:
        result = run(request.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
