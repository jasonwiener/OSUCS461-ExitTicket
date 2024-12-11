import hashlib
from typing import List
from OSUCS461.Config import MySQL as DatabaseConfig
from OSUCS461.ThirdParty.MySQL import MySQL
from Models import User, UserPost, ReadUser, ReadUserPost  # Adjust path as needed
DB = MySQL(**DatabaseConfig)

class UserLogic:
    @staticmethod
        
    def get_all_users() -> List[ReadUser]:
        """Fetch all users from the database."""
        query = "SELECT uuid, name, time_created FROM user"  # Ensure the table name is correct
        results = DB.query(query)
        if results is True or not results:
            return []
        return [ReadUser(uuid=row[0], name=row[1], time_created=row[2]) for row in results]

    @staticmethod
    def get_by_uuid(uuid: str) -> ReadUser:
        """Fetch a user by UUID."""
        query = f"SELECT uuid, name, time_created FROM user WHERE uuid = '{uuid}'"
        print('executing q:', query)
        result = DB.query(query)
        if not result:
            raise ValueError(f"User with UUID {uuid} not found.")
        return ReadUser(uuid=result[0][0], name=result[0][1], time_created=result[0][2])

    @staticmethod
    def create(name: str) -> ReadUser:
        """
        Create a new user with a unique UUID.
        The UUID is generated using an SHA224 hash of the name and the current timestamp.
        """
        import time
        timestamp = str(time.time())
        raw_uuid = f"{name}-{timestamp}"
        uuid = hashlib.sha224(raw_uuid.encode('utf-8')).hexdigest()

        query = f"INSERT INTO user (uuid, name, time_created) VALUES ('{uuid}', '{name}', '{timestamp}')"
        DB.query(query)
        
        return UserLogic.get_by_uuid(uuid)

    @staticmethod
    def save(user: User) -> str:
        """Insert or update the user in the database."""
        if user.uuid == "0":
            import time
            timestamp = str(time.time())
            # Insert a new user
            query = f"INSERT INTO user (name, time_created) VALUES ('{user.name}', '{timestamp}')"
            user_id = DB.insert(query)
            return user_id
        else:
            # Update an existing user
            query = f"UPDATE user SET name = {user.name} WHERE uuid = {user.uuid}"
            DB.query(query)
            return user.uuid

    @staticmethod
    def delete(uuid: str):
        """Delete a user by UUID."""
        query = f"DELETE FROM user WHERE uuid = {uuid}"
        DB.query(query)

class PostLogic:
    @staticmethod
    def get_by_uuid(uuid: str) -> ReadUserPost:
        """Fetch a post by UUID from the database."""
        query = f"SELECT uuid, user_uuid, post_9char, test, time_created FROM user_post WHERE uuid = '{uuid}'"
        result = DB.query(query)
        if not result:
            raise ValueError(f"Post with UUID {uuid} not found.")
        return ReadUserPost(
            uuid=result[0][0],
            user_uuid=result[0][1],
            post_9char=result[0][2],
            test=result[0][3],
            time_created=result[0][4],
        )

    @staticmethod
    def save(post: UserPost) -> str:
        """Insert or update the post in the database."""
        if post.uuid == "0":
            # Insert a new post
            query = f"INSERT INTO user_post (user_uuid, post_9char, test, time_created) VALUES ('{post.user_uuid}', '{post.post_9char}', '{post.test}', '{post.time_created}')"
            post_id = DB.insert(query)
            return post_id
        else:
            # Update an existing post
            query = f"UPDATE user_post SET user_uuid = {post.user_uuid}, post_9char = {post.post_9char}, test = {post.test}, time_created = {post.time_created} WHERE uuid = {post.uuid}"
            DB.query(query)
            return post.uuid

    @staticmethod
    def delete(uuid: str):
        """Delete a post by UUID."""
        query = f"DELETE FROM user_post WHERE uuid = {uuid}"
        DB.query(query)
