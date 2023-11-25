import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute

from scheduler import scheduler


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}" if len(route.tags) else f"unmarked-{route.name}"


app = FastAPI(
    generate_unique_id_function=custom_generate_unique_id,
    on_startup=[
        scheduler.start
    ],
    on_shutdown=[
        scheduler.shutdown
    ]
)


from src.routes import users

app.include_router(router=users.router)


if __name__ == "__main__":
    uvicorn.run(app, port=8010, host="0.0.0.0")