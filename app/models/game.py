from typing import Optional
from sqlmodel import SQLModel, Field


class Game(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    chess_variant_id: int = Field(nullable=False)
    position: int
    while_user_id: int = Field(nullable=False)
    black_user_id: int = Field(nullable=False)
    status_id: int = Field(nullable=False)
    moves: str


class Game_Chess_Variant(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    chess_variant: str

    #  = [
    #     (1, 'Инь-Ян'),
    #     (2, 'Фланговая'),
    #     (3, 'Инь-ян / Фланговая'),
    #     (4, 'Инь-ян / Фибоначчи'),
    #     (15, 'Классические'),
    #     (16, 'Фишера'),
    # ]


class Game_Status(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    status: str

    # status = [
    #     (0, 'Ход белых'),
    #     (1, 'Ход черных'),
    #     (2, 'Белые победили'),
    #     (3, 'Чёрные победили'),
    #     (4, 'Белые сдались'),
    #     (5, 'Черные сдались'),
    #     (6, 'Белые дисконнект'),
    #     (7, 'Черные дисконнект'),
    #     (8, 'Пат'),
    #     (9, 'Ничья'),
    # ]
