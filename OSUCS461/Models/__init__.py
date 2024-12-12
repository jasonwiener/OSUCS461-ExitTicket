from pydantic import BaseModel

class BasePydanticModel(BaseModel):
	class Config:
		from_attributes = False
		validate_assignment = True

# model one: user

class User(BaseModel):
	uuid: str = '0'
	name: str
	time_created: int


class ReadUser(User):
    uuid: str
    name: str
    time_created: int

    class Config(BasePydanticModel.Config):
        frozen = True  # makes the model immutable

# model two: post

class UserPost(BaseModel):
	uuid: str = '0'
	user_uuid: str
	post_9char: str
	text: str
	time_created: int

# creation
class CreateUserRequest(BaseModel):
    email: str
    

class CreatePostRequest(BaseModel):
    text: str
    user_uuid: str

class ReadUserPost(UserPost):
    uuid: str
    user_uuid: str
    post_9char: str
    text: str
    time_created: int

    class Config(BasePydanticModel.Config):
        frozen = True

class PreviewUserPost(BaseModel):
    uuid: str
    post_9char: str
    time_created: int