import uvicorn
from fastapi import FastAPI
from settings import settings

app = FastAPI()
app.include_router(app.router)

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        use_colors=True,
    )
