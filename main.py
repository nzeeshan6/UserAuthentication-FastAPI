from fastapi import FastAPI
# import uvicorn
from fastapi.staticfiles import StaticFiles
from routes import user
# from database import model
# from database.db_connect import user_engine


app = FastAPI()
app.mount("/public", StaticFiles(directory="html-pages/public"), name="static")
app.include_router(user.router)

# model.Base.metadata.create_all(user_engine)

# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=3000)

