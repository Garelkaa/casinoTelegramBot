import json

with open("config.json", mode="r", encoding="utf-8") as cfg:
    data = json.loads(cfg.read())

    for item in data:
        if "bot_token" in item:
            TOKEN = item["bot_token"]
            db_user = item["DB_USER"]
            password = item["DB_PASSWORD"]
            host = item["DB_HOST"]
            db_name = item["DB_NAME"]
            api_token_pay = item['pay_token']
            chat_id = item["chat_id"]
            casino_chat = item["casino_chat"]
            admin_ids = item["admin_ids"]
            pay_link = item["pinned_link"]
            back_money = item["back_money"]
            sub_link = item["sub_link"]
            erorr_users = item["erorr_users"]
            ref_link = item["ref_link"]
            mines_users = item["mines_users"]
            random_lose_mes = item["random_lose_mes"]
        elif "plays_link" in item:
            links = item["plays_link"]
            dice_link = links["dice"]
        elif "play_game" in item:
            numbers = item["play_game"]

    sqlalchemy_url = f'postgresql+asyncpg://{db_user}:{password}@{host}/{db_name}'
