from decimal import Decimal
from sqlalchemy import select, insert, update

from database.models import User, Ref, Statistic, PriceBonus, Percent, async_session


class UserDb:
    @staticmethod
    async def check_user(user_id, name):
        async with async_session() as session:
            existing_user = await session.execute(select(User.user_id).where(User.user_id == user_id))
            existing_user = existing_user.scalar_one_or_none()

            if not existing_user:
                await session.execute(insert(User).values(user_id=user_id, name=name))
                await session.commit()

    @staticmethod
    async def get_user(user_id):
        async with async_session() as session:
            user = await session.execute(select(User).where(User.user_id == user_id))
            user = user.scalar_one_or_none()
            return user
        
    @staticmethod
    async def check_user_referrer(user_id, referrer_id, name):
        async with async_session() as session:
            existing_user = await session.execute(select(Ref).where(
                Ref.referrer_id == referrer_id and Ref.user_id == user_id
                ))
            existing_user = existing_user.scalar_one_or_none()

            if not existing_user:
                await session.execute(insert(Ref).values(user_id=user_id, referrer_id=referrer_id,
                                                         name=name))
                await session.commit()
            return False
        
    @staticmethod
    async def get_statistic():
        async with async_session() as session:
            stat = await session.execute(select(Statistic))
            stat = stat.scalar()

            query = select(User.user_id)
            result = await session.execute(query)
            users = result.scalars().all()

            return stat, len(users)
        
    @staticmethod
    async def get_price_bonus():
        async with async_session() as session:
            bonus = await session.execute(select(PriceBonus))
            return bonus.scalars().all()
        
    @staticmethod
    async def get_bonus(id):
        async with async_session() as session:
            bonus = await session.execute(select(PriceBonus).where(PriceBonus.id == id))
            bonus = bonus.scalar_one_or_none()
            return bonus
        
    @staticmethod
    async def update_bonus(user_id, name_bonus, time, percent):
        async with async_session() as session:
            await session.execute(update(User).where(User.user_id == user_id).values(
                bonus=name_bonus,
                  time=time,
                  percent=percent))
            await session.commit()

    @staticmethod
    async def add_user_bet(user_id, name, money_ref, count_vin, all_play, all_money):
        async with async_session() as session:
            existing_user = await session.execute(select(User).where(User.user_id == user_id))
            existing_user = existing_user.scalar_one_or_none()

            if not existing_user:
                new_user = User(
                    user_id=user_id, name=name,
                    money_ref=money_ref, count_vin=count_vin,
                    all_play=all_play, all_money=all_money
                )
                session.add(new_user)
            else:
                existing_user.money_ref += money_ref
                existing_user.count_vin += count_vin
                existing_user.all_play += all_play
                existing_user.all_money += all_money

            await session.commit()

    @staticmethod
    async def get_percent_cub_one(status, play):
        async with async_session() as session:
            if status == 1:
                percent = await session.execute(select(Percent.percent_one).where(
                    Percent.status == status,
                      Percent.play == play))
            else:
                percent = await session.execute(select(Percent.percent_two).where(
                    Percent.status == status,
                      Percent.play == play))
                
            percent = percent.scalar()
            return percent

    @staticmethod
    async def add_statistic(all_dep, all_pay):
        async with async_session() as session:
            existing_stst = await session.execute(select(Statistic))
            existing_stst = existing_stst.scalar_one_or_none()

            if not existing_stst:
                new_stat = Statistic(
                    all_dep=all_dep,
                    all_pay=all_pay
                )
                session.add(new_stat)
            else:
                existing_stst.all_dep += all_dep
                existing_stst.all_pay += all_pay

            await session.commit()

    @staticmethod
    async def add_user_ref_money(user_id, amount):
        async with async_session() as session:
            async with session.begin():
                referrer_id_result = await session.execute(select(Ref.referrer_id).where(Ref.user_id == user_id))
                referrer_id = referrer_id_result.scalar_one_or_none()

                if not referrer_id:
                    return
                
                referrer_money_result = await session.execute(select(User.money_ref).where(User.user_id == referrer_id))
                referrer_money = referrer_money_result.scalar_one_or_none()
                
                if referrer_money is None:
                    return
                
                percent = amount / 5
                new_amount = referrer_money + percent
                await session.execute(
                    update(User)
                    .where(User.user_id == referrer_id)
                    .values(money_ref=new_amount)
                )

                await session.commit()

    @staticmethod
    async def get_user_ref(name):
        async with async_session() as session:
            user = await session.execute(select(User.user_id).where(User.name == name))
            user = user.scalar_one_or_none()
            return user if user else None
        
    @staticmethod
    async def get_user_bonus_percent(user_id):
        async with async_session() as session:
            bonus = await session.execute(select(User).where(User.user_id == user_id))
            bonus = bonus.scalar_one_or_none()
            if bonus.bonus != 'Отсутствует':
                return bonus.percent
            return None