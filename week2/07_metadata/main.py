from fastapi import FastAPI

description = """
FastAPIStudyApp에서 만든 예시용 API. 🚀

## Items

아이템 목록: **read items**

## Users

만드는 중입니다

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="FastAPIStudyApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Hannal the dyed",
        "url": "http://hannal.example.com/contact/",
        "email": "dyed@hannal.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.get("/items/")
async def read_items():
    return [{"name": "Kay"}]
