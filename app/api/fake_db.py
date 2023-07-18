from typing import Dict, Optional, TypedDict, List


class Answer(TypedDict):
    id: int
    text: str
    votes: int


class Poll(TypedDict):
    id: int
    title: str
    answers: List[Answer]
    total_votes: int


POLLS: Dict[str, Poll] = {
    "1": {
        "id": 1,
        "title": "What's your favourite color?",
        "answers": [
            {"id": 1, "text": "Red", "votes": 15},
            {"id": 2, "text": "Blue", "votes": 7},
            {"id": 3, "text": "Green", "votes": 3},
        ],
        "total_votes": 25,
    },
}


class Db:
    def get_poll(self, id: str) -> Optional[Poll]:
        return POLLS.get(id)

    def update_poll(self, poll_id: str, answer_id: str) -> Optional[Poll]:
        poll = POLLS.get(poll_id)

        if poll is None:
            return None

        for answer in poll["answers"]:
            if answer["id"] == int(answer_id):
                answer["votes"] += 1
                poll["total_votes"] += 1
                break
        else:
            return None

        return poll
