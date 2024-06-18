from sqlalchemy import BigInteger
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs

from loader_cfg import sqlalchemy_url

engine = create_async_engine(sqlalchemy_url)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    all_money: Mapped[int] = mapped_column(Float(), default=0)
    all_play: Mapped[int] = mapped_column(Integer(), default=0)
    count_vin: Mapped[int] = mapped_column(Integer(), default=0)
    money_ref: Mapped[int] = mapped_column(Float(), default=0)
    bonus: Mapped[str] = mapped_column(String(), default='Отсутствует')
    time: Mapped[int] = mapped_column(Integer(), default=0)
    percent: Mapped[int] = mapped_column(Float(), default=0)


class Ref(Base):
    __tablename__ = 'referrer'

    user_id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    referrer_id: Mapped[int] = mapped_column(BigInteger(), nullable=True)


class Statistic(Base):
    __tablename__ = 'statistic'

    all_dep: Mapped[int] = mapped_column(Integer(), default=0, primary_key=True)
    all_pay: Mapped[int] = mapped_column(Integer(), default=0)
    
    


class PriceBonus(Base):
    __tablename__ = 'price_bonus'

    id: Mapped[int] = mapped_column(primary_key=True)
    name_bonus: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer())
    percent: Mapped[int] = mapped_column(Float())
    time: Mapped[int] = mapped_column(Integer())


class Percent(Base):
    __tablename__ = 'percent'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    play: Mapped[str] = mapped_column(String())
    status: Mapped[int] = mapped_column(Integer())
    percent_one: Mapped[int] = mapped_column(Float())
    percent_two: Mapped[int] = mapped_column(Float())


async def async_main():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print('error', e)
