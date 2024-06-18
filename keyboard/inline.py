import random

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
)

from signature import userdb
from loader_cfg import (
    dice_link, pay_link, back_money, sub_link
)


class UserKeyboard:
    @staticmethod
    def user_menu():
        button = [
            ("Игры", "plays"),
            ("Профиль", "profile"),
            ("Бонусы", "bonuss"),
            ("Как играть?", "get_play"),
            ("Правила", "rules"),
            ("Статистика", "static"),
            ("Поддержка", "support"),
        ]

        menu = InlineKeyboardBuilder()
        for text, callback_data in button:
            menu.add(InlineKeyboardButton(text=text, callback_data=callback_data))
        return menu.adjust(1, 2, 1, 3).as_markup()
    
    @staticmethod
    def check_subs():
        buttons = [
            ("Подписаться", sub_link)
        ]
        menu = InlineKeyboardBuilder()
        for text, url in buttons:
            menu.add(InlineKeyboardButton(text=text, url=url))
        return menu.adjust(1).as_markup()


    @staticmethod
    def user_ref_menu():
        buttons = [
            ("Рефералка", "ref"),
            ("Вывести", "back_money"),
            ("Назад", "back")
        ]

        menu = InlineKeyboardBuilder()
        for text, callback_data in buttons:
            menu.add(InlineKeyboardButton(text=text, callback_data=callback_data))
        return menu.adjust(1, 1).as_markup()
    
    @staticmethod
    def back_referal():
        buttons = [
            ("Назад", "back_ref")
        ]

        menu = InlineKeyboardBuilder()
        for text, callback_data in buttons:
            menu.add(InlineKeyboardButton(text=text, callback_data=callback_data))
        return menu.adjust().as_markup()
    
    @staticmethod
    def back_stat():
        buttons = [
            ("Назад", "back")
        ]

        menu = InlineKeyboardBuilder()
        for text, callback_data in buttons:
            menu.add(InlineKeyboardButton(text=text, callback_data=callback_data))
        return menu.adjust().as_markup()

    @staticmethod
    async def get_bonus_menu():
        buttons = await userdb.get_price_bonus()
        
        menu = InlineKeyboardBuilder()
        for b in buttons:
            print(b)
            menu.add(InlineKeyboardButton(text=f"{b.name_bonus} - {b.price}$", callback_data=f'bonus_{b.id}'))
        menu.row(InlineKeyboardButton(text='Назад', callback_data='back'))
                 
        return menu.adjust(1).as_markup()

    @staticmethod
    def back_bonus(url):
        buttons = [
            ("Проверить", "check"),
            ("Назад", "back_bonus"),
        ]

        menu = InlineKeyboardBuilder()
        menu.row(InlineKeyboardButton(text='Купить', url=url))
        for text, callback_data in buttons:
            menu.add(InlineKeyboardButton(text=text, callback_data=callback_data))
        return menu.adjust(1).as_markup()
    
    @staticmethod
    def payment_back():
        buttons = [
            ("Вернуться в меню", "back")
        ]

        menu = InlineKeyboardBuilder()
        for text, callback_data in buttons:
            menu.add(InlineKeyboardButton(text=text, callback_data=callback_data))
        return menu.adjust().as_markup()
    
    def get_plays():
        buttons = [
            ("Кубик", dice_link)
        ]

        menu = InlineKeyboardBuilder()
        for text, url in buttons:
            menu.add(InlineKeyboardButton(text=text, url=url))
        menu.row(InlineKeyboardButton(text='Назад', callback_data='back'))
        return menu.adjust(1).as_markup()
    
    @staticmethod
    def create_link():
        bay = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🫦Испытать удачу", url=pay_link)]
        ])
        return bay
    
    @staticmethod
    def get_box(url):
        bay = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Забрать", url=url)]
        ])
        return bay
    
    @staticmethod
    def back_user_money():
        buttons = [
            ("Забрать", back_money)
        ]

        menu = InlineKeyboardBuilder()

        for text, url in buttons:
            menu.add(InlineKeyboardButton(text=text, url=url))    
        return menu.as_markup()
    
    @staticmethod
    def get_create_mines(player_id, user_bet):
        menu = InlineKeyboardBuilder()
        for x in range(7, 0, -1):
            row_buttons = []
            random_button_index = random.randint(0, 2)
            for button_num in range(3):
                if button_num == random_button_index:
                    callback_data = f"win_{x}_{player_id}"
                    text = "🎁"
                else:
                    callback_data = f"mines_{player_id}_{x}"
                    text = '🎁'
                row_buttons.append((text, callback_data))
            
            for text, callback_data in row_buttons:
                menu.add(InlineKeyboardButton(text=text, callback_data=callback_data))
        menu.row(InlineKeyboardButton(text=f'Забрать {user_bet}💲', callback_data=f'save_{player_id}_{user_bet}'))

        return menu.adjust(3).as_markup()