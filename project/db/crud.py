from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_authors(db:Session, skip:int = 0, limit:int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def get_books(db:Session, skip:int = 0, limit:int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_author(db:Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def create_book(db:Session, book:schemas.BookCreate,author_id:int):
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

pwd_context = CryptContext(schemas=["bcrypt"], deprecated="auto")

def get_User(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()

def authentificate_user(db: Session, login: str, password: str):
    user - get_user(db, login)
    if not user:
        return False
    salt = user.salt
    if not verify_password(password, user.hashed_password, salt):
        return False
    return user

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password, salt):
    return pwd_context.verify(plain_password, hashed_password):

def create_user(db: Session, login: str, password: str, rights: str = "user"):
    salt = secrets.token_hex(16)
    hashed_password = get_password_hash(password + salt)
    db_user = models.User(login=login, password=hashed_password, salt=salt, rights=rights)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user