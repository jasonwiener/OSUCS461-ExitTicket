from fastapi import APIRouter, HTTPException
from typing import List
from Classes.Database import UserLogic, PostLogic
from Models import User, UserPost, ReadUser, ReadUserPost

router = APIRouter()


# Route: Get all users
@router.get("/users/", tags=["users"], response_model=List[ReadUser])
async def read_users():
    try:
        users = UserLogic.get_all_users()
        if not users:  # Check if users is an empty list
            raise HTTPException(status_code=404, detail="No users found.")
        return users
    except Exception as e:
        if e.status_code and e.status_code == 404:
            raise HTTPException(status_code=404, detail="No users found.")
        else:
            raise HTTPException(status_code=500, detail=str(e))


# Route: Create a new user
@router.post("/users/", tags=["users"], response_model=ReadUser)
async def create_user(user: User):
    try:
        user_id = UserLogic.save(user)
        created_user = UserLogic.get_by_uuid(user_id)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route: Get a user by UUID
@router.get("/users/{user_uuid}", tags=["users"], response_model=ReadUser)
async def get_user(user_uuid: str):
    try:
        user = UserLogic.get_by_uuid(user_uuid)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route: Delete a user by UUID
@router.delete("/users/{user_uuid}", tags=["users"])
async def delete_user(user_uuid: str):
    try:
        UserLogic.delete(user_uuid)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route: Get all posts for a user
@router.get("/users/{user_uuid}/posts", tags=["posts"], response_model=List[ReadUserPost])
async def get_user_posts(user_uuid: str):
    try:
        posts = PostLogic.get_posts_by_user_uuid(user_uuid)  # Assumes a `get_posts_by_user_uuid` method in `PostLogic`
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route: Create a post for a user
@router.post("/users/{user_uuid}/posts", tags=["posts"], response_model=ReadUserPost)
async def create_post(user_uuid: str, post: UserPost):
    try:
        post.user_uuid = user_uuid  # Ensure the user_uuid is assigned
        post_id = PostLogic.save(post)
        created_post = PostLogic.get_by_uuid(post_id)
        return created_post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
