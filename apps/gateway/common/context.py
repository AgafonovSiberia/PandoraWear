from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UserContext:
    user_id: int
