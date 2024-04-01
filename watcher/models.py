from datetime import datetime

from sqlalchemy import Column, Integer, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapped_column, Mapped


Base = declarative_base()

user_serial = Table('user_serial', Base.metadata,
                    Column('user_id', ForeignKey('users.id'), primary_key=True),
                    Column('serial_id', ForeignKey('serials.id'), primary_key=True)
                    )


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    username: Mapped[str]
    last_name: Mapped[str]
    tracked_series: Mapped[str] = mapped_column(nullable=True)
    watched_series: Mapped[str] = mapped_column(nullable=True)
    tg_user_id: Mapped[int]

    watching_serials = relationship('Serial', secondary=user_serial, back_populates='watching_users')


class Serial(Base):
    __tablename__ = 'serials'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True)
    last_episode: Mapped[str] = mapped_column(nullable=True)
    last_season: Mapped[str] = mapped_column(nullable=True)
    last_update: Mapped[datetime] = mapped_column(nullable=True)

    watching_users = relationship('User', secondary=user_serial, back_populates='watching_serials')

    site_id = Column(Integer, ForeignKey('sites.id'))
    site = relationship('Site', back_populates='serials')


class Site(Base):
    __tablename__ = 'sites'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    name: Mapped[str]

    serials = relationship('Serial', back_populates='site')
