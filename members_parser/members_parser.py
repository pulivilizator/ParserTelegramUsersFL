import asyncio
from datetime import datetime, timedelta
from pyrogram import Client
from pyrogram.errors.rpc_error import RPCError
from config import config
from excel_writer.writer import writer
from .get_dates import getting_data
from exceptions import GetUserDataException
import configparser
from pyrogram.errors import FloodWait, MsgIdInvalid
from pyrogram.enums import ChatMembersFilter


async def parser_chats(app, writer: writer, chat: str):
    async def async_generator():
        counter = 0
        admins = app.get_chat_members(chat, filter=ChatMembersFilter.ADMINISTRATORS)
        async for user in admins:
            data, chek = getting_data(user.user, chat, True)
            yield data
        async for member in app.get_chat_members(chat):
            counter += 1
            print(counter, chat)
            try:
                if str(member.status) in ('ChatMemberStatus.ADMINISTRATOR', 'ChatMemberStatus.CREATORS'):
                    continue
                else:
                    data, check = getting_data(member.user, chat)
                if not check:
                    continue
                yield data
            except RPCError:
                raise GetUserDataException('Ошибка обработки/получения данных пользователя')

    await writer.writer(async_generator())


async def parser_channels(app, writer: writer, chat: str):
    async def async_generator():
        counter = 0
        posts = (
            message
            async for message in app.get_chat_history(chat)
            if message.date.strftime('%Y%d%m') in [(datetime.now() - timedelta(days=i)).strftime('%Y%d%m')
                                                   for i in range(1, paths.getint('program', 'days') + 1)]
        )
        async for post in posts:
            try:
                async for i in app.get_discussion_replies(chat, post.id):
                    counter += 1
                    print(counter, chat)
                    data, check = getting_data(i.from_user, chat)
                    if not check:
                        continue
                    yield data
            except MsgIdInvalid:
                pass

            except FloodWait as wait:
                print(f'FlooWait: {wait.value}')
                await asyncio.sleep(wait.value)

    await writer.writer(async_generator())


async def main_parser(app, writer: writer, chat: str):
    async with app:
        channel_type = str([i async for i in app.get_chat_history(chat, limit=1)][0].chat.type)
        if channel_type == 'ChatType.SUPERGROUP':
            await parser_chats(app, writer, chat)
        elif channel_type == 'ChatType.CHANNEL':
            await parser_channels(app, writer, chat)


def start_app():
    chats = writer.get_rows()
    for chat in chats:
        app.run(main_parser(app, writer, chat))


paths = configparser.ConfigParser()
paths.read('config.ini', encoding='utf-8')
session_data = config(paths.get('program', 'env'))
writer.create_file()
app = Client("session", api_id=int(session_data.api_id), api_hash=session_data.api_hash)
