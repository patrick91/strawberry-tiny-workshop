import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)
