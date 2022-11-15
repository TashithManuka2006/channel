import firebase_admin, requests, glob, shutil, imgbbpy
from mega import Mega
from firebase_admin import db, credentials
from telethon import TelegramClient, events, Button

firebase_admin.initialize_app(
    credentials.Certificate('firebase_json_file'),
    {
        'databaseURL': 'firebase_database_url'
    }
)
ref = db.reference('/')

VARS = {
    'API_ID': 'your_api_id',
    'API_HASH': 'your_api_hash',
    'BOT_TOKEN': '5484339827:AAGnILyXB3gAKjvW9mkLCua-03mUungjZEY',
    'GROUP_ID': -1001645270143,
    'ADMIN_LIST': [
        2053401462,
        1827968336,
        2086539199
    ],
    'CHANNEL_ID': -1001158782572
}

app = TelegramClient(
    'bot',
    VARS[
        'API_ID'
    ],
    VARS[
        'API_HASH'
    ]
).start(
    bot_token=VARS[
        'BOT_TOKEN'
    ]
)


@app.on(events.NewMessage())
async def add_to_db(event):
    chat = await event.get_chat()
    chat_id = chat.id

    list1 = []
    for i in ref.get().values():
        list1.append(i)

    global list2
    list2 = []
    for i in list1:
        for val in i.values():
            list2.append(val)

    if chat_id not in list2:
        ref.push(
            {
                'ID': chat_id
            }
        )


@app.on(events.NewMessage(pattern='/start'))
async def start_on_private(event):
    sender = await event.get_input_sender()
    chat = await event.get_chat()
    buttons = [
        [
            Button.url(
                '🔰 Channel 🔰',
                't.me/SinhalaAthalMeme'
            ),
            Button.url(
                '📥 Chat Group 📥',
                't.me/SinhalaAthalMeme_Chat'
            )
        ],
        [
            Button.url(
                '⚜️ Owner ⚜️',
                't.me/Dng_Rider'
            )
        ],
        [
            Button.url(
                '🤖 OWNER CONTACT BOT 🤖',
                't.me/SinhalaAthalMeme_bot'
            )
        ]
    ]  # [Button.inline('Admin List', 'admin_list')]

    name = chat.first_name
    # if chat == 'User':
    # elif chat == 'Channel':
        # msg = f'Hi, Welcome to *🎭 සංහල ආතල් Meme 🎭 [OFFICIAL BOT]*\n\n/help use කරන්න help menu එක ගන්න.'

    msg1 = f'Hi [{name}](t.me/{chat.username}), Welcome to *🎭 සංහල ආතල් Meme 🎭 [OFFICIAL BOT]*\n\n/help use කරන්න help menu එක ගන්න.'
    await app.send_file(
        entity=sender,
        file='https://res.cloudinary.com/da4uxvcr5/image/upload/v1657963145/photo_2022-07-13_13-41-20_shglm7.jpg',
        caption=msg1,
        buttons=buttons
    )
    '''await app.send_message(
        sender,
        'Developing period එකේ තියෙන්නෙ. Bot තාම හරියට වැඩ නෑ.'
    )'''


@app.on(events.NewMessage(pattern='/help'))
async def help(event):
    sender = await event.get_input_sender()

    btns = [
        [
            Button.inline(
                '📥 Contact Admin 📥',
                'contact_admin'
            )
        ],
        [
            Button.inline(
                '♻️ ඔයාගෙ post එකක් adminලට දාන්න. ♻️',
                'send_post_to_admin'
            )
        ]
    ]

    msg2 = '''මේ බොටාගෙන් ඔයාට පුලුවන් [සිංහල ආතල් Meme 🎭 #Meme Store🤣] (t.me/SinhalaAthalMeme) Channel එකේ adminලව contact කරගන්න වගේම ඔයාල ගාව තියෙන posts adminලට දාන්න. පහල Buttons use කරන්න.'''

    await app.send_message(
        sender,
        msg2,
        buttons=btns,
        link_preview=False
    )
    '''await app.send_message(
        sender,
        'Developing period එකේ තියෙන්නෙ. Bot තාම හරියට වැඩ නෑ.'
    )'''

@app.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    global msg
    sender = await event.get_input_sender()
    chat = await event.get_chat()
    chat_id = chat.id

    if chat_id in VARS['ADMIN_LIST']:
        msg = await app.send_message(
            sender,
            'Send message to broadcast!'
        )
    elif chat_id not in VARS['ADMIN_LIST']:
        await app.send_message(
            sender,
            'This command is only for admins. Don\'t use this command again!'
        )


    async with app.conversation(chat_id) as conv:
        broadcast_message = await conv.get_response(msg.id)

    for i in list2:
        requests.get(
            f'https://api.telegram.org/bot5484339827:AAGnILyXB3gAKjvW9mkLCua-03mUungjZEY/sendMessage?chat_id={i}&text={broadcast_message}'
        )

    await app.send_message(sender, 'DONE!\n\nMessage delivered to all the bot users!')


@app.on(events.CallbackQuery)
async def callbackquery(event):
    sender = await event.get_input_sender()
    chat = await event.get_chat()
    if event.data == b'contact_admin':
        msg = await app.send_message(sender, 'Type your message and send to me. I will forward it to admins!')
        async with app.conversation(chat.id) as conv:
            msg_to_admins = await conv.get_response(msg.id)
        
        await app.forward_messages(VARS['GROUP_ID'], msg_to_admins.id, sender)

        await app.send_message(sender, 'Done your message forwarded to admins! They will response you. Plz wait for response.')
    
    if event.data == b'send_post_to_admin':
        global post_to_channel
        global caption
        global up_img
        global post
        global accept_or_reject
        msg = await app.send_message(sender, 'Send post to channel!')
        async with app.conversation(chat.id) as conv:
            post_to_channel = await conv.get_response(msg.id)
        await app.send_message(sender, 'Your post forwarded to admins. If they accept it, It will post on Channel!')

        post = await app.forward_messages(VARS['GROUP_ID'], post_to_channel.id, sender)

        accept_or_reject = await app.send_message(VARS['GROUP_ID'], 'Do you accept this?', reply_to=post, buttons=[[Button.inline('Accept', 'accept'), Button.inline('Reject', 'reject')]])
        
        await app.download_media(post_to_channel, './down/file')

        client = imgbbpy.SyncClient('your_imgbb_api_key')
        
        for i in glob.glob(r'./down/file.*'):
            up_img = client.upload(file=i)
        shutil.rmtree('./down')

        caption = f'''
{post_to_channel.message}

Post from: [{chat.first_name}](t.me/{chat.username}) ---> {chat.id},

🎭 සංහල •─ ආතල් •─ Meme 🎭•─ 🔫
 @SinhalaAthalMeme  

🎭 සංහල •─ ආතල් •─ Meme 🎭•─ 🔫 චැට් ලන්තය 🤣
@SinhalaAthalMeme_Chat 

 ♡ ㅤ  ❍ㅤ    ⎙ㅤ  ⌲ 
 ˡᶦᵏᵉ  ᶜᵒᵐᵐᵉⁿᵗ  ˢᵃᵛᵉ  ˢʰᵃʳᵉ
'''
    if event.data == b'accept':
        await app.send_file(VARS['CHANNEL_ID'], up_img.url, caption=caption)
        await app.send_message(sender, f'Your post accepted!')
        await app.delete_messages(VARS['GROUP_ID'], [post.id, accept_or_reject.id])
    elif event.data == b'reject':
        await app.send_message(sender, f'Your post rejected!')
        await app.delete_messages(VARS['GROUP_ID'], [post.id, accept_or_reject.id])


if __name__ == '__main__':
    app.start()
    app.run_until_disconnected()
