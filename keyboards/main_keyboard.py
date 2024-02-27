from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Помощь'),
        BotCommand(command='add_anime',
                   description='Добавить аниме'),
        BotCommand(command='/anime_list',
                   description='Посмотреть список добавленных аниме'),
        BotCommand(command='/get_updates',
                   description='Получить новые апдейты'),
    ]
    await bot.set_my_commands(main_menu_commands)