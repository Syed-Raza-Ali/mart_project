from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, Field, SQLModel,create_engine, select
from app.settings import DATABASE_URL

# create a user base  class for store user data in database 
class UserBase(SQLModel):
    user_name : str
    user_address : str
    user_email : str
    user_password : str



# create a user class for generate id automatically 
class User(UserBase, table=True):
    user_id: Optional[int] = Field(default=None, primary_key = True)


# create a user update class for update user
class UserUpdateModel(SQLModel):
    user_name : str
    user_address : str
    user_password : str

 
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


# Dependency inection to get a session
DB_Session = Annotated[Session, Depends(get_session)]


# add FastAPI to create routes
app = FastAPI(lifespan= create_db_and_tables) 


@app.get('/')
def root_route():
    return {"Hello": "From Server"}



# add user in database 
def add_user_into_db(form_data : UserBase, session : Session):
    user_info = User(**form_data.dict())
    # Add user to database
    session.add(user_info)
    # Commit the changes to the database
    session.commit()
    # Refresh the user object to get the id, this is needed for the next commit operation
    session.refresh(user_info)
    # print statement for debugging purposes
    print("new user..", user_info)

    return user_info

# post route to add the new user in to database
@app.post('/api/add_user')
def get_user(new_user: UserBase ,session : DB_Session):
    add_user = add_user_into_db(new_user, session)
    return add_user


# function to retreive data from database
def get_user_from_db(session : DB_Session):
    statement = select(User)
    user_list = session.exec(statement).all()
    if not user_list:
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        return user_list
    
# api get user
@app.get('/api/get_user')
def get_user(session: DB_Session):
    users = get_user_from_db(session)
    return users


def update_user_from_db(selected_id: int, form_data:UserUpdateModel, session: DB_Session):
    statement = select(User).where(User.user_id == selected_id)
    selected_user = session.exec(statement).first()
    if not selected_user:
        raise HTTPException(status_code=404, detail="User not Found")
    # from database         = from form data
    selected_user.user_name = form_data.user_name
    selected_user.user_address = form_data.user_address
    selected_user.user_password = form_data.user_password

    session.add(selected_user)
    session.commit()
    session.refresh(selected_user)
    return selected_user

@app.put('/api/update_user')
def update_user(id:int, user_details: UserUpdateModel, session: DB_Session):
    user = update_user_from_db(id, user_details, session)
    return user