from pyrogram.types.user_and_chats.user import User


def getting_data(member: User, chat):
    name = _name(member)
    bot = 'бот' if member.is_bot else 'не бот'
    last_online = _last_online(member)
    chat = _chat(chat)
    data = [name,
            member.username,
            member.id,
            member.phone_number,
            last_online,
            bot,
            chat]
    return data, last_online


def _name(member: User):
    first_name = member.first_name
    last_name = member.last_name
    if last_name and first_name:
        return f'{first_name} {last_name}'
    elif first_name:
        return first_name
    elif last_name:
        return last_name
    return None


def _last_online(member: User):
    if member.last_online_date:
        return member.last_online_date
    match str(member.status):
        case 'UserStatus.ONLINE':
            return 'Онлайн'
        case 'UserStatus.RECENTLY':
            return 'Заходил недавно'
        case 'UserStatus.LAST_WEEK':
            return 'Заходил в течении недели'
        case 'UserStatus.LAST_MONTH':
            return 'Заходил в течении месяца'
        case 'UserStatus.LONG_AGO':
            return False

def _chat(chat: str):
    return f'https://t.me/{chat}'