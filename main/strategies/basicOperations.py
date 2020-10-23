from enum import Enum, auto

class BasicOperation(Enum):
    """
    The basic operations are the ones that could be banned the account.
    These are like, follow and unfllow.
    """
    LIKE = auto()
    FOLLOW = auto()
    UNFOLLOW = auto()
    COMMENT = auto()