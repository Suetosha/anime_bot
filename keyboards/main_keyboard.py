from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon import COMMAND_LEXICON


async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/help',
                   description=COMMAND_LEXICON['/help']),
        BotCommand(command='/add_anime',
                   description=COMMAND_LEXICON['/add_anime']),
        BotCommand(command='/added_anime_list',
                   description=COMMAND_LEXICON['/added_anime_list']),
        BotCommand(command='/get_updates',
                   description=COMMAND_LEXICON['/get_updates']),
        BotCommand(command='/get_anime_list',
                   description=COMMAND_LEXICON['/get_anime_list']),
        BotCommand(command='/mailing',
                   description=COMMAND_LEXICON['/mailing']),

    ]
    await bot.set_my_commands(main_menu_commands)
