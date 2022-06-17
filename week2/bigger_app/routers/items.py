'''
다음과 같은 path를 추가하고 싶음. (users.py랑 거의 비슷)
    /items/
    /items/{item_id}

하지만,
- /items/ 부분이 공통이니까 DRY해보자
- 모든 items 엔드포인트에 tags=items를 중복 없이 넣어보자
- 모든 items 엔드포인트에 추가 response
- 모든 items 엔드포인트에 의존성 주입(방금 만든 X-Token)
'''
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header


# 의존성(get_token_header 부분)에는 인자를 넘기지 않습니다
router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db


# path는 `/`로 시작해야 합니다
# path 끝에는 `/`를 붙이지 않습니다.
@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],  # 기존 태그인 items에 custom도 추가됨. 즉, tags=["items", "custom"]
    responses={403: {"desription": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}


# 의존성 뿐 아니라 Security 관련 의존성도 넣을 수 있겠지요.