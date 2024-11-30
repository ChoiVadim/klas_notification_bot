from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

# Create base class for declarative models
Base = declarative_base()


# Define User model
class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.encrypted_password,
        }
