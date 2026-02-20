import logging
import time
import logging
import uuid
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from orchestrator.graph import build_graph
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Modular Agentic Worker Framework",
    description="Multi-agent orchestration system with validation and retry logic.",
    version="1.0.0"
)

llm = ChatOllama(
    model="gemma3:4b",
    temperature=0.7,
)

graph = build_graph()

class TaskRequest(BaseModel):
    task: str

@app.middleware("http")
async def log_requests(request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    logging.info(f"Request ID:{request_id} started")
    response = await call_next(request)
    duration = round(time.time() - start_time, 3)
    logging.info(f"Request ID:{request_id} completed in {duration}s")
    response.headers["X-Request-ID"] = request_id
    return response

@app.post("/run")
def run_agent(request: TaskRequest):
    logging.info("New task received")
    result = graph.invoke({
        "task": request.task,
        'retry_count': 0
    })
    return result

@app.get("/stream")
async def stream(prompt: str):
    async def generator():
        async for chunk in llm.astream(
            [HumanMessage(content=prompt)]
        ):
            yield chunk.content

    return StreamingResponse(generator(), media_type="text/plain")

@app.get("/health")
def health():
    return {"status": "ok"}


