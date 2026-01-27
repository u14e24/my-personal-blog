import getpass

from sqlmodel import Session, SQLModel, select

from app.database import get_engine
from app.models.user import User, UserRole
from app.utils.security import hash_passwd 

# TODO: Add database backup script (e.g., daily copy to cloud storage like S3)

def main():
    engine = get_engine()  # create SQLAlchemy engine

    # Create all tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        username = input("Enter admin username: ")
        password = getpass.getpass("Enter admin password: ")

        existing_user = session.exec(select(User).where(User.username == username)).first()
        if existing_user:
            print(f"User '{username}' already exists.")
            return

        admin_user = User(
            username=username,
            hashed_password=hash_passwd(password),
            role=UserRole.admin 
        )

        session.add(admin_user)
        session.commit()
        session.refresh(admin_user)

        print(f"Admin user '{username}' created successfully with ID {admin_user.id}.")

if __name__ == "__main__":
    main()