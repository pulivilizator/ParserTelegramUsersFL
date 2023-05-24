from pyrogram import Client
from pyrogram.errors.rpc_error import RPCError
from config import config
from excel_writer.writer import ExcelWriter
from .get_dates import getting_data
from exceptions import GetUserDataException


async def parser(app, writer: ExcelWriter, chat: str):
    counter = 0
    async with app:
        async for member in app.get_chat_members(chat):
            counter += 1
            print(counter, chat)
            try:
                data, check = getting_data(member.user, chat)
                if not check:
                    continue
                writer.writer(data)
            except RPCError:
                raise GetUserDataException('Ошибка обработки/получения данных пользователя')


def start_app():
    chats = writer.get_rows()
    for chat in chats:
        app.run(parser(app, writer, chat))


session_data = config()
writer = ExcelWriter()
writer.create_file()
app = Client("session", api_id=int(session_data.api_id), api_hash=session_data.api_hash)
