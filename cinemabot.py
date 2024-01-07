import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from templates import render_template
from config import TELEGRAM_BOT_TOKEN
from cinemaservice import find_movie, find_movie_link
from dbservice import add_history, get_history, get_stats


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(render_template('start.j2'))


@dp.message(Command('help'))
async def command_help_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    await message.answer(render_template('help.j2'))


@dp.message(Command('history'))
async def command_history_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/history` command
    """
    if message.from_user:
        await message.answer(
            render_template(
                'history.j2',
                {'movies': await get_history(message.from_user.id)}
            )
        )


@dp.message(Command('stats'))
async def command_stats_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/stats` command
    """
    if message.from_user:
        await message.answer(
            render_template(
                'stats.j2', {'movies': await get_stats(message.from_user.id)}
            )
        )


@dp.message()
async def find_film_handler(message: types.Message) -> None:
    """
    Handler will send link for a film
    """
    if not message.text or not message.from_user:
        return

    movie = await find_movie(message.text)

    if not movie:
        await message.reply(
            render_template(
                'find_film_aborted.j2', {'film_name': message.text}
            )
        )
        return

    await add_history(message.from_user.id, movie.name)

    if movie.poster_url:
        poster = types.URLInputFile(
            movie.poster_url
        )
        try:
            text = render_template(
                'find_film.j2',
                {'movie': movie, 'link': await find_movie_link(movie.name)}
            )
            await message.answer_photo(poster, text, parse_mode='html')
        except Exception as e:
            logging.exception(e)
            await message.reply(
                render_template(
                    'find_film.j2',
                    {'movie': movie, 'link': await find_movie_link(movie.name)}
                ),
                parse_mode='html')


async def main() -> None:
    bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
