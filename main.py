import uvicorn
from fastapi import FastAPI
from database.db import init_db
from routers import router


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app=app)