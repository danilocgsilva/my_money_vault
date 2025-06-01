from typing import Optional

class State:
    id: Optional[int] = None

    def validate(self) -> bool:
        return True