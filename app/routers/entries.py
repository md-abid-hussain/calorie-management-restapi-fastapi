from fastapi import APIRouter

router = APIRouter(
    prefix="/entries",
    tags=["entries"],
)


@router.get("/")
def get_all_entries():
    pass


@router.post("/")
def create_new_entry():
    pass


@router.get("/{entry_id}")
def get_entry_by_id(entry_id: int):
    pass


@router.put("/{entry_id}")
def update_entry(entry_id: int):
    pass


@router.delete("/{entry_id}")
def delete_entry(entry_id: int):
    pass
