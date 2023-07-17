from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.api.schema import schema


graphql_app = GraphQLRouter[None, None](schema)


app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
