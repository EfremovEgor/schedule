from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
import parse_data
import csv
import asyncio
import aioschedule
import parse_schedule as ps

TOKEN = "6169975124:AAFoc4LiUZryQLpNIi-Wceq7kfpVC0rAciw"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def get_new_schedule():
    file = "current_schedule"
    try:
        df = ps.prepare_df(full_path=f"downloads\\{file}.xlsx")
    except parse_data.PageDoesNotResponseException:
        for channel in get_channels():
            await bot.send_message(channel, "Проблемы с сайтом")
            await asyncio.sleep(120)
            return
    ps.save_df(df, f"raw_{file}")
    ps.save_df(ps.split_schedule(df, "upper"), f"upper_{file}")
    ps.save_df(ps.split_schedule(df, "lower"), f"lower_{file}")

    for channel in get_channels():
        media = types.MediaGroup()
        media.attach_photo(
            types.InputFile("output\\upper_current_schedule.png"), "Верхняя"
        )
        media.attach_photo(
            types.InputFile("output\\lower_current_schedule.png"), "Нижняя"
        )
        await bot.send_media_group(channel, media=media)
        await asyncio.sleep(0.5)
    await asyncio.sleep(120)


def get_channels() -> list:
    with open("channels.csv", "r") as f:
        reader = csv.reader(f)
        data = [int(item[0]) for item in list(reader)]
    return data


async def scheduler():
    aioschedule.every().day.at("22:30").do(get_new_schedule)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


@dp.message_handler(commands=["send"])
async def send_schedule_manually(message: types.Message):
    for channel in get_channels():
        media = types.MediaGroup()
        media.attach_photo(
            types.InputFile("output\\upper_current_schedule.png"), "Верхняя"
        )
        media.attach_photo(
            types.InputFile("output\\lower_current_schedule.png"), "Нижняя"
        )
        await bot.send_media_group(channel, media=media)
        await asyncio.sleep(0.5)


@dp.channel_post_handler(Command(commands="register"))
async def register_channel(message: types.Message):
    admins = await message.chat.get_administrators()
    for admin in admins:
        if isinstance(admin, types.ChatMemberOwner):
            user_id = admin["user"]["id"]
            chat_id = message.chat.id
            with open("channels.csv", "r") as f:
                reader = csv.reader(f)
                data = [int(item[0]) for item in list(reader)]
            if chat_id not in data:
                with open("channels.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([chat_id])
                    await bot.send_message(
                        user_id, f"Chat with id: {chat_id} has been registered"
                    )
            else:
                await bot.send_message(
                    user_id, f"Chat with id: {chat_id} has already been registered"
                )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
