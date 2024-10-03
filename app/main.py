from typing import Annotated, Optional
from fastapi import Depends, FastAPI
from sqlmodel import Session, Field, SQLModel,create_engine

from app.settings import DATABASE_URL
from app.user_model import User, UserBase



class UserBase(SQLModel):
    user_name : str
    user_address : str
    user_email : str
    user_password : str

class User(UserBase, table=True):
    user_id: Optional[int] = Field(default=None, primary_key = True)




 
# .replace() for replace postgresql to postgresql + psycopg for using psycopg in postgrsql
#connection string for connect data base 

connection_string = str(DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)



# pool_recycle=300 = reload after 300 seconds to update connection string
# Is engine ke through aap database ke saath kaam karte ho. Hum " connection_string " pass karte hain jo bataata hai ke kis database se connect karna hai.
# connect_args ek parameter hai jo humein database connection ke liye additional options dene ki sahoolat deta hai. Is code mein humne empty dictionary di hai, iska matlab hai koi extra argument nahi diya.



engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

# create_db_and_tables Ye function FastAPI ko argument ke tor pe accept karta hai, taake jab app chalaye to yeh function database ke tables create kar sake.
# SQLModel.metadata.create_all(engine) se SQLModel ka metadata (jo database ke tables ke structure ko define karta hai) ko use karke sab tables ko database mein create kiya jata hai.



async def create_db_and_tables(app: FastAPI):
    print(f"Creating tables...{app}") 
    SQLModel.metadata.create_all(engine)
    yield




# get_session() ek function hai jo database session ko return karta hai, aur with statement se ensure karta hai ke session close ho jaye jab kaam khatam ho jaye. yield se session ko FastAPI ko diya jata hai taake use kar sake.
def get_session():
    with Session(engine) as session:
        yield session



DB_Session = Annotated[Session, Depends(get_session)]






# add FastAPI to create routes
app = FastAPI(lifespan= create_db_and_tables) 


@app.get('/')
def root_route():
    return {"message": "Hello, FastAPI!"}

# add user in database 
def add_user_into_db(form_data : UserBase, session : Session):
    user_info = User(**form_data.dict())

    session.add(user_info)
    session.commit()
    session.refresh(user_info)
    print("new user..", user_info)

    return user_info

    # add_user = select(User)
    # user = session.exec(add_user)

@app.post('/api/add_user')
def get_user(new_user: UserBase ,session : DB_Session):
    add_user = add_user_into_db(new_user, session)
    return add_user
