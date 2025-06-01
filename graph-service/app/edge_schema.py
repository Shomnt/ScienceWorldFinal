from pydantic import BaseModel


class EdgeGetIn(BaseModel):
    user_area_list: list[str]
    article_area_list: list[str]
    user_rating: float

class EdgeGetOut(BaseModel):
    addition_rating: float
