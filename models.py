from dataclasses import dataclass


@dataclass
class News:
    id: str
    title: str
    link: str
    source: str
    score: int = 0
    reason: str = ""
    article: str = ""