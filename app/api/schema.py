import strawberry

from typing import List, Optional

from typing_extensions import Annotated


from strawberry.types import Info
from strawberry.arguments import UNSET


@strawberry.type
class Answer:
    id: strawberry.ID
    text: str
    votes: int


@strawberry.type(name="Poll")
class PollType:
    id: strawberry.ID
    question: str
    total_votes: int
    answers: List[Answer]
    old_votes: Optional[int] = strawberry.field(
        deprecation_reason="use total_votes", default=1
    )

    @strawberry.field
    def old_votes2(self) -> int:
        breakpoint()
        return self.total_votes

    @classmethod
    def from_dict(cls, poll) -> "PollType":  # type: ignore
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
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    count: int


@strawberry.type
class PollsPage:
    items: List[PollType]
    page_info: PageInfo


@strawberry.type
class Query:
    @strawberry.field
    async def poll(self, id: strawberry.ID, info: Info) -> Optional[PollType]:
        db = info.context["db"]

        poll = db.get_poll(id)

        if poll is None:
            return None

        return PollType.from_dict(poll)

    @strawberry.field
    def polls(self, info: Info, page: int, per_page: int) -> PollsPage:
        assert page > 0
        assert per_page > 0
        assert per_page <= 50

        db = info.context["db"]

        polls = db.list_polls(page=1)

        return PollsPage(
            items=[PollType.from_dict(poll) for poll in polls],
            page_info=PageInfo(
                has_next_page=False,
                has_previous_page=False,
                count=len(polls),
            ),
        )


# query {
#   vote(pollId:"1", answerId: "2") {
#     id
#   }
# }


@strawberry.type
class Mutation:
    @strawberry.mutation
    def vote(
        self,
        info: Info,
        pollId: strawberry.ID,
        answerId: strawberry.ID,
        def_: Annotated[
            int,
            strawberry.argument(
                name="def",
                description="this is a def",
            ),
        ] = UNSET,
    ) -> Optional[PollType]:
        db = info.context["db"]

        poll = db.update_poll(pollId, answerId)

        if poll is None:
            return None

        return PollType.from_dict(poll)

    @strawberry.mutation
    def delete_poll(self, info: Info, id: strawberry.ID) -> None:
        db = info.context["db"]

        db.delete_poll(id)


schema = strawberry.Schema(query=Query, mutation=Mutation)
