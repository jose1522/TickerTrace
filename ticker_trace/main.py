from fastapi import FastAPI

import settings
from endpoints.v1 import router as v1_router
from models import migrate
from utils.middleware import ExceptionMiddleware

app = FastAPI(debug=settings.DEBUG, title="Ticker Trace API", version="0.1.0")
app.include_router(v1_router)
app.add_middleware(ExceptionMiddleware)


@app.on_event("startup")
async def startup():
    migrate()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=5000, reload=True)
