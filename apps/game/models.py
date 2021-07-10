from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, sql
from sqlalchemy.orm import relationship, backref
from db import Base


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    # chess_variants = [
    #     (1, 'Инь-Ян'),
    #     (2, 'Фланговая'),
    #     (3, 'Инь-ян / Фланговая'),
    #     (4, 'Инь-ян / Фибоначчи'),
    #     (15, 'Классические'),
    #     (16, 'Фишера'),
    # ]
    #
    # chess_variant = Column
    arrangement = Column(Integer)
    # white = Column(Integer, ForeignKey())
    # black = Column(Integer, ForeignKey())
    moves = Column(String)

    # results = [
    #     (0, 'Недоиграна'),
    #     (1, 'Белые победили'),
    #     (2, 'Чёрные победили'),
    #     (3, 'Белые сдались'),
    #     (4, 'Черные сдались'),
    #     (5, 'Белые дисконнект'),
    #     (6, 'Черные дисконнект'),
    #     (7, 'Пат'),
    #     (9, 'Ничья'),
    # ]
    # result = Column

    # start_game = Column

    # title = Column(String)
    # text = Column(String(350))
    # date = Column(DateTime(timezone=True), server_default=sql.func.now())
    # user = Column(String, ForeignKey('user.id'))
    # user_id = relationship("User")
    # parent_id = Column(Integer, ForeignKey('microblog_posts.id'), nullable=True)
    # children = relationship("Post", backref=backref('parent', remote_side=[id]))


posts = Game.__table__
