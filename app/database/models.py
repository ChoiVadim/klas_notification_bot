from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

# Create base class for declarative models
Base = declarative_base()


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


class LibraryUser(Base):
    __tablename__ = "library_users"

    user_id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.encrypted_password,
            "phone_number": self.phone_number,
        }
