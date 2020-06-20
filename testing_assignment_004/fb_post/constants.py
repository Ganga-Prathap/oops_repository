from enum import Enum
from django.db.models import *
class ReactionEnum(Enum):
    WOW  = 'WOW'
    LIT = 'LIT'
    LOVE = 'LOVE'
    HAHA = 'HAHA'
    THUMBSUP = 'THUMBS-UP'
    THUMBSDOWN = 'THUMBS-DOWN'
    ANGRY = 'ANGRY'
    SAD = 'SAD'