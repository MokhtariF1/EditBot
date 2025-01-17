from telethon import events, Button, TelegramClient, types
from sqlite3 import connect
import config


bot = TelegramClient("bot", config.api_id, config.api_hash,
                     proxy=None if config.proxy is False else config.proxy_address)
print("connecting...")
bot.start(bot_token=config.bot_token)
# bot.start()
# bot.connect()
print("connected!")
db = connect('bot.db')
cur = db.cursor()
bot_text = config.bot_text


@bot.on(events.NewMessage())
async def new_message(event):
    user_id = None
    if type(event.original_update.message.peer_id) == types.PeerUser:
        user_id = event.original_update.message.peer_id.user_id
        if user_id in config.admins:
            buttons = [
                Button.inline(bot_text["show_text"], b'show_text')
            ]
            await event.reply(bot_text["start"], buttons=buttons)


@bot.on(events.NewMessage(chats=config.channel_id))
async def channel_message(event):
    print(event.text)
    e = event.message.entities
    text_msg = event.message.text
    status = cur.execute("SELECT status FROM end_text").fetchone()
    if status[0] == "on":
        peer_id = event.original_update.message.peer_id.channel_id
        text = cur.execute("SELECT text FROM end_text").fetchone()[0]
        await bot.edit_message(peer_id, event.message.id, text_msg + "\n\n" + text, formatting_entities=e)

@bot.on(events.CallbackQuery(data=b'show_text'))
async def show_text(event):
    user_id = event.sender_id
    status = cur.execute("SELECT status FROM end_text").fetchone()
    text = cur.execute("SELECT text FROM end_text").fetchone()[0]
    status_fa = "🔴وضعیت"
    if status[0] == "on":
        status_fa = "🟢وضعیت"
    buttons = [
        [
            Button.inline(status_fa, b'change_status')
        ],
        [
            Button.inline(bot_text["edit_text"], b'edit_text')
        ]
    ]
    await event.reply(bot_text["text_info"].format(text=text), buttons=buttons)


@bot.on(events.CallbackQuery(data=b'change_status'))
async def change_status(event):
    user_id = event.sender_id
    msg_id = event.original_update.msg_id
    status = cur.execute("SELECT status FROM end_text").fetchone()
    text = cur.execute("SELECT text FROM end_text").fetchone()
    fa_status = "🟢وضعیت"
    if status[0] == "on":
        fa_status = "🔴وضعیت"
        buttons = [
            [
                Button.inline(fa_status, b'change_status')
            ],
            [
                Button.inline(bot_text["edit_text"], b'edit_text')
            ]
        ]
        cur.execute(f"UPDATE end_text SET status = 'off'")
        db.commit()
        await bot.edit_message(user_id, msg_id, bot_text["text_info"].format(text=text[0]), buttons=buttons)
    else:
        buttons = [
            [
                Button.inline(fa_status, b'change_status')
            ],
            [
                Button.inline(bot_text["edit_text"], b'edit_text')
            ]
        ]
        cur.execute(f"UPDATE end_text SET status = 'on'")
        db.commit()
        await bot.edit_message(user_id, msg_id, bot_text["text_info"].format(text=text[0]), buttons=buttons)


@bot.on(events.CallbackQuery(data=b'edit_text'))
async def edit_text(event):
    user_id = event.sender_id
    async with bot.conversation(user_id, timeout=1000) as conv:
        back = Button.text(bot_text["back"], resize=1)
        await conv.send_message(bot_text["enter_text"], buttons=back)
        text = await conv.get_response()
        text = text.raw_text
        if text == bot_text["back"]:
            await conv.send_message(bot_text["canceled"])
            return
        else:
            cur.execute(f"UPDATE end_text SET text = '{text}'")
            db.commit()
            await conv.send_message(bot_text["saved"])
    # user_id = None
    # if type(event.original_update.message.peer_id) == types.PeerChannel:
    #     return
    # elif type(event.original_update.message.peer_id) == types.PeerChat:
    #     return
    # elif type(event.original_update.message.peer_id) == types.PeerUser:
    #     user_id = event.original_update.message.peer_id.user_id
    # else:
    #     return


bot.run_until_disconnected()
