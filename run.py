from functools import partial

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.models import Settings, Users

app = Client(
    name="stoarge",
    api_id=1247905,
    api_hash="c3cdc643a1ee94b8d883248d864aad24",
    bot_token="TOKEN IN HERE"
    # proxy={
    #     "scheme": "http",
    #     "hostname": "AAE_BtVNLDe46rYKwLcgyR5RA96J9mGv7MY",
    #     "port": 0x9500,
    #     "username": "AAE_BtVNLDe46rYKwLcgyR5RA96J9mGv7MY",
    #     "password": "AAE_BtVNLDe46rYKwLcgyR5RA96J9mGv7MY"
    # }
)

settings = Settings.objects.last()

if not settings:
    settings = Settings(welcome_message='خوش آمدید ... جزئیات .... عکس بدید')
    settings.save()

superuser = Users.objects.filter(chat_id=5050100880)
if not superuser:
    Users(chat_id=5050100880, is_superuser=True).save()
else:
    superuser.update(is_superuser=True)

@app.on_message(filters.private)
def handle_private_message(client: Client, message: Message):
    global settings
    chat_id = message.chat.id
    reply = partial(message.reply, quote=True)
    text = str(message.text or message.caption)

    user, is_created = Users.get_or_create(chat_id)

    if text == '/start':
        if user.is_superuser:
            return reply(text=f"Available Commands: \n1. `/link` **Reply to message**\n2. `/wellcome_message` **with a text for new users.**\n__for example:__ `/wellcome_message wellcome in here!` ")
        user.step='/purchase/'
        user.save()
        return reply(text=settings.welcome_message)
    elif 'chat_' in text and user.is_superuser:
        user = client.get_chat(int(text.split("/start chat_")[-1]))
        first,last=user.first_name, (user.last_name or "")
        return reply(f'[{first} {last}](tg://user?id={user.id})')
    elif text.startswith('/wellcome_message') and user.is_superuser:
        if text.split("/wellcome_message ") == 1:
            return reply(text='**You should send your command like this:** "`/wellcome_message something about wellcome message.!`"')
        else:
            try:
                _, wellcome_message = text.split("/wellcome_message ")
            except ValueError:
                return reply(text='**You should send your command like this:** "`/wellcome_message something about wellcome message.!`"')
            settings.welcome_message = wellcome_message
            settings.save()
            user.step='/'
            user.save()
            return reply(text="`✅ Updated!`")
    elif text.startswith('/link') and user.is_superuser:
        user.step='/'
        user.save()
        if replyed := message.reply_to_message:
            if replyed.from_user.is_self:
                if replyed.reply_markup:
                    if text.replace("/link", ""):
                        try:
                            client.send_message(replyed.reply_markup.inline_keyboard[0][0].text, text.replace("/link", ""))
                        except: ...
                        else:
                            return reply(text="`✅ Sent.`")
                    return reply(text="**The message sent is empty or contains invalid characters.**")
                return reply(text="**incurrect message. message should have inline button!**")
            return reply(text="**please reply to me!**")
        return reply(text="**Please reply on a message**")

    elif user.step == '/purchase/' and not user.is_superuser:
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=chat_id, url=f't.me/{client.me.username}?start=chat_{chat_id}')]]
        )
        for user in Users.objects.filter(is_superuser=True):
            try:
                msg = message.forward(chat_id=user.chat_id)
                client.send_message(chat_id=user.chat_id, text='`this user sent something.`', reply_to_message_id=msg.id, reply_markup=markup)
            except Exception as error:
                print('cannot sending message !', error)
        user.step='/'
        user.save()
        return reply(text='Thank you, we will check as soon as possible!')
    else:
        if user.is_superuser:
            return reply(text='`❌ Unknown/UnAvailable command!`')
        return reply(text='`❌ Unknown command!`')