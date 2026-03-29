import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database.db import init_db
from routers import router
import time


app = FastAPI()

@app.middleware('http')
async def log_request(request: Request, call_next):
    start_time = time.time()
    responce = await call_next(request)
    process_time = time.time() - start_time
    print(f'{request.method} {request.url} - {responce.status_code} ({process_time:.2f}s)')
    return responce


@app.exception_handler(Exception)
async def gen_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={'detail': 'internal server error'})


@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app=app)