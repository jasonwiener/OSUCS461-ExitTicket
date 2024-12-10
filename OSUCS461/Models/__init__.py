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


# model two: post

class UserPost(BaseModel):
	uuid: str = '0'
	user_uuid: str
	post_9char: str
	test: str
	time_created: int


class ReadUser(User):
    uuid: str

    class Config(BasePydanticModel.Config):
        frozen = True  # makes the model immutable

class ReadUserPost(UserPost):
    uuid: str
    user_uuid: str
    post_9char: str
    test: str
    time_created: int

    class Config(BasePydanticModel.Config):
        frozen = True