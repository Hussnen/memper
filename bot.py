#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
try:
    from telethon.sessions import StringSession
    import asyncio, re, json, shutil
    from kvsqlite.sync import Client as uu
    from telethon.tl.types import KeyboardButtonUrl
    from telethon.tl.types import KeyboardButton, ReplyInlineMarkup
    from telethon import TelegramClient, events, functions, types, Button
    from telethon.tl.types import DocumentAttributeFilename
    import time, datetime, random 
    from datetime import timedelta
    from telethon.errors import (
        ApiIdInvalidError,
        PhoneNumberInvalidError,
        PhoneCodeInvalidError,
        PhoneCodeExpiredError,
        SessionPasswordNeededError,
        PasswordHashInvalidError
    )
    from plugins.messages import *
    from plugins.get_code import *
    from plugins.SessionConverter import *
    from telethon.errors.rpcerrorlist import UserDeactivatedBanError
    from telethon.sessions import StringSession
    from telethon.tl.types import InputPeerUser, InputPeerChannel
    from telethon.tl.functions.account import GetAuthorizationsRequest
    from telethon.tl.functions.messages import GetHistoryRequest
except:
    os.system("python3 set_module.py")
    try:
        from telethon.sessions import StringSession
        import asyncio, re, json, shutil
        from kvsqlite.sync import Client as uu
        from telethon.tl.types import KeyboardButtonUrl
        from telethon.tl.types import KeyboardButton
        from telethon import TelegramClient, events, functions, types, Button
        from telethon.tl.types import DocumentAttributeFilename
        import time, datetime, random 
        from datetime import timedelta
        from telethon.errors import (
            ApiIdInvalidError,
            PhoneNumberInvalidError,
            PhoneCodeInvalidError,
            PhoneCodeExpiredError,
            SessionPasswordNeededError,
            PasswordHashInvalidError
        )
        from plugins.messages import *
        from plugins.get_code import *
        from plugins.SessionConverter import *
        from telethon.errors.rpcerrorlist import UserDeactivatedBanError
        from telethon.sessions import StringSession
        from telethon.tl.types import InputPeerUser, InputPeerChannel
        from telethon.tl.functions.account import GetAuthorizationsRequest
        from telethon.tl.functions.messages import GetHistoryRequest
    except Exception as errors:
        print('An Erorr with: ' + str(errors))
        exit(0)


def check_vip(user):
    user_id = int(user)
    users = db.get(f"vip_{user_id}")
    noww = time.time()
    if db.exists(f"vip_{user_id}"):
        last_time = users['vip']
        timeee = int(db.get(f"vip_{user_id}_time"))
        WAIT_TIMEE = int(timeee) * 24 * 60 * 60
        elapsed_time = noww - last_time
        if elapsed_time < WAIT_TIMEE:
            remaining_time = WAIT_TIMEE - elapsed_time
            return int(remaining_time)
        else:
            return None
    else:
        return None
        
        
if not os.path.isdir('database'):
    os.mkdir('database')

API_ID = "1724716"
API_HASH = "00b2d8f59c12c1b9a4bc63b70b461b2f"
admin = 7618293197
new_password = "@NB_DZ" #التحقق بخطوتين للحسابات التي سيتم بيعها
# Replace with your bot token
token = "8670030981:AAHmMawowuuUWoJ5OUdPw6D6xKENnLerHMQ"
client = TelegramClient('BotSession', api_id=API_ID, api_hash=API_HASH).start(bot_token=token)
bot = client

#Create DataBase
db = uu('database/KingA.ss', 'bot')

if not db.exists("accounts"):
    db.set("accounts", [])

if not db.exists("countries"):
    db.set("countries", [])

if not db.exists("bad_guys"):
    db.set("bad_guys", [])

if not db.exists("force"):
   db.set("force", [])

if not db.exists("admins"):
   db.set("admins", [admin])

@client.on(events.NewMessage(pattern="/sell_price", func = lambda x: x.is_private))
async def start(event):
    user_id = event.chat_id
    bans = db.get('bad_guys') if db.exists('bad_guys') else []
    async with bot.conversation(event.chat_id) as x:
        countries = db.get("countries")
        text = ""
        for i in countries:
            text += f'{i["name"]} ({i["calling_code"]}): {i["sell_price"]}$'
        await x.send_message(text)
@client.on(events.NewMessage(pattern="/start", func = lambda x: x.is_private))
async def start(event):
    user_id = event.chat_id
    bans = db.get('bad_guys') if db.exists('bad_guys') else []
    async with bot.conversation(event.chat_id) as x:
        try:
            force = db.get("force")
            for channel in force:
                result = await client(functions.channels.GetParticipantRequest(
                    channel=channel,
                    participant=user_id
                ))
        except Exception as a:
            await x.send_message(f"**⚠️︙عذراً عزيزي يجب عليك الاشتراك بقناة البوت**\n🚀︙القناه يتم بها عمليات تحديث البوت \n ✨︙رابط القناه : @{channel} \n\n• اشترك في القناه ثم أرسل : /start")
            return
        keyboard = [
            [
                Button.inline("💎 ⚙️ إعدادات الأرقام", data="ajxjao", style="primary"),
            ],
            [
                Button.inline("💎 📢 الإشتراك الإجباري", data="ajxkho", style="success"), 
                Button.inline("🔥 👨‍💼 قسم الإدمنية", data="aksgl", style="danger"), 
            ],
            [
                Button.inline("👑 💸 قسم البيع والشراء", data="ajkofgl", style="success"),
            ],
            [
                Button.inline("🎭 💰 قسم الرصيد", data="ajkcoingl", style="success"), 
                Button.inline("🌟 🚫 قسم الحظر", data="bbvjls", style="danger"), 
            ],
            [
                Button.inline("💎 📊 قناة إثباتات التسليم", data="set_trust_channel", style="success"),
            ],
            [
                Button.inline("🎯 📜 تعديل رسالة القوانين", data="edit_rules", style="danger"),
            ],
        ]
        
        buttons = [
            [
                Button.inline("🎯 🛒 شراء رقم", data="buy", style="success"),
            ],
            [
                Button.inline("✨ 💳 سحب رصيد", data="ssart", style="success"),
                Button.inline("🔥 🔄 تحويل رصيد", data="transfer", style="success"),
            ],
            [
                Button.inline("⚡ 👨‍💻 الدعم الفني", data="supper", style="primary"),
                Button.inline("⚡ 📋 القوانين", data="liscgh", style="primary"),
            ],
            [
                Button.inline("🔥 💱 بيع حساب", data="sell", style="success"),
            ]
        ]
        
    if user_id in bans: return
    if not db.exists(f"user_{user_id}"):
        members = 0
        db.set(f"user_{user_id}", {"coins": 0, "id": user_id})
        if user_id == admin:
            await event.reply(msgs['ADMIN_MESSAGE'], buttons=keyboard)
            await event.reply(msgs['START_MESSAGE'].format(event.chat_id, 0), buttons=buttons)
        else:
            await event.reply(msgs['START_MESSAGE'].format(event.chat_id, 0), buttons=buttons)
        user_info = await client.get_entity(user_id)
        users = db.keys('user_%')
        for _ in users:
            members+=1
        if user_info.username == None: username = "None"
        else: username = "@"+str(user_info.username)
        await bot.send_message(admin, f'• دخل شخص جديد الي البوت الخاص بك 👾\n\n- معلومات المستخدم الجديد .\n\n- اسمه : <a href="tg://user?id={user_id}">{user_info.first_name}</a>\n- معرفه : {username}\n- ايديه : {user_id}\n\n• اجمالي الاعضاء : {members}', parse_mode="html")
    else:
        coins = db.get(f"user_{user_id}")["coins"]
        if user_id == admin or user_id in db.get("admins"):
            await event.reply(msgs['ADMIN_MESSAGE'], buttons=keyboard)
            await event.reply(msgs['START_MESSAGE'].format(event.chat_id, coins), buttons=buttons)
        else:
            await event.reply(msgs['START_MESSAGE'].format(event.chat_id, coins), buttons=buttons)
        
@bot.on(events.CallbackQuery(pattern=b'ajxjao'))
async def numgpv_button(event):
    await event.answer('قسم إدارة الأرقام')
    await event.edit('**📱 قسم إدارة الأرقام** \n\n⚡️ يمكنك التحكم في أرقام البوت بكل سهولة\n🔄 يتم تحديث الأرقام تلقائياً\n✨ اختر الإجراء المناسب:',
                    buttons=[
                        [
                            Button.inline("🎭 📊 عدد أرقام البوت", data="all_of_number", style="success")
                        ],
                        [
                            Button.inline("🎪 ➕ إضافة دولة", data="add_country", style="success"),
                            Button.inline("💎 ➖ حذف دولة", data="del_country", style="danger")
                        ],
                        [
                            Button.inline("✨ ➕ إضافة رقم", data="add", style="primary"),
                            Button.inline("🌟 ➖ حذف رقم", data="del_account", style="danger")
                        ],
                        [
                            Button.inline("🔥 🔙 رجوع", data="admin_panel", style="danger")
                        ]
                    ])

                             
@bot.on(events.CallbackQuery(pattern=b'ajxkho'))
async def nuupv_button(event):
    await event.answer('قسم الإشتراك الإجباري')
    await event.edit('**📢 قسم الإشتراك الإجباري**\n\nاختر الإجراء المناسب:',
                    buttons=[
                        [
                            Button.inline("💎 ➕ إضافة قناة", data="add_force", style="success"),
                            Button.inline("✨ ➖ حذف قناة", data="del_force", style="danger")
                        ],
                        [
                            Button.inline("💎 🔙 رجوع", data="admin_panel", style="danger")
                        ]
                    ])
@bot.on(events.CallbackQuery(pattern=b'aksgl'))
async def nuupv_button(event):
    await event.answer('قسم الإدمنية')
    await event.edit('**👨‍💼 قسم الإدمنية**\n\nاختر الإجراء المناسب:',
                    buttons=[
                        [
                            Button.inline("🎭 ➕ إضافة أدمن", data="add_admin", style="success"),
                            Button.inline("💎 ➖ حذف أدمن", data="del_admin", style="danger")
                        ],
                        [
                            Button.inline("🎊 🔙 رجوع", data="admin_panel", style="danger")
                        ]
                    ])
@bot.on(events.CallbackQuery(pattern=b'ajkofgl'))
async def nuupv_button(event):
    await event.answer('قسم البيع والشراء')
    await event.edit('**💸 قسم البيع والشراء**\n\nاختر الإجراء المناسب:',
                    buttons=[
                        [
                            Button.inline("👑 💰 تغيير سعر الشراء", data="change_price", style="success"),
                            Button.inline("🎊 💵 تغيير سعر البيع", data="change_sell_price", style="success")
                        ],
                        [
                            Button.inline("🔥 🔙 رجوع", data="admin_panel", style="danger")
                        ]
                    ])              
@bot.on(events.CallbackQuery(pattern=b'ajkcoingl'))
async def nuupv_button(event):
    await event.answer('قسم الرصيد')
    await event.edit('**💰 قسم الرصيد**\n\nاختر الإجراء المناسب:',
                    buttons=[
                        [
                            Button.inline("👑 ➕ إضافة رصيد", data="add_coins", style="success"),
                            Button.inline("🌟 ➖ خصم رصيد", data="del_coins", style="danger")
                        ],
                        [
                            Button.inline("👑 🔙 رجوع", data="admin_panel", style="danger")
                        ]
                    ])            

@bot.on(events.CallbackQuery(pattern=b'bbvjls'))
async def nuupv_button(event):
    await event.answer('قسم الحظر')
    await event.edit('**🚫 قسم الحظر**\n\nاختر الإجراء المناسب:',
                    buttons=[
                        [
                            Button.inline("🔥 🚫 حظر شخص", data="ban", style="danger"),
                            Button.inline("🎨 ✅ إلغاء حظر", data="unban", style="success")
                        ],
                        [
                            Button.inline("💎 🔙 رجوع", data="admin_panel", style="danger")
                        ]
                    ])       

@bot.on(events.CallbackQuery(pattern=b'reply_'))
async def reply_button(event):
    data = event.data.decode('utf-8')
    user_id = int(data.split('_')[-1])
    
    async with bot.conversation(admin) as conv:
        await conv.send_message("الرجاء إرسال الرسالة التي تريد إرسالها للعضو.")
        response = await conv.get_response()
        
        await bot.send_message(
            user_id,
            f"رسالة من الدعم: {response.text}"
        )
        await conv.send_message("تم إرسال الرسالة للعضو بنجاح.")

    


@bot.on(events.CallbackQuery(pattern=b'ssart'))
async def withdraw_balance(event):
    user_id = event.chat_id
    user_data = db.get(f"user_{user_id}")
    if user_data["coins"] < 1:
        await event.answer("الحد الأدنى للسحب هو 1$")
        return
    
    async with bot.conversation(user_id) as conv:
        await conv.send_message("📤 أرسل رقم الكاش أو معلومات محفظتك:")
        cash_info = await conv.get_response()
        
        await conv.send_message("💵 أدخل المبلغ الذي تريد سحبه:")
        amount_info = await conv.get_response()
        
        try:
            amount = float(amount_info.text)
            if amount > user_data["coins"]:
                await conv.send_message("رصيدك غير كافٍ لهذا السحب")
                return
            user_data["coins"] -= amount
            db.set(f"user_{user_id}", user_data)
            
            withdraw_message = await bot.send_message(
                admin, 
                f"📤 طلب سحب رصيد جديد\n\n👤 العضو: {user_id}\n📝 معلومات الدفع: {cash_info.text}\n💵 المبلغ: {amount}$",
                buttons=[
                    [Button.inline("✅ تأكيد التحويل", data=f"confirm_withdraw_{user_id}")]
                ]
            )
            
            await conv.send_message(f"✅ تم تقديم طلب السحب بنجاح\n\nالمبلغ: {amount}$\nسيتم المعالجة قريباً")
        except ValueError:
            await conv.send_message("يرجى إدخال مبلغ صحيح")

@bot.on(events.CallbackQuery(pattern=b'confirm_withdraw_'))
async def confirm_withdraw(event):
    data = event.data.decode('utf-8')
    user_id = int(data.split('_')[-1])
    
    await bot.send_message(user_id, "✅ تم تحويل الرصيد بنجاح")
    await event.edit("✅ تم إرسال التأكيد للعضو")

@bot.on(events.CallbackQuery(pattern=b'supper'))
async def support_button(event):
    user_id = event.chat_id
    async with bot.conversation(user_id) as conv:
        await conv.send_message("💬 اكتب رسالتك للدعم الفني:", buttons=[Button.inline("🌟 🔙 رجوع", data="main", style="danger")])
        response = await conv.get_response()
        
        user_info = await client.get_entity(user_id)
        username = f"@{user_info.username}" if user_info.username else "لا يوجد"
        
        await bot.send_message(
            admin,
            f"📩 رسالة دعم جديدة\n\n"
            f"👤 الاسم: <a href='tg://user?id={user_id}'>{user_info.first_name}</a>\n"
            f"🆔 المعرف: {username}\n"
            f"📊 الايدي: {user_id}\n\n"
            f"💭 الرسالة: {response.text}",
            parse_mode="html",
            buttons=[Button.inline("📤 الرد على العضو", data=f"reply_{user_id}")]
        )
        await conv.send_message("✅ تم إرسال رسالتك للدعم الفني")

@bot.on(events.CallbackQuery(pattern=b'reply_'))
async def reply_button(event):
    data = event.data.decode('utf-8')
    user_id = int(data.split('_')[-1])
    
    async with bot.conversation(admin) as conv:
        await conv.send_message("📝 اكتب رسالة الرد:")
        response = await conv.get_response()
        
        await bot.send_message(
            user_id,
            f"📬 رد من الدعم الفني:\n\n{response.text}"
        )
        await conv.send_message("✅ تم إرسال الرد للعضو")
        
@bot.on(events.CallbackQuery(pattern=b'liscgh'))
async def rules_button(event):
    if db.exists("rules_message"):
        rules_message = db.get("rules_message")
    else:
        rules_message = "📜 **قوانين استخدام البوت**\n\n1️⃣ احترام جميع الأعضاء\n2️⃣ عدم إساءة استخدام الخدمات\n3️⃣ الالتزام بالقوانين العامة\n4️⃣ التواصل بلطف مع الدعم الفني"
    
    await event.edit(rules_message, buttons=[Button.inline("💫 🔙 رجوع", data="main", style="danger")])

@bot.on(events.CallbackQuery(pattern=b'edit_rules'))
async def edit_rules_button(event):
    async with bot.conversation(admin) as conv:
        await conv.send_message("📝 الرجاء إرسال رسالة القوانين الجديدة:")
        response = await conv.get_response()
        
        db.set("rules_message", response.text)
        await conv.send_message("✅ تم تحديث رسالة القوانين بنجاح")

                                                                                           
@client.on(events.callbackquery.CallbackQuery())
async def start_lis(event):
    data = event.data.decode('utf-8')
    user_id = event.chat_id
    bans = db.get('bad_guys') if db.exists('bad_guys') else []
    global new_password
    if data == "change_sell_price":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['sell_price']
            if len(row) < 2:
                row.append(Button.inline(text=f" {name}: {price}$", data=f"chs_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f" {name}: {price}$", data=f"chs_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="🔙 رجوع", data="admin_panel")])
        await event.edit("💰 **تغيير أسعار البيع**\n\nاختر الدولة لتعديل سعر البيع:", parse_mode='markdown', buttons=buttons)
        return 
    
    if data.startswith("chs_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"💰 أدخل سعر البيع الجديد لدولة {name}:")
            ch = await x.get_response()
            try:
                price = float(ch.text)
            except:
                await x.send_message("❌ الرجاء إدخال رقم صحيح")
                return
            countries = db.get("countries")
            for i in countries:
                if calling_code == i['calling_code']:
                    i['sell_price'] = price
                    db.set("countries", countries)
                    await x.send_message(f"✅ تم تغيير سعر {name} إلى {price}$")
                    return
            await x.send_message("❌ حدث خطأ أثناء التحديث")
            
    if data == "change_price":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f" {name}: {price}$", data=f"chg_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f" {name}: {price}$", data=f"chg_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="🔙 رجوع", data="admin_panel")])
        await event.edit("💰 **تغيير أسعار الشراء**\n\nاختر الدولة لتعديل سعر الشراء:", parse_mode='markdown', buttons=buttons)
        return 
    
    if data.startswith("chg_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"💰 أدخل السعر الجديد لدولة {name}:")
            ch = await x.get_response()
            try:
                price = float(ch.text)
            except:
                await x.send_message("❌ الرجاء إدخال رقم صحيح")
                return
            countries = db.get("countries")
            for i in countries:
                if calling_code == i['calling_code']:
                    i['price'] = price
                    db.set("countries", countries)
                    await x.send_message(f"✅ تم تغيير سعر {name} إلى {price}$")
                    return
            await x.send_message("❌ حدث خطأ أثناء التحديث")
            
    if data == "add_force":
        async with bot.conversation(event.chat_id) as x:
            force = db.get("force")
            await x.send_message("📢 أرسل معرف أو رابط قناة الإشتراك الإجباري:")
            ch = await x.get_response()
            channel = ch.text.replace('https://t.me/', '').replace('@', '').replace(" ", "")
            if channel in force:
                await x.send_message("⚠️ هذه القناة مضافه بالفعل")
                return
            force.append(channel)
            db.set("force", force)
            await x.send_message("✅ تم إضافة القناة بنجاح")
            return
            
    if data == "del_force":
        async with bot.conversation(event.chat_id) as x:
            force = db.get("force")
            await x.send_message("🗑️ أرسل معرف القناة لحذفها:")
            ch = await x.get_response()
            channel = ch.text.replace('https://t.me/', '').replace('@', '').replace(" ", "")
            if channel not in force:
                await x.send_message("❌ القناة غير موجودة")
                return
            force.remove(channel)
            db.set("force", force)
            await x.send_message("✅ تم حذف القناة بنجاح")
            return
    async with bot.conversation(event.chat_id) as x:
        try:
            force = db.get("force")
            for channel in force:
                result = await client(functions.channels.GetParticipantRequest(
                    channel=channel,
                    participant=user_id
                ))
        except Exception as a:
            await event.edit(f"⚠️ **يجب الإشتراك في القناة**\n\n📢 @{channel}\n\n✅ اشترك ثم أرسل /start")
            return
    if user_id in bans:
        return
    
    if data == "sell":
        await event.edit("⏳ جاري التحضير...")
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("📱 **بيع حساب تليجرام**\n\nأرسل رقم الهاتف مع رمز الدولة:\nمثال: +20123456789")
            ch = await x.get_response()
            phone_number = ch.text.replace("+", "").replace(" ", "")
            if "+" not in ch.text:
                await x.send_message("❌ أرسل الرقم مع علامة +")
            else:
                countries = db.get("countries")
                for code in countries:
                    if ch.text.startswith(code['calling_code']):
                        calling_code = code['calling_code']
                        name = code["name"]
                        sell_price = code["sell_price"]
                        message = f"📋 **تفاصيل البيع**\n\n📞 الرقم: {ch.text}\n🌍 الدولة: {name}\n💰 السعر: {sell_price}$\n\n⚠️ تأكيد عملية البيع؟"
                        buttons = [
                            [
                                Button.inline("👑 ❌ إلغاء", data="back", style="danger"),
                                Button.inline("✅ متابعة", data=f"next_sell:+{phone_number}"),
                            ],
                        ]
                        await event.reply(message, buttons=buttons)
                        return 
                await x.send_message("❌ هذه الدولة غير متاحة للبيع")
                
    if data.startswith("next_sell:"):
        await event.edit("⏳ جاري المعالجة...")
        async with bot.conversation(event.chat_id) as x:
            phone_number = data.split(':')[1]
            countries = db.get("countries")
            for code in countries:
                if phone_number.startswith(code['calling_code']):
                    calling_code = code['calling_code']
                    name = code["name"]
                    sell_price = code["sell_price"]
                    app = TelegramClient(StringSession(), api_id=API_ID, api_hash=API_HASH)
                    await app.connect()
                    password=None
                    try:
                        code = await app.send_code_request(phone_number)
                    except (ApiIdInvalidError):
                        await x.send_message("❌ خطأ في API")
                        return
                    except (PhoneNumberInvalidError):
                        await x.send_message("❌ رقم الهاتف غير صحيح")
                        return
                    await x.send_message("📲 **تم إرسال كود التحقق**\n\nأرسل الكود (مثال: 1 2 3 4 5)")
                    txt = await x.get_response()
                    code = txt.text.replace(" ", "")
                    try:
                        await app.sign_in(phone_number, code, password=None)
                        string_session = app.session.save()
                        data = {"phone_number": phone_number, "two-step": "لا يوجد", "session": string_session}
                        accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
                        accounts.append(data)
                        db.set(f"accounts_{calling_code}", accounts)
                        buttons = [
                            [
                                Button.inline("✅ تحقق", data=f"check:{phone_number}:{calling_code}"),
                            ]
                        ]
                        try:
                            session = MangSession.TELETHON_TO_PYROGRAM(string_session)
                            await enable_password(session, new_password)
                        except Exception as a:
                            print(a)
                            pass
                        await event.reply(f"✅ **تم التحقق بنجاح**\n\n📝 سجل الخروج من جميع الجلسات الأخرى\n💸 ستحصل على: {sell_price}$", buttons=buttons)
                        
                    except (PhoneCodeInvalidError):
                        await x.send_message("❌ كود التحقق خاطئ")
                        return
                    except (PhoneCodeExpiredError):
                        await x.send_message("❌ كود التحقق منتهي")
                        return
                    except (SessionPasswordNeededError):
                        await x.send_message("🔒 أرسل رمز التحقق بخطوتين")
                        txt = await x.get_response()
                        password = txt.text
                        try:
                            await app.sign_in(password=password)
                        except (PasswordHashInvalidError):
                            await x.send_message("❌ رمز التحقق خاطئ")
                            return
                        string_session = app.session.save()
                        data = {"phone_number": phone_number, "two-step": password, "session": string_session}
                        accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
                        accounts.append(data)
                        db.set(f"accounts_{calling_code}", accounts)
                        try:
                            session = MangSession.TELETHON_TO_PYROGRAM(string_session)
                            await change_password(session, password, new_password)
                        except:
                            pass
                        buttons = [
                            [
                                Button.inline("✅ تحقق", data=f"check:{phone_number}:{calling_code}"),
                            ]
                        ]
                        await event.reply(f"✅ **تم التحقق بنجاح**\n\n📝 سجل الخروج من جميع الجلسات الأخرى\n💸 ستحصل على: {sell_price}$", buttons=buttons)
                        
    if data.startswith("check:"):
        await event.edit("⏳ جاري التحقق...")
        async with bot.conversation(event.chat_id) as x:
            phone_number = data.split(':')[1]
            calling_code = data.split(':')[2]
            countries = db.get("countries")
            for code in countries:
                if phone_number.startswith(code['calling_code']):
                    calling_code = code['calling_code']
                    name = code["name"]
                    sell_price = code["sell_price"]
                    accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
                    for i in accounts:
                        if phone_number == i["phone_number"]:
                            ses = i["session"]
                            xx = await count_ses(ses)
                            mkk = isinstance(xx, list)
                            if mkk is False:
                                await x.send_message(f"❌ حدث خطأ، حاول مرة أخرى\n\n{xx}")
                                return
                            xv = len(xx)
                            if xv == 1:
                                message = f"✅ **تم التحقق بنجاح**\n\n📞 الرقم: {phone_number}\n🌍 الدولة: {name}\n💰 المبلغ المضاف: {sell_price}$"
                                user = db.get(f"user_{user_id}")
                                user["coins"] += float(sell_price)
                                db.set(f"user_{user_id}", user)
                                await x.send_message(message)
                                message = f"📊 **بيع جديد**\n\n👤 المشتري: {user_id}\n📞 الرقم: {phone_number}\n💰 السعر: {sell_price}$\n🌍 الدولة: {name}"
                                await client.send_message(admin, message)
                            else:
                                bm = ""
                                for i in xx:
                                    bm += f"• {i}\n"
                                xxx = f"""❌ **فشل التحقق**

⚠️ مازالت هناك جلسات نشطة:

{bm}

🔓 سجل الخروج من جميع الجلسات ثم اضغط تحقق"""
                                buttons = [
                                    [
                                        Button.inline("✅ تحقق", data=f"check:{phone_number}:{calling_code}"),
                                    ]
                                ]
                                await x.send_message(xxx, buttons=buttons)
    if data == "set_trust_channel":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("📊 أرسل معرف قناة إثباتات التسليم:")
            ch = await x.get_response()
            channel = ch.text.replace('https://t.me/', '').replace('@', '').replace(" ", "")
            try:
                message = "✅ تم تفعيل القناة بنجاح"
                await client.send_message(channel, message)
            except:
                message = "❌ تأكد من رفع البوت كأدمن في القناة"
                await x.send_message(message)
                return
            message = "✅ تم تفعيل القناة بنجاح"
            await x.send_message(message)
            db.set("trust_channel", channel)
        
    if data == "transfer":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(msgs['TRANSFER_MESSAGE'])
            iii = await x.get_response()
            try:
                id = int(iii.text)
            except:
                return await x.send_message("❌ أرسل ايدي صحيح")
            if user_id == id:
                return await x.send_message("❌ لا يمكن التحويل لنفسك")
            if not db.exists(f"user_{id}"):
                return await x.send_message("❌ المستخدم غير موجود")
            less = db.get("transfer_minimum") if db.exists("transfer_minimum") else 5
            await x.send_message(f"💸 **تحويل الرصيد**\n\nأدخل المبلغ (الحد الأدنى: {less}$)")
            cou = await x.get_response()
            try:
                count = float(cou.text)
            except:
                return await x.send_message("❌ أرسل مبلغ صحيح")
            info = db.get(f"user_{user_id}")
            count += 0.02 * float(cou.text)
            if info['coins'] < count:
                return await x.send_message("❌ رصيد غير كافٍ")
            if less > count:
                return await x.send_message(f"❌ الحد الأدنى: {less}$")
            info['coins'] -= count 
            db.set(f"user_{user_id}", info)
            acc = db.get(f"user_{id}")
            acc['coins'] += float(cou.text)
            db.set(f"user_{id}", acc)
            await client.send_message(id, f"📥 **تحويل وارد**\n\n💰 المبلغ: {float(cou.text)}$\n👤 المرسل: {user_id}")
            await x.send_message(f"📤 **تحويل صادر**\n\n💰 المبلغ: {float(cou.text)}$\n👤 المستلم: {id}")
            await client.send_message(admin, f"💸 **عملية تحويل**\n\n👤 المرسل: {user_id}\n👤 المستلم: {id}\n💰 المبلغ: {cou.text}$\n📊 العمولة: {0.02 * float(cou.text)}$")
    if data == "add_coins":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("👤 أرسل ايدي المستخدم:")
            id = await x.get_response()
            if not db.exists(f"user_{id.text}"):
                await x.send_message("❌ المستخدم غير موجود")
                return
            info = db.get(f"user_{id.text}")
            await x.send_message(f"📊 **معلومات المستخدم**\n\n🆔 الايدي: {id.text}\n💰 الرصيد الحالي: {info['coins']}$\n\n💵 أدخل المبلغ للإضافة:")
            count = await x.get_response()
            try:
                info['coins'] += float(count.text)
            except:
                await x.send_message("❌ أرسل مبلغ صحيح")
                return
            db.set(f"user_{id.text}", info)
            await x.send_message(f"✅ تمت الإضافة\n💰 الرصيد الجديد: {info['coins']}$")
            message = f"💰 **إضافة رصيد**\n\n✅ تم إضافة {count.text}$\n📊 رصيدك الحالي: {info['coins']}$"
            await client.send_message(int(id.text), message)
            return 
    if data == "del_coins":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("👤 أرسل ايدي المستخدم:")
            id = await x.get_response()
            if not db.exists(f"user_{id.text}"):
                await x.send_message("❌ المستخدم غير موجود")
                return
            info = db.get(f"user_{id.text}")
            await x.send_message(f"📊 **معلومات المستخدم**\n\n🆔 الايدي: {id.text}\n💰 الرصيد الحالي: {info['coins']}$\n\n💸 أدخل المبلغ للخصم:")
            count = await x.get_response()
            try:
                info['coins'] -= float(count.text)
            except:
                await x.send_message("❌ أرسل مبلغ صحيح")
                return
            db.set(f"user_{id.text}", info)
            await x.send_message(f"✅ تم الخصم\n💰 الرصيد الجديد: {info['coins']}$")
            return
        
    if data == "ban":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("🚫 أرسل ايدي المستخدم للحظر:")
            id = await x.get_response()
            try:
                i = int(id.text)
            except:
                await x.send_message("❌ أرسل ايدي صحيح")
                return
            bans = db.get('bad_guys') if db.exists('bad_guys') else []
            if id.text in bans:
                await x.send_message("⚠️ المستخدم محظور بالفعل")
                return
            bans.append(id.text)
            db.set("bad_guys", bans)
            await x.send_message("✅ تم الحظر بنجاح")
            return 
    
    if data == "unban":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("✅ أرسل ايدي المستخدم لإلغاء الحظر:")
            id = await x.get_response()
            try:
                i = int(id.text)
            except:
                await x.send_message("❌ أرسل ايدي صحيح")
                return
            bans = db.get('bad_guys') if db.exists('bad_guys') else []
            if id.text not in bans:
                await x.send_message("⚠️ المستخدم غير محظور")
                return
            bans.remove(id.text)
            db.set("bad_guys", bans)
            await x.send_message("✅ تم إلغاء الحظر بنجاح")
            return 
    
    if data == "all_of_number":
        countries = db.get("countries")
        count = 0
        keys = db.keys("accounts_%")
        for i in keys:
            count += len(db.get(i[0]))
                          
        return await event.answer(f"📊 عدد الأرقام: {count}", alert=True)
        
    if data == "main":
        coins = db.get(f"user_{user_id}")["coins"]
        buttons = [
            [
                Button.inline("🎯 🛒 شراء رقم", data="buy", style="success"),
            ],
            [
                Button.inline("💎 💳 سحب رصيد", data="ssart", style="success"),
                Button.inline("🎪 🔄 تحويل رصيد", data="transfer", style="success"),
            ],
            [
                Button.inline("🌟 👨‍💻 الدعم الفني", data="supper", style="primary"),
                Button.inline("⚡ 📋 القوانين", data="liscgh", style="success"),
            ],
            [
                Button.inline("⚡ 💱 بيع حساب", data="sell", style="success"),
            ]
        ]
        await event.edit(msgs['START_MESSAGE'].format(event.chat_id, coins), parse_mode='markdown', buttons=buttons)
        return
        
    if data == "admin_panel":
        keyboard = [
            [
                Button.inline("💫 ⚙️ إعدادات الأرقام", data="ajxjao", style="success"),
            ],
            [
                Button.inline("💎 📢 الإشتراك الإجباري", data="ajxkho", style="success"), 
                Button.inline("🔥 👨‍💼 قسم الإدمنية", data="aksgl", style="primary"), 
            ],
            [
                Button.inline("💫 💸 قسم البيع والشراء", data="ajkofgl", style="primary"),
            ],
            [
                Button.inline("🎯 💰 قسم الرصيد", data="ajkcoingl", style="success"), 
                Button.inline("🔥 🚫 قسم الحظر", data="bbvjls", style="danger"), 
            ],
            [
                Button.inline("🎯 📊 قناة إثباتات التسليم", data="set_trust_channel", style="success"),
            ],
        ]
        await event.edit(msgs['ADMIN_MESSAGE'], buttons=keyboard)
        return 
        
    if data == "buy" or data == "back":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f" {name}: {price}$", data=f"countries_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f" {name}: {price}$", data=f"countries_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="🔙 رجوع", data="main")])
        await event.edit(msgs['COUNTRY_LIST'], parse_mode='markdown', buttons=buttons)
        return
        
    if data == "del_account":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f" {name}: {price}$", data=f"show_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f" {name}: {price}$", data=f"show_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="🔙 رجوع", data="admin_panel")])
        await event.edit("🗑️ اختر الدولة لحذف رقم منها:", parse_mode='markdown', buttons=buttons)
        return
    
    if data.startswith("show_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        if accounts == []:
           return await event.answer("❌ لا توجد حسابات", alert=True)
        text = ""
        buttons = [[Button.inline(f"{count}: +{i['phone_number']}", data=f"v:{i['phone_number']}:{calling_code}:{name}:{price}")] for count, i in enumerate(accounts, 1)]
        buttons.append([Button.inline("🔙 رجوع", data=f"del_account")])
        await event.edit(f"📋 حسابات {name}:", parse_mode='markdown', buttons=buttons)
        return
        
    if data.startswith("v:"):
        phone_number = data.split(':')[1]
        calling_code = data.split(':')[2]
        name = data.split(':')[3]
        price = data.split(':')[4]
        info = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        for i in info:
            if i['phone_number'] == phone_number:
                text = f"📞 **معلومات الحساب**\n\n📱 الرقم: `+{i['phone_number']}`\n🔒 التحقق بخطوتين: `{i['two-step']}`\n\nاختر الإجراء المناسب:"
        keyboard = [
            [
                Button.inline("📲 الحصول على الكود", data=f"get:{phone_number}:{calling_code}:{name}:{price}"),
            ],
            [
            Button.inline(f"❌ حذف +{phone_number}", data=f"del:{phone_number}:{calling_code}:{name}"), 
            ],
            [
            Button.inline("🔙 رجوع", data=f"show_{calling_code}_{name}_{price}")
            ]
        ]
        await event.edit(text, parse_mode='markdown', buttons=keyboard)
        return
        
    if data.startswith("del:"):
        phone_number = data.split(':')[1]
        calling_code = data.split(':')[2]
        name = data.split(':')[3]
        text = f"⚠️ **تأكيد الحذف**\n\n📱 الرقم: `+{phone_number}`\n\nهل أنت متأكد من الحذف؟"
        keyboard = [
            [
            Button.inline("🔙 رجوع", data=f"v:{phone_number}:{calling_code}:{name}"),
            Button.inline("❌ حذف", data=f"del_done:{phone_number}:{calling_code}:{name}")
            ]
        ]
        await event.edit(text, parse_mode='markdown', buttons=keyboard)
        return
        
    if data.startswith("del_done:"):
        phone_number = data.split(':')[1]
        calling_code = data.split(':')[2]
        name = data.split(':')[3]
        keyboard = [
            [
            Button.inline("✨ 🔙 رجوع", data="admin_panel", style="danger")
            ]
        ]
        
        info = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        for i in info:
            if i['phone_number'] == phone_number:
                info.remove(i)
                db.set(f"accounts_{calling_code}", info)
                await event.edit(f"✅ تم حذف الرقم `+{phone_number}` من {name}", parse_mode='markdown', buttons=keyboard)
                return
        await event.edit(f"❌ فشل حذف الرقم", parse_mode='markdown', buttons=keyboard)
        return 
        
    if data == "add":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f" {name}: {price}$", data=f"rig_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f" {name}: {price}$", data=f"rig_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="🔙 رجوع", data="main")])
        await event.edit("➕ اختر الدولة لإضافة رقم:", parse_mode='markdown', buttons=buttons)
        return 
        
    if data.startswith("rig_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"📱 أرسل رقم الهاتف لدولة {name} (مع +)")
            txt = await x.get_response()
            phone_number = txt.text.replace("+", "").replace(" ", "")
            app = TelegramClient(StringSession(), api_id=API_ID, api_hash=API_HASH)
            await app.connect()
            password=None
            try:
                code = await app.send_code_request(phone_number)
            except (ApiIdInvalidError):
                await x.send_message("❌ خطأ في API")
                return
            except (PhoneNumberInvalidError):
                await x.send_message("❌ رقم غير صحيح")
                return
            await x.send_message("📲 أرسل كود التحقق (مثال: 1 2 3 4 5)")
            txt = await x.get_response()
            code = txt.text.replace(" ", "")
            try:
                await app.sign_in(phone_number, code, password=None)
                string_session = app.session.save()
                data = {"phone_number": phone_number, "two-step": "AmmarKing", "session": string_session}
                accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
                accounts.append(data)
                db.set(f"accounts_{calling_code}", accounts)
                await x.send_message(f"✅ تمت الإضافة بنجاح\n📊 عدد الأرقام: {len(accounts)}")
            except (PhoneCodeInvalidError):
                await x.send_message("❌ كود خاطئ")
                return
            except (PhoneCodeExpiredError):
                await x.send_message("❌ كود منتهي")
                return
            except (SessionPasswordNeededError):
                await x.send_message("🔒 أرسل رمز التحقق بخطوتين")
                txt = await x.get_response()
                password = txt.text
                try:
                    await app.sign_in(password=password)
                except (PasswordHashInvalidError):
                    await x.send_message("❌ رمز خاطئ")
                    return
                string_session = app.session.save()
                data = {"phone_number": phone_number, "two-step": password, "session": string_session}
                accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
                accounts.append(data)
                db.set(f"accounts_{calling_code}", accounts)
                await x.send_message(f"✅ تمت الإضافة بنجاح\n📊 عدد الأرقام: {len(accounts)}")
        return 
        
    if data == 'zip_all':
        folder_path = f"./database"
        zip_file_name = f"database.zip"
        zip_file_nam = f"database"
        try:
            shutil.make_archive(zip_file_nam, 'zip', folder_path)
            with open(zip_file_name, 'rb') as zip_file:
                await client.send_file(user_id, zip_file, attributes=[DocumentAttributeFilename(file_name="database.zip")])
            os.remove(zip_file_name)
        except Exception as a:
            print(a)
    if data.startswith("get:"):
        phone_number = data.split(':')[1]
        calling_code = data.split(':')[2]
        name = data.split(':')[3]
        price = data.split(':')[4]
        info = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        keyboard = [
            [
            Button.inline("🔥 🔙 رجوع", data="main", style="danger")
            ]
        ]
        for i in info:
            if i['phone_number'] == phone_number:
                code = await get_code(i['session'])
                try:
                    cd = int(code)
                    text = f"✅ **تم الحصول على الكود**\n\n📱 الرقم: `+{i['phone_number']}`\n🔒 التحقق بخطوتين: `{i['two-step']}`\n🔢 الكود: `{code}`"
                    now = datetime.datetime.now()
                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    bots = await client.get_me()
                    user_info = await client.get_entity(bots.id)
                    keyboards = [
                        [
                            KeyboardButtonUrl("🛒 شراء حساب تليجرام", url=f"https://t.me/{user_info.username}"),
                        ]
                    ]
                    if db.exists("trust_channel"):
                        await client.send_message(
                            db.get("trust_channel"),
                            msgs['TRUST_MESSAGE'].format(
                                name,
                                f"{phone_number}"[:8],
                                price,
                                f"{user_id}"[:8],
                                code,
                                current_time
                            ),
                            buttons=keyboards,
                            parse_mode="markdown"
                        )
                    info.remove(i)
                    db.set(f"accounts_{calling_code}", info)
                except Exception as a:
                    print(a)
                    text = f"❌ **لم يتم الحصول على الكود**\n\n📱 الرقم: `+{i['phone_number']}`\n🔒 التحقق بخطوتين: `{i['two-step']}`"
                async with bot.conversation(event.chat_id) as x:
                    await x.send_message(text, buttons=keyboard)
        return 
    if data == "add_country":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("🌍 أرسل اسم الدولة:\nمثال: مصر 🇪🇬")
            name = await x.get_response()
            await x.send_message(f"🔢 أرسل رمز الدولة لـ {name.text}:\nمثال: +20")
            calling_code = await x.get_response()
            await x.send_message(f"💰 أرسل سعر الشراء ($):")
            price = await x.get_response()
            try:
                am = float(price.text)
            except:
                await x.send_message("❌ أرسل رقم صحيح")
                return 
            await x.send_message(f"💵 أرسل سعر البيع لدولة {name.text}:")
            sell_price = await x.get_response()
            countries = db.get("countries")
            countries.append({"name": name.text, "calling_code": calling_code.text, "price": price.text, "sell_price": sell_price.text})
            db.set("countries", countries)
            await x.send_message(f"✅ تمت الإضافة\n📊 عدد الدول: {len(countries)}")
            return 
    
    if data == "del_country":
        countries = db.get("countries")
        buttons = []
        row = []
        for code in countries:
            calling_code = code['calling_code']
            name = code['name']
            price = code['price']
            if len(row) < 2:
                row.append(Button.inline(text=f" {name}: {price}$", data=f"delete_{calling_code}_{name}_{price}"))
            else:
                buttons.append(row)
                row = [Button.inline(text=f" {name}: {price}$", data=f"delete_{calling_code}_{name}_{price}")]
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline(text="🔙 رجوع", data="main")])
        await event.edit("🗑️ اختر الدولة للحذف:", parse_mode='markdown', buttons=buttons)
    
    if data.startswith("delete_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        countries = db.get("countries")
        buttons = [
            [
            Button.inline("💫 🔙 رجوع", data="del_country", style="danger")
            ]
        ]
        for data in countries:
            if data["calling_code"] == calling_code:
                countries.remove(data)
                await event.edit("✅ تم الحذف بنجاح", parse_mode='markdown', buttons=buttons)
                db.set("countries", countries)
                return
        await event.edit("❌ فشل الحذف", parse_mode='markdown', buttons=buttons)
        
    if data.startswith("countries_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        coins = db.get(f"user_{user_id}")['coins']
        if float(coins) < float(price):
            return await event.answer("❌ رصيدك غير كافٍ", alert=True)
        accounts = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        if accounts == []:
            return await event.answer("❌ لا توجد أرقام متاحة", alert=True)
        keyboard = [
            [
                Button.inline("🎨 ❌ إلغاء", data="back", style="danger"),
                Button.inline("✅ تأكيد", data=f"buy_{calling_code}_{name}_{price}")
            ],
        ]
        await event.edit(msgs['BUY_MESSAGE'].format(name, price), parse_mode='markdown', buttons=keyboard)
        return
        
    if data.startswith("buy_"):
        calling_code = data.split('_')[1]
        name = data.split('_')[2]
        price = data.split('_')[3]
        acc = db.get(f"user_{user_id}")
        acc['coins'] -= float(price)
        db.set(f"user_{user_id}", acc)
        info = db.get(f"accounts_{calling_code}") if db.exists(f"accounts_{calling_code}") else []
        i = random.choice(info)
        text = f"🎉 **تم الشراء بنجاح**\n\n📱 الرقم: `+{i['phone_number']}`\n🔒 التحقق بخطوتين: `{i['two-step']}`\n\n📲 اضغط للحصول على الكود:"
        keyboard = [
            [
                Button.inline("📲 الحصول على الكود", data=f"get:{i['phone_number']}:{calling_code}:{name}:{price}"),
            ]
        ]
        await event.edit(text, buttons=keyboard)
    if data == "add_admin":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("👨‍💼 أرسل ايدي العضو لرفعه أدمن:")
            name = await x.get_response()
            try:
                id = int(name.text)
            except:
                return await x.send_message("❌ أرسل ايدي صحيح")
            admins = db.get("admins")
            if id in admins:
                return await x.send_message("⚠️ العضو أدمن بالفعل")
            admins.append(id)
            db.set("admins", admins)
            await x.send_message("✅ تم الرفع بنجاح")
            
    if data == "del_admin":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("🗑️ أرسل ايدي الأدمن للحذف:")
            name = await x.get_response()
            try:
                id = int(name.text)
            except:
                return await x.send_message("❌ أرسل ايدي صحيح")
            admins = db.get("admins")
            if id not in admins:
                return await x.send_message("❌ العضو ليس أدمن")
            admins.remove(id)
            db.set("admins", admins)
            await x.send_message("✅ تم الحذف بنجاح")

async def count_ses(session):
    api_hash='d00b2a9f2c9b17ee7b25cbac6ef9f1bf'
    api_id=27140514
    try:
        app = TelegramClient(StringSession(session), api_id=API_ID, api_hash=API_HASH)
        await app.connect()
        try:
            resulkt = await app(functele.auth.ResetAuthorizationsRequest())
        except:
            pass
        unauthorized_attempts = await app(GetAuthorizationsRequest())
        listt = []
        for i in unauthorized_attempts.authorizations:
        	mod = listt.append(i.device_model)
        return listt
    except Exception as a:
        print(str(a))
        return str(a)
        
client.run_until_disconnected()