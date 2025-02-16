import os
import sys
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the root directory of your project
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

from core.services.logger_service import LoggerService
from web.admin_models.user import User
from core.services.postgres_db_connect import get_db_cursor  # Replace with your actual SQLAlchemy User model

def create_user(name: str,
                username: str,
                password: str,
                email: str,
                role: str = "USER") -> None:
    """
    Create a new user in the database using the DatabaseConnection service.

    Args:
        username (str): Username of the user.
        password (str): Plain-text password of the user.
        email (str): Email address of the user.
        role (str): Role of the user. Default is "USER".
    """
    logger_service = LoggerService()

    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # SQL query to insert the user
        query = """
        INSERT INTO "user" (name, login, password, email, role)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        params = (name, username, hashed_password, email, role)

        # Execute the query using DatabaseConnection
        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            user_id = cursor.fetchone()["id"]

        logger_service.log(f"User '{username}' created successfully with ID: {user_id}.")
        print(f"User '{username}' created successfully with ID: {user_id}.")

    except Exception as e:
        logger_service.error(f"Error creating user: {e}")
        print(f"Error creating user: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python create_user_service.py <username> <password> <email> [role]")
        sys.exit(1)

    name = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    email = sys.argv[4]
    role = sys.argv[5] if len(sys.argv) > 4 else "USER"

    create_user(name, username, password, email, role)
