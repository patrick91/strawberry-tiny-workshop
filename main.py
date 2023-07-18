from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.api.schema import schema
from app.api.fake_db import Db


def context_getter():
    db = Db()

    return {"db": db, "user": None}


graphql_app = GraphQLRouter[None, None](schema, context_getter=context_getter)


app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
