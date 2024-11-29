import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from src.task_tracker.router import router as tasks_router
from src.auth.router import router as auth_router

app = FastAPI()

app.include_router(tasks_router)
app.include_router(auth_router)

from fastapi.testclient import TestClient


# @app.get("/")
# async def root():
#     return {"message": "Tomato"}
#
#
# @pytest.mark.asyncio
# async def test_root():
#     async with AsyncClient(
#             transport=ASGITransport(app=app),
#             base_url="http://test"
#     ) as client:
#
#         response = await client.get("/")
#     import pdb;pdb.set_trace()
#     assert response.status_code == 200
#     assert response.json() == {"message": "Tomato"}
