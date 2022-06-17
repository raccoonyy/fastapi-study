from fastapi import FastAPI

app = FastAPI(
    openapi_url="/api/v1/openapi.json",  # None도 가능합니다
    docs_url="/documentation",
    redoc_url=None,
)


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
