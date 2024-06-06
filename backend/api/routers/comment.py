from fastapi import APIRouter

from api.schemes.comment import CreateComment

router = APIRouter()

@router.get("/comment/{post_id}")
async def get_comments(post_id: int):
    pass

@router.post("/comment/{post_id}")
async def post_comment(post_id: int, commet_body: CreateComment):
    pass

@router.delete("/comment/{comment_id}")
async def delete_comment(comment_id: int):
    pass