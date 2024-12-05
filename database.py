from sqlalchemy import create_engine, Column, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    want = Column(Boolean, default=False)
    data = Column(String, default="To your notice")
    sent = Column(Boolean, default=False)


with engine.connect() as connection:
    print("Connected to the database!")

session = Session(engine)


def add_user(user_id, username, name):
    user = User(
        user_id=user_id,
        username=username,
        name=name,
    )

    session.add(user)
    session.commit()


def get_all_users():
    return session.query(User.user_id).where(User.sent == False).all()


def get_users_except(user_id):
    return (
        session.query(User)
        .filter((User.user_id != user_id) & (User.sent == False))
        .all()
    )


def update_sent(user_id):
    user = session.query(User).filter(User.user_id == user_id).first()

    user.sent = True

    session.commit()


def update_want(user_id):
    user = session.query(User).filter(User.user_id == user_id).first()

    if not user:
        return

    user.want = True

    session.commit()


def get_want(user_id):
    want = session.query(User.want).where(User.user_id == user_id).first()

    if not want:
        return False

    return want[0]


def update_data(user_id, data):
    user = session.query(User).where(User.user_id == user_id).first()

    if not user:
        return

    user.data = data
    user.want = False

    session.commit()
    return True
