from fastapi import APIRouter, HTTPException
from typing import List
from Classes.Database import UserLogic, PostLogic
from Models import ReadUser, ReadUserPost, CreateUserRequest, CreatePostRequest, PreviewUserPost

router = APIRouter()

# Route: Get all users
@router.get("/users/", tags=["users"], response_model=List[ReadUser])
async def get_all_users():
    try:
        users = UserLogic.get_all_users()
        if not users:
            raise HTTPException(status_code=404, detail="No users found.")
        return users
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users/", tags=["users"], response_model=ReadUser)
async def create_user(user: CreateUserRequest):
    try:
        created_user = UserLogic.create(user.email)
        if not created_user:
            raise HTTPException(status_code=404, detail="User could not be retrieved after creation.")
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Get a user by UUID
@router.get("/users/{user_uuid}", tags=["users"], response_model=ReadUser)
async def get_user(user_uuid: str):
    try:
        user = UserLogic.get_by_uuid(user_uuid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Update a user by UUID
@router.put("/users/{user_uuid}", tags=["users"], response_model=ReadUser)
async def update_user(user_uuid: str, nuser: dict):
    try:
        user = UserLogic.get_by_uuid(user_uuid)
        # only name can be edited
        try:
            if "name" in nuser:
                name = nuser["name"]
            elif "email" in nuser:
                name = nuser["email"]
            else:
                name = user.name
        except Exception as e:
            name=user.name
        updated_user = ReadUser(uuid=user.uuid, name=name, time_created=user.time_created)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found for update.")
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Delete a user by UUID
@router.delete("/users/{user_uuid}", tags=["users"])
async def delete_user(user_uuid: str):
    try:
        deleted = UserLogic.delete(user_uuid)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found for deletion.")
        return {"message": "User deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e))


# TEXT POSTS =========================


# Route: Get all posts
@router.get("/posts/", tags=["posts"], response_model=List[PreviewUserPost])
async def get_all_posts():
    try:
        posts = PostLogic.get_all()
        if not posts or posts == []:
            raise HTTPException(status_code=404, detail="No posts found")
        return posts
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Route: Get all posts for a user
@router.get("/users/{user_uuid}/posts", tags=["posts"], response_model=List[PreviewUserPost])
async def get_user_posts(user_uuid: str):
    try:
        posts = PostLogic.get_by_user(user_uuid)
        if not posts or posts == []:
            raise HTTPException(status_code=404, detail="No posts found for this user.")
        return posts
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Route: Get post by UUID
@router.get("/posts/{post_uuid}", tags=["posts"], response_model=ReadUserPost)
async def get_post(post_uuid: str):
    try:
        post = PostLogic.get_by_uuid(post_uuid)
        if not post:
            raise HTTPException(status_code=404, detail="No post found.")
        return post
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Create a post for a user
@router.post("/users/{user_uuid}/posts", tags=["posts"], response_model=ReadUserPost)
async def create_post(post: CreatePostRequest):
    try:
        created_post = PostLogic.create(post.text, post.user_uuid)
        if not created_post:
            raise HTTPException(status_code=404, detail="Post could not be retrieved after creation.")
        return created_post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Update a post by UUID
@router.put("/posts/{post_uuid}", tags=["posts"], response_model=ReadUserPost)
async def update_post(post_uuid: str, txt: dict):
    try:
        post = PostLogic.get_by_uuid(post_uuid)
        npost = ReadUserPost(uuid=post.uuid, user_uuid=post.user_uuid, post_9char=txt['text'][:9], text=txt['text'], time_created=post.time_created)
        updated_post = PostLogic.save(npost)
        return updated_post
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Delete a post by UUID
@router.delete("/posts/{post_uuid}", tags=["posts"])
async def delete_user(post_uuid: str):
    try:
        deleted = PostLogic.delete(post_uuid)
        if not deleted:
            raise HTTPException(status_code=404, detail="Post not found for deletion.")
        return {"message": "Post deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e))