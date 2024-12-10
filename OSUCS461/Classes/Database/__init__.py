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
        query = "SELECT uuid, name, time_created FROM users"  # Ensure the table name is correct
        results = DB.query(query)

        if not results:  # Check if the result is None or an empty list
            return []

        return [ReadUser(uuid=row[0], name=row[1], time_created=row[2]) for row in results]

    @staticmethod
    def get_by_uuid(uuid: str) -> ReadUser:
        """Fetch a user by UUID."""
        query = "SELECT uuid, name, time_created FROM user WHERE uuid = %s"
        result = DB.query(query, (uuid,))
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

        query = "INSERT INTO user (uuid, name, time_created) VALUES (%s, %s, NOW())"
        DB.execute(query, (uuid, name))
        
        return UserLogic.get_by_uuid(uuid)

    @staticmethod
    def save(user: User) -> str:
        """Insert or update the user in the database."""
        if user.uuid == "0":
            # Insert a new user
            query = "INSERT INTO user (name, time_created) VALUES (%s, NOW())"
            user_id = DB.insert(query, (user.name,))
            return user_id
        else:
            # Update an existing user
            query = "UPDATE user SET name = %s WHERE uuid = %s"
            DB.execute(query, (user.name, user.uuid))
            return user.uuid

    @staticmethod
    def delete(uuid: str):
        """Delete a user by UUID."""
        query = "DELETE FROM user WHERE uuid = %s"
        DB.execute(query, (uuid,))

class PostLogic:
    @staticmethod
    def get_by_uuid(uuid: str) -> ReadUserPost:
        """Fetch a post by UUID from the database."""
        query = "SELECT uuid, user_uuid, post_9char, test, time_created FROM user_post WHERE uuid = %s"
        result = DB.query(query, (uuid,))
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
            query = "INSERT INTO user_post (user_uuid, post_9char, test, time_created) VALUES (%s, %s, %s, %s)"
            post_id = DB.insert(query, (post.user_uuid, post.post_9char, post.test, post.time_created))
            return post_id
        else:
            # Update an existing post
            query = "UPDATE user_post SET user_uuid = %s, post_9char = %s, test = %s, time_created = %s WHERE uuid = %s"
            DB.execute(query, (post.user_uuid, post.post_9char, post.test, post.time_created, post.uuid))
            return post.uuid

    @staticmethod
    def delete(uuid: str):
        """Delete a post by UUID."""
        query = "DELETE FROM user_post WHERE uuid = %s"
        DB.execute(query, (uuid,))
