import strawberry

from typing import List, Optional

from strawberry.types import Info


@strawberry.type
class Answer:
    id: strawberry.ID
    text: str
    votes: int


@strawberry.type
class Poll:
    id: strawberry.ID
    question: str
    answers: List[Answer]
    total_votes: int

    @classmethod
    def from_dict(cls, poll) -> "Poll":  # type: ignore
        return cls(
            question=poll["title"],
            id=strawberry.ID(str(poll["id"])),
            total_votes=poll["total_votes"],
            answers=[
                Answer(
                    id=strawberry.ID(str(answer["id"])),
                    text=answer["text"],
                    votes=answer["votes"],
                )
                for answer in poll["answers"]
            ],
        )


# query {
#   poll(id:"1") {
#     id
#   }
# }


@strawberry.type
class Query:
    @strawberry.field
    def poll(self, id: strawberry.ID, info: Info) -> Optional[Poll]:
        db = info.context["db"]

        poll = db.get_poll(id)

        if poll is None:
            return None

        return Poll.from_dict(poll)


# query {
#   vote(pollId:"1", answerId: "2") {
#     id
#   }
# }


@strawberry.type
class Mutation:
    @strawberry.mutation
    def vote(
        self, info: Info, pollId: strawberry.ID, answerId: strawberry.ID
    ) -> Optional[Poll]:
        db = info.context["db"]

        poll = db.update_poll(pollId, answerId)

        if poll is None:
            return None

        return Poll.from_dict(poll)


schema = strawberry.Schema(query=Query, mutation=Mutation)
