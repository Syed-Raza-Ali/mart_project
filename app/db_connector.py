# from fastapi import Depends
# from sqlmodel import SQLModel, Session, create_engine
# from typing import Annotated

# from app.settings import DATABASE_URL

# # .replace() for replace postgresql to postgresql + psycopg for using psycopg in postgrsql
# #connection string for connect data base 

# connection_string = str(DATABASE_URL).replace(
#     "postgresql", "postgresql+psycopg"
# )



# # pool_recycle=300 = reload after 300 seconds to update connection string
# # Is engine ke through aap database ke saath kaam karte ho. Hum " connection_string " pass karte hain jo bataata hai ke kis database se connect karna hai.
# # connect_args ek parameter hai jo humein database connection ke liye additional options dene ki sahoolat deta hai. Is code mein humne empty dictionary di hai, iska matlab hai koi extra argument nahi diya.



# engine = create_engine(
#     connection_string, connect_args={}, pool_recycle=300
# )

# # create_db_and_tables Ye function FastAPI ko argument ke tor pe accept karta hai, taake jab app chalaye to yeh function database ke tables create kar sake.
# # SQLModel.metadata.create_all(engine) se SQLModel ka metadata (jo database ke tables ke structure ko define karta hai) ko use karke sab tables ko database mein create kiya jata hai.



# def create_db_and_tables()->None:
#     print("Creating tables...") 
#     SQLModel.metadata.create_all(engine)




# # get_session() ek function hai jo database session ko return karta hai, aur with statement se ensure karta hai ke session close ho jaye jab kaam khatam ho jaye. yield se session ko FastAPI ko diya jata hai taake use kar sake.
# def get_session():
#     with Session(engine) as session:
#         yield session


# DB_Session = Annotated[Session, Depends(get_session)]