from typing import Optional

class State:
    id: Optional[int] = None

    def __init__(self, account_id: Optional[int] = None, balance: Optional[float] = None):
        self.account_id = account_id
        self.balance = balance

    def validate(self) -> bool:
        return True
    