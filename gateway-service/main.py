import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ARTICLE_SERVICE_URL = "http://article-service:8002"
AUTH_SERVICE_URL = "http://auth-service:8004/auth-service"
DISCUSSION_SERVICE_URL = "http://discussion-service:8003"
GRAPH_SERVICE_URL = "http://graph-service:8001/graph-service"

@app.api_route("/article-service/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy_to_article_service(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{ARTICLE_SERVICE_URL}/{path.lstrip('/')}",
            headers=dict(request.headers),
            content=await request.body(),
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )

@app.api_route("/auth-service/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy_to_auth_service(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{AUTH_SERVICE_URL}/{path.lstrip('/')}",
            headers=dict(request.headers),
            content=await request.body(),
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )

@app.api_route("/discussion-service/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy_to_discussion_service(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{DISCUSSION_SERVICE_URL}/{path.lstrip('/')}",
            headers=dict(request.headers),
            content=await request.body(),
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )

@app.api_route("/graph-service/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy_to_graph_service(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{GRAPH_SERVICE_URL}/{path.lstrip('/')}",
            headers=dict(request.headers),
            content=await request.body(),
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )