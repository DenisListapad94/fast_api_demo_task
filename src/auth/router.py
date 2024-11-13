from fastapi import  APIRouter


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get(
    "",
    description="test auth endpoint",
)
def read_root_auth(
):
    return {
        "Hello": "World",
    }
