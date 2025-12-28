import asyncio
import aiohttp
import random
import json
import requests
import re
import time
import os
from datetime import datetime
import telebot
from telebot import types
import threading


TELEGRAM_TOKEN = ("7634220547:AAEQT8ImDoiTmX0tJn25NEz8IJ4xaNs8cYQ")
ADMIN_IDS = [6806810777]  
PROMPTS_CHANNEL_LINK = "https://t.me/NanoBananaAI1"
bot = telebot.TeleBot(TELEGRAM_TOKEN)


ACCOUNTS_FILE = "accounts/accounts_data.json"
USERS_FILE = "users/users_data.json"
CHANNELS_FILE = "channels/channels_data.json"
os.makedirs("accounts", exist_ok=True)
os.makedirs("users", exist_ok=True)
os.makedirs("channels", exist_ok=True)


LANGUAGES = {
    'ar': 'العربية',
    'en': 'English', 
    'fa': 'فارسی'
}

MESSAGES = {
    'ar': {
        'welcome': "🎨 مرحبًا بك في بوت إنشاء وتعديل الصور باستخدام NanoBanana AI!",
        'choose_language': "🌐 الرجاء اختيار اللغة / Please choose language / لطفا زبان را انتخاب کنید",
        'select_option': "اختر أحد الخيارات:",
        'create_image': "🖼️ إنشاء صورة جديدة",
        'edit_image': "✏️ تعديل صورة",
        'edit_multiple': "🖼️✏️ تعديل ودمج عدة صور",
        'send_prompt': "✍️ الرجاء إرسال وصف الصورة المطلوبة:",
        'prompt_too_short': "❌ الوصف قصير جدًا. الرجاء إدخال وصف مفصل.",
        'processing': "⏳ تم إرسال طلبك، يرجى الانتظار قليلاً...",
        'send_image': "📤 الرجاء إرسال الصورة التي تريد تعديلها:",
        'no_image': "❌ لم يتم إرسال صورة. الرجاء المحاولة مرة أخرى.",
        'image_received': "✅ تم استلام الصورة.\n✍️ الرجاء إرسال وصف التعديل المطلوب:",
        'send_images': "📤 الرجاء إرسال الصور التي تريد دمجها وتعديلها (حتى 5 صور):",
        'images_received': "✅ تم استلام {} صور بنجاح.\n📤 أرسل صورة أخرى أو انقر ✅ تم للبدء في التعديل.",
        'send_edit_prompt': "✍️ الآن أرسل وصف التعديل المطلوب على جميع الصور:",
        'processing_images': "🔄 جاري معالجة وتعديل الصور...",
        'image_created': "✅ تم إنشاء الصورة بنجاح!",
        'image_edited': "✅ تم تعديل الصورة بنجاح!",
        'images_edited': "✅ تم تعديل ودمج الصور بنجاح!",
        'error': "❌ حدث خطأ. الرجاء المحاولة لاحقًا.",
        'admin_panel': "👑 لوحة الإدارة",
        'back': "↩️ رجوع",
        'stats': "📊 إحصائيات البوت",
        'accounts_list': "📋 قائمة الحسابات",
        'broadcast': "📢 إرسال إشعار للجميع",
        'enter_broadcast': "✍️ أدخل الرسالة للإرسال:",
        'broadcast_sent': "✅ تم إرسال الرسالة إلى {} مستخدم.",
        'total_users': "👥 إجمالي المستخدمين: {}",
        'total_accounts': "📧 إجمالي الحسابات: {}",
        'accounts_per_user': "📊 متوسط الحسابات لكل مستخدم: {:.1f}",
        'enter_user_id': "🆔 أدخل معرف المستخدم:",
        'user_info': "👤 معلومات المستخدم",
        'user_id': "المعرف: {}",
        'user_lang': "اللغة: {}",
        'user_accounts': "عدد الحسابات: {}",
        'user_requests': "عدد الطلبات: {}",
        'user_not_found': "❌ المستخدم غير موجود.",
        'subscription_required': "⚠️ الاشتراك إجباري!\n\nيجب عليك الانضمام إلى القنوات التالية لاستخدام البوت:",
        'join_channels': "📢 انضم إلى القنوات",
        'check_subscription': "✅ التحقق من الاشتراك",
        'channels_management': "📢 إدارة القنوات",
        'add_channel': "➕ إضافة قناة",
        'remove_channel': "➖ إزالة قناة",
        'channels_list': "📋 قائمة القنوات",
        'enter_channel': "🔗 أرسل رابط أو يوزر القناة:",
        'channel_added': "✅ تمت إضافة القناة بنجاح!",
        'channel_removed': "✅ تمت إزالة القناة بنجاح!",
        'select_channel_to_remove': "📝 اختر القناة التي تريد إزالتها:",
        'no_channels': "📭 لا توجد قنوات مضافة.",
        'forward_message': "📤 أرسل لي رسالة من القناة (يجب أن تكون القناة خاصة)",
        'message_forwarded': "✅ تم استلام الرسالة. جاري إضافة القناة...",
        'must_be_admin': "⚠️ يجب أن يكون البوت مسؤولاً في القناة!",
        'subscription_verified': "✅ تم التحقق من اشتراكاتك! يمكنك الآن استخدام البوت.",
        'not_subscribed': "❌ لم تنضم بعد إلى جميع القنوات المطلوبة.",
        'admin_only': "❌ هذا الأمر للمشرفين فقط!",
        'add_another_image': "➕ إضافة صورة أخرى",
        'done_adding': "✅ تم الانتهاء",
        'max_images_reached': "⚠️ وصلت للحد الأقصى (5 صور). انقر ✅ تم للمتابعة.",
        'bot_owner_contact': "👑 تواصل مع المطور",
        'change_language': "🌐 تغيير اللغة",
        'prompts_button': "💡 البروميتات"
    },
    'en': {
        'welcome': "🎨 Welcome to NanoBanana AI Image Creation & Editing Bot!",
        'choose_language': "🌐 Please choose language / الرجاء اختيار اللغة / لطفا زبان را انتخاب کنید",
        'select_option': "Choose an option:",
        'create_image': "🖼️ Create New Image",
        'edit_image': "✏️ Edit Image",
        'edit_multiple': "🖼️✏️ Edit & Merge Multiple Images",
        'send_prompt': "✍️ Please send the image description:",
        'prompt_too_short': "❌ Description is too short. Please enter a detailed description.",
        'processing': "⏳ Your request has been sent, please wait a moment...",
        'send_image': "📤 Please send the image you want to edit:",
        'no_image': "❌ No image sent. Please try again.",
        'image_received': "✅ Image received.\n✍️ Please send the edit description:",
        'send_images': "📤 Please send the images you want to merge and edit (up to 5 images):",
        'images_received': "✅ Received {} images successfully.\n📤 Send another image or click ✅ Done to start editing.",
        'send_edit_prompt': "✍️ Now send the edit description for all images:",
        'processing_images': "🔄 Processing and editing images...",
        'image_created': "✅ Image created successfully!",
        'image_edited': "✅ Image edited successfully!",
        'images_edited': "✅ Images edited and merged successfully!",
        'error': "❌ An error occurred. Please try again later.",
        'admin_panel': "👑 Admin Panel",
        'back': "↩️ Back",
        'stats': "📊 Bot Statistics",
        'accounts_list': "📋 Accounts List",
        'broadcast': "📢 Broadcast Message",
        'enter_broadcast': "✍️ Enter message to broadcast:",
        'broadcast_sent': "✅ Message sent to {} users.",
        'total_users': "👥 Total Users: {}",
        'total_accounts': "📧 Total Accounts: {}",
        'accounts_per_user': "📊 Average accounts per user: {:.1f}",
        'enter_user_id': "🆔 Enter user ID:",
        'user_info': "👤 User Information",
        'user_id': "ID: {}",
        'user_lang': "Language: {}",
        'user_accounts': "Accounts count: {}",
        'user_requests': "Requests count: {}",
        'user_not_found': "❌ User not found.",
        'subscription_required': "⚠️ Subscription Required!\n\nYou must join the following channels to use the bot:",
        'join_channels': "📢 Join Channels",
        'check_subscription': "✅ Check Subscription",
        'channels_management': "📢 Channels Management",
        'add_channel': "➕ Add Channel",
        'remove_channel': "➖ Remove Channel",
        'channels_list': "📋 Channels List",
        'enter_channel': "🔗 Send channel link or username:",
        'channel_added': "✅ Channel added successfully!",
        'channel_removed': "✅ Channel removed successfully!",
        'select_channel_to_remove': "📝 Select channel to remove:",
        'no_channels': "📭 No channels added.",
        'forward_message': "📤 Forward me a message from the channel (channel must be private)",
        'message_forwarded': "✅ Message received. Adding channel...",
        'must_be_admin': "⚠️ Bot must be admin in the channel!",
        'subscription_verified': "✅ Subscription verified! You can now use the bot.",
        'not_subscribed': "❌ You haven't joined all required channels.",
        'admin_only': "❌ This command is for admins only!",
        'add_another_image': "➕ Add Another Image",
        'done_adding': "✅ Done",
        'max_images_reached': "⚠️ Reached maximum (5 images). Click ✅ Done to continue.",
        'bot_owner_contact': "👑 Contact Developer",
        'change_language': "🌐 Change Language",
        'prompts_button': "💡 Prompts Library"
    },
    'fa': {
        'welcome': "🎨 به ربات ایجاد و ویرایش تصاویر NanoBanana AI خوش آمدید!",
        'choose_language': "🌐 لطفا زبان را انتخاب کنید / Please choose language / الرجاء اختيار اللغة",
        'select_option': "یک گزینه را انتخاب کنید:",
        'create_image': "🖼️ ایجاد تصویر جدید",
        'edit_image': "✏️ ویرایش تصویر",
        'edit_multiple': "🖼️✏️ ویرایش و ادغام چندین تصویر",
        'send_prompt': "✍️ لطفا توضیحات تصویر را ارسال کنید:",
        'prompt_too_short': "❌ توضیحات بسیار کوتاه است. لطفا توضیحات مفصلی وارد کنید.",
        'processing': "⏳ درخواست شما ارسال شد، لطفا کمی منتظر بمانید...",
        'send_image': "📤 لطفا تصویری که می‌خواهید ویرایش کنید را ارسال کنید:",
        'no_image': "❌ تصویری ارسال نشد. لطفا مجددا تلاش کنید.",
        'image_received': "✅ تصویر دریافت شد.\n✍️ لطفا توضیحات ویرایش را ارسال کنید:",
        'send_images': "📤 لطفا تصاویری که می‌خواهید ادغام و ویرایش کنید را ارسال کنید (حداکثر ۵ تصویر):",
        'images_received': "✅ {} تصویر با موفقیت دریافت شد.\n📤 تصویر دیگری ارسال کنید یا برای شروع ویرایش کلیک کنید.",
        'send_edit_prompt': "✍️ حالا توضیحات ویرایش برای تمام تصاویر را ارسال کنید:",
        'processing_images': "🔄 در حال پردازش و ویرایش تصاویر...",
        'image_created': "✅ تصویر با موفقیت ایجاد شد!",
        'image_edited': "✅ تصویر با موفقیت ویرایش شد!",
        'images_edited': "✅ تصاویر با موفقیت ویرایش و ادغام شدند!",
        'error': "❌ خطایی رخ داد. لطفا بعدا تلاش کنید.",
        'admin_panel': "👑 پنل مدیریت",
        'back': "↩️ بازگشت",
        'stats': "📊 آمار ربات",
        'accounts_list': "📋 لیست حساب‌ها",
        'broadcast': "📢 ارسال پیام همگانی",
        'enter_broadcast': "✍️ پیام برای ارسال همگانی را وارد کنید:",
        'broadcast_sent': "✅ پیام به {} کاربر ارسال شد.",
        'total_users': "👥 کل کاربران: {}",
        'total_accounts': "📧 کل حساب‌ها: {}",
        'accounts_per_user': "📊 میانگین حساب‌ها برای هر کاربر: {:.1f}",
        'enter_user_id': "🆔 شناسه کاربر را وارد کنید:",
        'user_info': "👤 اطلاعات کاربر",
        'user_id': "شناسه: {}",
        'user_lang': "زبان: {}",
        'user_accounts': "تعداد حساب‌ها: {}",
        'user_requests': "تعداد درخواست‌ها: {}",
        'user_not_found': "❌ کاربر یافت نشد.",
        'subscription_required': "⚠️ اشتراک اجباری!\n\nبرای استفاده از ربات باید در کانال‌های زیر عضو شوید:",
        'join_channels': "📢 عضویت در کانال‌ها",
        'check_subscription': "✅ بررسی اشتراک",
        'channels_management': "📢 مدیریت کانال‌ها",
        'add_channel': "➕ افزودن کانال",
        'remove_channel': "➖ حذف کانال",
        'channels_list': "📋 لیست کانال‌ها",
        'enter_channel': "🔗 لینک یا نام کاربری کانال را ارسال کنید:",
        'channel_added': "✅ کانال با موفقیت افزوده شد!",
        'channel_removed': "✅ کانال با موفقیت حذف شد!",
        'select_channel_to_remove': "📝 کانال مورد نظر برای حذف را انتخاب کنید:",
        'no_channels': "📭 هیچ کانالی افزوده نشده است.",
        'forward_message': "📤 یک پیام از کانال برای من فوروارد کنید (کانال باید خصوصی باشد)",
        'message_forwarded': "✅ پیام دریافت شد. در حال افزودن کانال...",
        'must_be_admin': "⚠️ ربات باید مدیر کانال باشد!",
        'subscription_verified': "✅ اشتراک تایید شد! اکنون می‌توانید از ربات استفاده کنید.",
        'not_subscribed': "❌ شما در همه کانال‌های مورد نیاز عضو نشده‌اید.",
        'admin_only': "❌ این دستور فقط برای مدیران است!",
        'add_another_image': "➕ افزودن تصویر دیگر",
        'done_adding': "✅ انجام شد",
        'max_images_reached': "⚠️ به حداکثر رسید (۵ تصویر). برای ادامه کلیک کنید.",
        'bot_owner_contact': "👑 تماس با توسعه دهنده",
        'change_language': "🌐 تغییر زبان",
        'prompts_button': "💡 پرامپت‌ها"
    }
}


def load_data(file_path, default=[]):
    if not os.path.exists(file_path):
        return default
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_accounts():
    return load_data(ACCOUNTS_FILE, [])

def save_accounts(accounts):
    save_data(ACCOUNTS_FILE, accounts)

def load_users():
    return load_data(USERS_FILE, [])

def save_users(users):
    save_data(USERS_FILE, users)

def load_channels():
    return load_data(CHANNELS_FILE, [])

def save_channels(channels):
    save_data(CHANNELS_FILE, channels)

def get_user(user_id):
    users = load_users()
    for user in users:
        if user.get('id') == user_id:
            return user
    return None

def save_user(user_data):
    users = load_users()
    user_id = user_data['id']
    
    for i, user in enumerate(users):
        if user.get('id') == user_id:
            users[i] = user_data
            break
    else:
        users.append(user_data)
    
    save_users(users)

def get_user_language(user_id):
    user = get_user(user_id)
    if user and 'language' in user:
        return user['language']
    return 'ar'

def get_message(user_id, key):
    lang = get_user_language(user_id)
    return MESSAGES[lang].get(key, key)


user_sessions = {}

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    return user_sessions[user_id]

def clear_user_session(user_id):
    if user_id in user_sessions:
        session = user_sessions[user_id]
        if 'temp_images' in session:
            for img_path in session['temp_images']:
                if os.path.exists(img_path):
                    os.remove(img_path)
        del user_sessions[user_id]


def check_user_subscription(user_id):
    channels = load_channels()
    if not channels:
        return True, []
    
    not_joined = []
    
    for channel in channels:
        channel_id = channel.get('channel_id')
        chat_id = channel.get('chat_id')
        
        if channel_id:
            try:
                
                chat_member = bot.get_chat_member(chat_id, user_id)
                if chat_member.status not in ['member', 'administrator', 'creator']:
                    not_joined.append(channel)
            except Exception as e:
                not_joined.append(channel)
    
    return len(not_joined) == 0, not_joined

def show_subscription_required(user_id, not_joined_channels):
    user_lang = get_user_language(user_id)
    
    message = get_message(user_id, 'subscription_required') + "\n\n"
    
    for i, channel in enumerate(not_joined_channels, 1):
        title = channel.get('title', 'Unknown Channel')
        username = channel.get('username')
        
        if username:
            link = f"https://t.me/{username}" if not username.startswith('@') else f"https://t.me/{username[1:]}"
        else:
            link = channel.get('invite_link', '#')
        
        message += f"{i}. {title}\n"
        message += f"   🔗 {link}\n\n"
    
    markup = types.InlineKeyboardMarkup()
    
    
    for channel in not_joined_channels:
        username = channel.get('username')
        if username:
            channel_link = username if username.startswith('@') else f"@{username}"
            markup.add(types.InlineKeyboardButton(
                text=f"📢 {channel.get('title', 'Channel')}",
                url=f"https://t.me/{username[1:] if username.startswith('@') else username}"
            ))
    
 
    markup.add(types.InlineKeyboardButton(
        text=get_message(user_id, 'check_subscription'),
        callback_data="check_subscription"
    ))
    
    return message, markup

def extract_channel_info_from_message(message):
    try:
        if message.forward_from_chat:
            chat = message.forward_from_chat
            
            try:
                bot_member = bot.get_chat_member(chat.id, bot.get_me().id)
                if bot_member.status not in ['administrator', 'creator']:
                    return None, "not_admin"
            except:
                return None, "not_admin"
            
            channel_info = {
                'chat_id': chat.id,
                'title': chat.title,
                'type': chat.type,
                'username': chat.username,
                'invite_link': None
            }
            
       
            if not chat.username:
                try:
                    invite = bot.create_chat_invite_link(chat.id, member_limit=1)
                    channel_info['invite_link'] = invite.invite_link
                except:
                    pass
            
            return channel_info, "success"
        
        return None, "not_channel"
    except Exception as e:
        return None, "error"

def extract_channel_info_from_link(link_or_username):
    try:
        
        link_or_username = link_or_username.strip()
        
        
        if 't.me/' in link_or_username:
            username = link_or_username.split('t.me/')[-1].split('/')[0]
            if username.startswith('@'):
                username = username[1:]
        elif link_or_username.startswith('@'):
            username = link_or_username[1:]
        else:
            username = link_or_username
        
        
        chat = bot.get_chat(f"@{username}")
        
        
        try:
            bot_member = bot.get_chat_member(chat.id, bot.get_me().id)
            if bot_member.status not in ['administrator', 'creator']:
                return None, "not_admin"
        except:
            return None, "not_admin"
        
        channel_info = {
            'chat_id': chat.id,
            'title': chat.title,
            'type': chat.type,
            'username': chat.username,
            'invite_link': None
        }
        
        return channel_info, "success"
        
    except Exception as e:
        return None, "error"


async def create_email_account():
    email_url = "https://api.mail.tm"
    email_headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        async with aiohttp.ClientSession(headers=email_headers) as session:
            domains_resp = await session.get(f"{email_url}/domains")
            domains_data = await domains_resp.json()
            domain = domains_data["hydra:member"][0]["domain"]
            
            username = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(12))
            email = f"{username}@{domain}"
            password = f"Pass{random.randint(1000, 9999)}!"
            
            payload = {"address": email, "password": password}
            await session.post(f"{email_url}/accounts", json=payload)
            
            token_resp = await session.post(f"{email_url}/token", json=payload)
            token_data = await token_resp.json()
            token = token_data.get("token")
            
            return email, password, token
            
    except Exception as e:
        return False, False, False

async def wait_for_verification_code(token, email):
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Authorization": f"Bearer {token}"
    }
    
    timeout = 300
    start_time = time.time()
    
    async with aiohttp.ClientSession(headers=headers) as session:
        while time.time() - start_time < timeout:
            try:
                messages_resp = await session.get("https://api.mail.tm/messages")
                inbox = await messages_resp.json()
                messages = inbox.get("hydra:member", [])
                
                for msg in messages:
                    sender = msg.get('from', {}).get('address', '')
                    if 'nanabanana.ai' in sender:
                        msg_id = msg["id"]
                        msg_resp = await session.get(f"https://api.mail.tm/messages/{msg_id}")
                        full_msg = await msg_resp.json()
                        text_content = full_msg.get('text', '')
                        matches = re.findall(r'\b\d{6}\b', text_content)
                        if matches:
                            code = matches[0]
                            return code
                
                await asyncio.sleep(5)
            except Exception as e:
                await asyncio.sleep(5)
    
    return None

async def create_nanabanana_account():
    
    email, password, mail_token = await create_email_account()
    
    if not email or not mail_token:
        return None, None, None
    
    nana_headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?1",
        'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    csrf_response = requests.get("https://nanabanana.ai/api/auth/csrf", headers=nana_headers)
    csrf_token = None
    csrf_cookie = None
    
    if csrf_response.text:
        try:
            csrf_data = json.loads(csrf_response.text)
            csrf_token = csrf_data.get("csrfToken")
        except:
            pass
    
    if '__Host-authjs.csrf-token' in csrf_response.cookies:
        csrf_cookie = csrf_response.cookies.get('__Host-authjs.csrf-token')
    
    cookies_dict = csrf_response.cookies.get_dict()
    
    verification_headers = {**nana_headers, 'Content-Type': "application/json", 'origin': "https://nanabanana.ai", 'referer': "https://nanabanana.ai/ar/ai-image", 'Cookie': f"__Host-authjs.csrf-token={csrf_cookie}"}
    
    for key, value in cookies_dict.items():
        if key != '__Host-authjs.csrf-token':
            verification_headers['Cookie'] += f"; {key}={value}"
    
    verification_payload = {"email": email}
    verification_response = requests.post("https://nanabanana.ai/api/auth/email-verification", data=json.dumps(verification_payload), headers=verification_headers)
    
    code = await wait_for_verification_code(mail_token, email)
    
    if not code:
        return None, None, None
    
    callback_headers = {**nana_headers, 'x-auth-return-redirect': "1", 'origin': "https://nanabanana.ai", 'referer': "https://nanabanana.ai/ar/ai-image", 'Cookie': f"__Host-authjs.csrf-token={csrf_cookie}"}
    
    for key, value in cookies_dict.items():
        if key != '__Host-authjs.csrf-token':
            callback_headers['Cookie'] += f"; {key}={value}"
    
    callback_payload = {'email': email, 'code': code, 'redirect': "false", 'csrfToken': csrf_token, 'callbackUrl': "https://nanabanana.ai/ar/ai-image"}
    final_response = requests.post("https://nanabanana.ai/api/auth/callback/email-verification", data=callback_payload, headers=callback_headers)
    
    final_cookies = final_response.cookies.get_dict()
    session_token = None
    if '__Secure-authjs.session-token' in final_cookies:
        session_token = final_cookies['__Secure-authjs.session-token']
    
    if session_token:
        return email, password, session_token
    else:
        return None, None, None

def upload_image(image_path):
    url = "https://nanabanana.ai/api/upload"
    try:
        if not os.path.exists(image_path):
            return None
        
        with open(image_path, 'rb') as f:
            file_content = f.read()
        
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
            'sec-ch-ua-platform': "\"Android\"",
            'sec-ch-ua': "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            'sec-ch-ua-mobile': "?1",
            'origin': "https://nanabanana.ai",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://nanabanana.ai/ar/ai-image",
            'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            'priority': "u=1, i"
        }
        
        files = [('file', (os.path.basename(image_path), file_content, 'image/jpeg'))]
        response = requests.post(url, files=files, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            image_url = data.get("url")
            return image_url
        else:
            return None
    except Exception as e:
        return None

def create_or_edit_image(session_token, prompt, image_urls=None):
    url = "https://nanabanana.ai/api/image-generation-nano-banana/create"
    payload = {
        "prompt": prompt,
        "output_format": "png",
        "image_size": "auto",
        "enable_pro": False,
        "width": 1024,
        "height": 1024,
        "steps": 20,
        "guidance_scale": 7.5,
        "is_public": False
    }
    
    if image_urls:
        payload["image_urls"] = image_urls
    
    cookie_string = f"__Secure-authjs.session-token={session_token}; __Secure-authjs.callback-url=https%3A%2F%2Fnanabanana.ai%2Far%2Fai-image"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?1",
        'origin': "https://nanabanana.ai",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://nanabanana.ai/ar/ai-image",
        'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        'priority': "u=1, i",
        'Cookie': cookie_string
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        task_id = data.get("task_id")
        if task_id:
            return task_id
        else:
            return None
    else:
        return None

def check_status(task_id, session_token, max_attempts=40, delay=5):
    url = "https://nanabanana.ai/api/image-generation-nano-banana/status"
    cookie_string = f"__Secure-authjs.session-token={session_token}; __Secure-authjs.callback-url=https%3A%2F%2Fnanabanana.ai%2Far%2Fai-image"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?1",
        'origin': "https://nanabanana.ai",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://nanabanana.ai/ar/ai-image",
        'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        'priority': "u=1, i",
        'Cookie': cookie_string
    }
    
    for attempt in range(max_attempts):
        payload = {"taskId": task_id}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "generations" in data and len(data["generations"]) > 0:
                generation = data["generations"][0]
                status = generation.get("status", "unknown")
                if status == "succeed":
                    image_url = generation.get("url", "")
                    if image_url:
                        return image_url
                    else:
                        return None
                elif status == "failed":
                    return None
                elif status == "waiting":
                    time.sleep(delay)
                elif status == "processing":
                    time.sleep(delay)
                else:
                    time.sleep(delay)
            else:
                time.sleep(delay)
        else:
            time.sleep(delay)
    
    return None

def download_image(image_url, task_id, account_email):
    try:
        response = requests.get(image_url, stream=True)
        
        if response.status_code == 200:
            os.makedirs("generated_images", exist_ok=True)
            safe_email = account_email.replace("@", "_").replace(".", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_images/image_{safe_email}_{timestamp}.png"
            
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            
            return filename
        else:
            return None
    except Exception as e:
        return None


async def create_account_for_request(user_id):
    email, password, session_token = await create_nanabanana_account()
    
    if session_token:
        
        accounts = load_accounts()
        new_account = {
            'user_id': user_id,
            'email': email,
            'password': password,
            'session_token': session_token,
            'created_at': datetime.now().isoformat()
        }
        accounts.append(new_account)
        save_accounts(accounts)
        
        
        user = get_user(user_id)
        if user:
            user['request_count'] = user.get('request_count', 0) + 1
            save_user(user)
        
        return new_account
    return None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
   
    is_subscribed, not_joined = check_user_subscription(user_id)
    
    if not is_subscribed and user:
        
        message_text, markup = show_subscription_required(user_id, not_joined)
        bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='HTML')
        return
    
    if not user:
 
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn_ar = types.KeyboardButton('🇸🇦 العربية')
        btn_en = types.KeyboardButton('🇬🇧 English')
        btn_fa = types.KeyboardButton('🇮🇷 فارسی')
        markup.add(btn_ar, btn_en, btn_fa)
        
        bot.send_message(message.chat.id, 
                        get_message(user_id, 'choose_language'), 
                        reply_markup=markup)
        
        
        new_user = {
            'id': user_id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'language': '',
            'request_count': 0,
            'created_at': datetime.now().isoformat(),
            'is_admin': user_id in ADMIN_IDS
        }
        save_user(new_user)
    else:
       
        show_main_menu(message, user)

@bot.message_handler(func=lambda message: message.text in ['🇸🇦 العربية', '🇬🇧 English', '🇮🇷 فارسی'])
def handle_language_selection(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if user:
  
        if message.text == '🇸🇦 العربية':
            user['language'] = 'ar'
        elif message.text == '🇬🇧 English':
            user['language'] = 'en'
        elif message.text == '🇮🇷 فارسی':
            user['language'] = 'fa'
        
        save_user(user)
        
        
        is_subscribed, not_joined = check_user_subscription(user_id)
        if not is_subscribed:
            message_text, markup = show_subscription_required(user_id, not_joined)
            bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='HTML')
        else:
            show_main_menu(message, user)

def handle_change_language(message):
    user_id = message.from_user.id
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_ar = types.KeyboardButton('🇸🇦 العربية')
    btn_en = types.KeyboardButton('🇬🇧 English')
    btn_fa = types.KeyboardButton('🇮🇷 فارسی')
    markup.add(btn_ar, btn_en, btn_fa)
    
    bot.send_message(message.chat.id, 
                    get_message(user_id, 'choose_language'), 
                    reply_markup=markup)

def handle_prompts_button(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    inline_markup = types.InlineKeyboardMarkup()
    
    button_text = "🔗 قناة البروميتات" if lang == 'ar' else ("🔗 Prompts Channel" if lang == 'en' else "🔗 کانال پرامپت‌ها")
    
    inline_markup.add(types.InlineKeyboardButton(text=button_text, url=PROMPTS_CHANNEL_LINK))
    
    response_text = "اضغط على الزر أدناه للانتقال إلى قناة البروميتات:" if lang == 'ar' else (
                    "Click the button below to go to the prompts channel:" if lang == 'en' else
                    "برای رفتن به کانال پرامپت‌ها، روی دکمه زیر کلیک کنید:")
                    
    bot.send_message(message.chat.id, response_text, reply_markup=inline_markup)
    show_main_menu(message)


def show_main_menu(message, user=None):
    user_id = message.from_user.id
    if not user:
        user = get_user(user_id)
    
    
    is_subscribed, not_joined = check_user_subscription(user_id)
    if not is_subscribed:
        message_text, markup = show_subscription_required(user_id, not_joined)
        bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='HTML')
        return
    
   
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    
    btn1 = types.KeyboardButton(get_message(user_id, 'create_image'))
    btn2 = types.KeyboardButton(get_message(user_id, 'edit_image'))
    btn3 = types.KeyboardButton(get_message(user_id, 'edit_multiple'))
    
    markup.add(btn1, btn2, btn3)
    
   
    btn_check = types.KeyboardButton(get_message(user_id, 'check_subscription'))
    btn_owner = types.KeyboardButton(get_message(user_id, 'bot_owner_contact'))
    btn_lang = types.KeyboardButton(get_message(user_id, 'change_language'))
    btn_prompts = types.KeyboardButton(get_message(user_id, 'prompts_button'))

    markup.add(btn_check, btn_owner, btn_lang, btn_prompts)
    
  
    
    if user.get('is_admin') or user_id in ADMIN_IDS:
        btn_admin = types.KeyboardButton(get_message(user_id, 'admin_panel'))
        markup.add(btn_admin)
    
   
    welcome_msg = f"{get_message(user_id, 'welcome')}\n\n{get_message(user_id, 'select_option')}"
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def handle_check_subscription(call):
    user_id = call.from_user.id
    is_subscribed, not_joined = check_user_subscription(user_id)
    
    if is_subscribed:
        bot.answer_callback_query(call.id, get_message(user_id, 'subscription_verified'))
        show_main_menu(call.message)
    else:
        message_text, markup = show_subscription_required(user_id, not_joined)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=message_text,
            reply_markup=markup,
            parse_mode='HTML'
        )
        bot.answer_callback_query(call.id, get_message(user_id, 'not_subscribed'))


def show_channels_management(message):
    user_id = message.from_user.id
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton(get_message(user_id, 'add_channel'))
    btn2 = types.KeyboardButton(get_message(user_id, 'remove_channel'))
    btn3 = types.KeyboardButton(get_message(user_id, 'channels_list'))
    btn_back = types.KeyboardButton(get_message(user_id, 'back'))
    markup.add(btn1, btn2, btn3, btn_back)
    
    bot.send_message(message.chat.id, get_message(user_id, 'channels_management'), reply_markup=markup)

def handle_add_channel(message):
    user_id = message.from_user.id
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_link = types.KeyboardButton("🔗 رابط / يوزر")
    btn_forward = types.KeyboardButton("📤 توجيه رسالة")
    btn_back = types.KeyboardButton(get_message(user_id, 'back'))
    markup.add(btn_link, btn_forward, btn_back)
    
    msg = bot.send_message(message.chat.id, 
                          "اختر طريقة إضافة القناة:" if get_user_language(user_id) == 'ar' else
                          "Choose channel addition method:" if get_user_language(user_id) == 'en' else
                          "روش افزودن کانال را انتخاب کنید:",
                          reply_markup=markup)
    
    bot.register_next_step_handler(msg, process_add_channel_method)

def process_add_channel_method(message):
    user_id = message.from_user.id
    method = message.text
    
    if method == get_message(user_id, 'back'):
        show_admin_panel(message)
        return
    
    if method == "🔗 رابط / يوزر":
        msg = bot.send_message(message.chat.id, get_message(user_id, 'enter_channel'),
                             reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_channel_link)
    elif method == "📤 توجيه رسالة":
        msg = bot.send_message(message.chat.id, get_message(user_id, 'forward_message'),
                             reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_forwarded_message)
    else:
        show_channels_management(message)

def process_channel_link(message):
    user_id = message.from_user.id
    link_or_username = message.text
    
    if link_or_username == get_message(user_id, 'back'):
        show_channels_management(message)
        return
    
    bot.send_message(message.chat.id, "⏳ جاري التحقق من القناة..." if get_user_language(user_id) == 'ar' else
                    "⏳ Checking channel..." if get_user_language(user_id) == 'en' else
                    "⏳ در حال بررسی کانال...")
    
    channel_info, status = extract_channel_info_from_link(link_or_username)
    
    if status == "success" and channel_info:
        channels = load_channels()
        
        for ch in channels:
            if ch.get('chat_id') == channel_info['chat_id']:
                bot.send_message(message.chat.id, 
                                "⚠️ القناة مضافَة مسبقاً!" if get_user_language(user_id) == 'ar' else
                                "⚠️ Channel already added!" if get_user_language(user_id) == 'en' else
                                "⚠️ کانال قبلا افزوده شده است!")
                show_channels_management(message)
                return
        
        channels.append(channel_info)
        save_channels(channels)
        
        bot.send_message(message.chat.id, get_message(user_id, 'channel_added'))
        show_channels_management(message)
    elif status == "not_admin":
        bot.send_message(message.chat.id, get_message(user_id, 'must_be_admin'))
        show_channels_management(message)
    else:
        bot.send_message(message.chat.id, 
                        "❌ فشل في إضافة القناة. تأكد من الرابط." if get_user_language(user_id) == 'ar' else
                        "❌ Failed to add channel. Check the link." if get_user_language(user_id) == 'en' else
                        "❌ افزودن کانال ناموفق بود. لینک را بررسی کنید.")
        show_channels_management(message)

def process_forwarded_message(message):
    user_id = message.from_user.id
    
    if not message.forward_from_chat:
        bot.send_message(message.chat.id, 
                        "❌ يجب توجيه رسالة من قناة!" if get_user_language(user_id) == 'ar' else
                        "❌ Must forward a message from a channel!" if get_user_language(user_id) == 'en' else
                        "❌ باید پیامی از کانال فوروارد کنید!")
        show_channels_management(message)
        return
    
    bot.send_message(message.chat.id, get_message(user_id, 'message_forwarded'))
    
    channel_info, status = extract_channel_info_from_message(message)
    
    if status == "success" and channel_info:
        channels = load_channels()
        
        for ch in channels:
            if ch.get('chat_id') == channel_info['chat_id']:
                bot.send_message(message.chat.id, 
                                "⚠️ القناة مضافَة مسبقاً!" if get_user_language(user_id) == 'ar' else
                                "⚠️ Channel already added!" if get_user_language(user_id) == 'en' else
                                "⚠️ کانال قبلا افزوده شده است!")
                show_channels_management(message)
                return
        
        channels.append(channel_info)
        save_channels(channels)
        
        bot.send_message(message.chat.id, get_message(user_id, 'channel_added'))
        show_channels_management(message)
    elif status == "not_admin":
        bot.send_message(message.chat.id, get_message(user_id, 'must_be_admin'))
        show_channels_management(message)
    else:
        bot.send_message(message.chat.id, 
                        "❌ فشل في إضافة القناة." if get_user_language(user_id) == 'ar' else
                        "❌ Failed to add channel." if get_user_language(user_id) == 'en' else
                        "❌ افزودن کانال ناموفق بود.")
        show_channels_management(message)

def handle_remove_channel(message):
    user_id = message.from_user.id
    channels = load_channels()
    
    if not channels:
        bot.send_message(message.chat.id, get_message(user_id, 'no_channels'))
        show_channels_management(message)
        return
    
    markup = types.InlineKeyboardMarkup()
    for i, channel in enumerate(channels):
        btn_text = f"❌ {channel.get('title', f'Channel {i+1}')}"
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"remove_channel_{i}"))
    
    markup.add(types.InlineKeyboardButton("↩️ رجوع" if get_user_language(user_id) == 'ar' else 
                                         "↩️ Back" if get_user_language(user_id) == 'en' else 
                                         "↩️ بازگشت", callback_data="back_to_channels"))
    
    bot.send_message(message.chat.id, get_message(user_id, 'select_channel_to_remove'), reply_markup=markup)

def handle_channels_list(message):
    user_id = message.from_user.id
    channels = load_channels()
    
    if not channels:
        bot.send_message(message.chat.id, get_message(user_id, 'no_channels'))
        show_channels_management(message)
        return
    
    response = "📋 قائمة القنوات:\n\n" if get_user_language(user_id) == 'ar' else \
              "📋 Channels List:\n\n" if get_user_language(user_id) == 'en' else \
              "📋 لیست کانال‌ها:\n\n"
    
    for i, channel in enumerate(channels, 1):
        response += f"{i}. {channel.get('title', 'Unknown Channel')}\n"
        if channel.get('username'):
            response += f"   👤 @{channel.get('username')}\n"
        else:
            response += f"   🔒 قناة خاصة\n" if get_user_language(user_id) == 'ar' else \
                       f"   🔒 Private channel\n" if get_user_language(user_id) == 'en' else \
                       f"   🔒 کانال خصوصی\n"
        response += f"   🆔 ID: {channel.get('chat_id')}\n"
        response += "   ───────────────\n"
    
    bot.send_message(message.chat.id, response)
    show_channels_management(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_channel_"))
def handle_remove_channel_callback(call):
    user_id = call.from_user.id
    channel_index = int(call.data.split("_")[-1])
    
    channels = load_channels()
    
    if 0 <= channel_index < len(channels):
        removed_channel = channels.pop(channel_index)
        save_channels(channels)
        
        bot.answer_callback_query(call.id, get_message(user_id, 'channel_removed'))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"✅ تمت إزالة القناة: {removed_channel.get('title', 'Unknown')}" if get_user_language(user_id) == 'ar' else
                 f"✅ Channel removed: {removed_channel.get('title', 'Unknown')}" if get_user_language(user_id) == 'en' else
                 f"✅ کانال حذف شد: {removed_channel.get('title', 'Unknown')}",
            reply_markup=None
        )
    else:
        bot.answer_callback_query(call.id, "❌ خطأ في الفهرس")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_channels")
def handle_back_to_channels(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_channels_management(call.message)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user or not user.get('language'):
        send_welcome(message)
        return
    

    if user.get('is_admin') or user_id in ADMIN_IDS:
        if message.text == get_message(user_id, 'admin_panel'):
            show_admin_panel(message)
            return
        elif message.text == get_message(user_id, 'channels_management'):
            show_channels_management(message)
            return
    
    msg_text = message.text
    
    if msg_text == get_message(user_id, 'create_image'):
        handle_create_image(message)
    elif msg_text == get_message(user_id, 'edit_image'):
        handle_edit_image(message)
    elif msg_text == get_message(user_id, 'edit_multiple'):
        handle_edit_multiple(message)
    elif msg_text == get_message(user_id, 'check_subscription'):
        is_subscribed, not_joined = check_user_subscription(user_id)
        if is_subscribed:
            bot.send_message(message.chat.id, get_message(user_id, 'subscription_verified'))
        else:
            message_text, markup = show_subscription_required(user_id, not_joined)
            bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='HTML')
    elif msg_text == get_message(user_id, 'bot_owner_contact'):
        bot.send_message(message.chat.id, f"👑 Developer: @X_GXN")
        show_main_menu(message, user)
    elif msg_text == get_message(user_id, 'change_language'):
        handle_change_language(message)
    elif msg_text == get_message(user_id, 'prompts_button'):
        handle_prompts_button(message)
    elif msg_text == get_message(user_id, 'back'):
        show_main_menu(message, user)
    elif msg_text == get_message(user_id, 'stats'):
        if user.get('is_admin') or user_id in ADMIN_IDS:
            show_stats(message)
        else:
            bot.send_message(message.chat.id, get_message(user_id, 'admin_only'))
    elif msg_text == get_message(user_id, 'accounts_list'):
        if user.get('is_admin') or user_id in ADMIN_IDS:
            show_accounts_list(message)
        else:
            bot.send_message(message.chat.id, get_message(user_id, 'admin_only'))
    elif msg_text == get_message(user_id, 'broadcast'):
        if user.get('is_admin') or user_id in ADMIN_IDS:
            ask_broadcast_message(message)
        else:
            bot.send_message(message.chat.id, get_message(user_id, 'admin_only'))
    elif msg_text == get_message(user_id, 'user_info'):
        if user.get('is_admin') or user_id in ADMIN_IDS:
            ask_user_id(message)
        else:
            bot.send_message(message.chat.id, get_message(user_id, 'admin_only'))
    elif msg_text in [get_message(user_id, 'add_channel'), 
                     get_message(user_id, 'remove_channel'), 
                     get_message(user_id, 'channels_list')]:
        if user.get('is_admin') or user_id in ADMIN_IDS:
            if msg_text == get_message(user_id, 'add_channel'):
                handle_add_channel(message)
            elif msg_text == get_message(user_id, 'remove_channel'):
                handle_remove_channel(message)
            elif msg_text == get_message(user_id, 'channels_list'):
                handle_channels_list(message)
        else:
            bot.send_message(message.chat.id, get_message(user_id, 'admin_only'))
    else:
        
        handle_conversation_flow(message)

def handle_create_image(message):
    user_id = message.from_user.id
    
    
    is_subscribed, not_joined = check_user_subscription(user_id)
    if not is_subscribed:
        message_text, markup = show_subscription_required(user_id, not_joined)
        bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='HTML')
        return
    
    msg = bot.send_message(message.chat.id, get_message(user_id, 'send_prompt'))
    bot.register_next_step_handler(msg, process_create_image_prompt)

def process_create_image_prompt(message):
    user_id = message.from_user.id
    prompt = message.text
    
    if not prompt or len(prompt.strip()) < 3:
        bot.send_message(message.chat.id, get_message(user_id, 'prompt_too_short'))
        return
    
    is_subscribed, not_joined = check_user_subscription(user_id)
    if not is_subscribed:
        message_text, markup = show_subscription_required(user_id, not_joined)
        bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='HTML')
        return
    

    bot.send_message(message.chat.id, get_message(user_id, 'processing'))
    

    def create_image_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:

            account = loop.run_until_complete(create_account_for_request(user_id))
            
            if not account:
                bot.send_message(message.chat.id, get_message(user_id, 'error'))
                return
            
            
            task_id = create_or_edit_image(account['session_token'], prompt)
            
            if task_id:
                image_url = check_status(task_id, account['session_token'])
                if image_url:
                    filename = download_image(image_url, task_id, account['email'])
                    if filename:
                        with open(filename, 'rb') as photo:
                            bot.send_photo(message.chat.id, photo, 
                                         caption=get_message(user_id, 'image_created'))
                    else:
                        bot.send_message(message.chat.id, get_message(user_id, 'error'))
                else:
                    bot.send_message(message.chat.id, get_message(user_id, 'error'))
            else:
                bot.send_message(message.chat.id, get_message(user_id, 'error'))
        except Exception as e:
            bot.send_message(message.chat.id, get_message(user_id, 'error'))
        finally:
            loop.close()
    
    thread = threading.Thread(target=create_image_thread)
    thread.start()

def handle_edit_image(message):
    user_id = message.from_user.id
    
    
    is_subscribed, not_joined = check_user_subscription(user_id)
    if not is_subscribed:
        message_text, markup = show_subscription_required(user_id, not_joined)
        bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='HTML')
        return
    
    msg = bot.send_message(message.chat.id, get_message(user_id, 'send_image'))
    bot.register_next_step_handler(msg, process_edit_image_step1)

def process_edit_image_step1(message):
    user_id = message.from_user.id
    
    
    is_subscribed, not_joined = check_user_subscription(user_id)
    if not is_subscribed:
        message_text, markup = show_subscription_required(user_id, not_joined)
        bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='HTML')
        return
    
    if not message.photo:
        bot.send_message(message.chat.id, get_message(user_id, 'no_image'))
        return
    
    
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    os.makedirs("temp_images", exist_ok=True)
    temp_path = f"temp_images/{user_id}_{int(time.time())}.jpg"
    
    with open(temp_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    msg = bot.send_message(message.chat.id, get_message(user_id, 'image_received'))
    bot.register_next_step_handler(msg, lambda m: process_edit_image_step2(m, temp_path))

def process_edit_image_step2(message, image_path):
    user_id = message.from_user.id
    prompt = message.text
    
    is_subscribed, not_joined = check_user_subscription(user_id)
    if not is_subscribed:
        bot.send_message(message.chat.id, get_message(user_id, 'prompt_too_short'))
        if os.path.exists(image_path):
            os.remove(image_path)
        return
    
    if not prompt or len(prompt.strip()) < 3:
        bot.send_message(message.chat.id, get_message(user_id, 'prompt_too_short'))
        if os.path.exists(image_path):
            os.remove(image_path)
        return
    
    
    bot.send_message(message.chat.id, get_message(user_id, 'processing'))
    
    
    def edit_image_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            
            account = loop.run_until_complete(create_account_for_request(user_id))
            
            if not account:
                bot.send_message(message.chat.id, get_message(user_id, 'error'))
                if os.path.exists(image_path):
                    os.remove(image_path)
                return
            
           
            uploaded_url = upload_image(image_path)
            if os.path.exists(image_path):
                os.remove(image_path)
            
            if not uploaded_url:
                bot.send_message(message.chat.id, get_message(user_id, 'error'))
                return
            
            
            task_id = create_or_edit_image(account['session_token'], prompt, [uploaded_url])
            
            if task_id:
                image_url = check_status(task_id, account['session_token'])
                if image_url:
                    filename = download_image(image_url, task_id, account['email'])
                    if filename:
                        with open(filename, 'rb') as photo:
                            bot.send_photo(message.chat.id, photo, 
                                         caption=get_message(user_id, 'image_edited'))
                    else:
                        bot.send_message(message.chat.id, get_message(user_id, 'error'))
                else:
                    bot.send_message(message.chat.id, get_message(user_id, 'error'))
            else:
                bot.send_message(message.chat.id, get_message(user_id, 'error'))
        except Exception as e:
            bot.send_message(message.chat.id, get_message(user_id, 'error'))
        finally:
            loop.close()
    
    thread = threading.Thread(target=edit_image_thread)
    thread.start()

def handle_edit_multiple(message):
    user_id = message.from_user.id
    
    
    is_subscribed, not_joined = check_user_subscription(user_id)
    if not is_subscribed:
        message_text, markup = show_subscription_required(user_id, not_joined)
        bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='HTML')
        return
    
    
    session = get_user_session(user_id)
    session['temp_images'] = []
    
    

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_more = types.KeyboardButton(get_message(user_id, 'add_another_image'))
    btn_done = types.KeyboardButton(get_message(user_id, 'done_adding'))
    btn_back = types.KeyboardButton(get_message(user_id, 'back'))
    markup.add(btn_more, btn_done, btn_back)
    
    msg = bot.send_message(message.chat.id, get_message(user_id, 'send_images'), reply_markup=markup)
    bot.register_next_step_handler(msg, process_edit_multiple_collect)

def process_edit_multiple_collect(message):
    user_id = message.from_user.id
    session = get_user_session(user_id)
    
    
    if message.text == get_message(user_id, 'back'):
        clear_user_session(user_id)
        show_main_menu(message)
        return
    
    
    if message.text == get_message(user_id, 'done_adding'):
        if len(session['temp_images']) == 0:
            bot.send_message(message.chat.id, get_message(user_id, 'no_image'),
                           reply_markup=types.ReplyKeyboardRemove())
            clear_user_session(user_id)
            show_main_menu(message)
            return
        
       
        msg = bot.send_message(message.chat.id, get_message(user_id, 'send_edit_prompt'),
                             reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_edit_multiple_prompt)
        return
    
   
    if message.photo:
        
        if len(session['temp_images']) >= 5:
            bot.send_message(message.chat.id, get_message(user_id, 'max_images_reached'))
            
            
            msg = bot.send_message(message.chat.id, get_message(user_id, 'send_edit_prompt'),
                                 reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, process_edit_multiple_prompt)
            return
        
        
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        os.makedirs("temp_images", exist_ok=True)
        temp_path = f"temp_images/{user_id}_{int(time.time())}_{len(session['temp_images'])}.jpg"
        
        with open(temp_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        session['temp_images'].append(temp_path)
        
        
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn_more = types.KeyboardButton(get_message(user_id, 'add_another_image'))
        btn_done = types.KeyboardButton(get_message(user_id, 'done_adding'))
        btn_back = types.KeyboardButton(get_message(user_id, 'back'))
        markup.add(btn_more, btn_done, btn_back)
        
        status_msg = get_message(user_id, 'images_received').format(len(session['temp_images']))
        msg = bot.send_message(message.chat.id, status_msg, reply_markup=markup)
        
        
        if message.media_group_id and len(session['temp_images']) < 5:
            
            bot.register_next_step_handler(msg, process_edit_multiple_collect)
            return
        
        
        bot.register_next_step_handler(msg, process_edit_multiple_collect)
        return
    
   
    if message.text == get_message(user_id, 'add_another_image'):
        if len(session['temp_images']) >= 5:
            bot.send_message(message.chat.id, get_message(user_id, 'max_images_reached'))
        
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn_more = types.KeyboardButton(get_message(user_id, 'add_another_image'))
        btn_done = types.KeyboardButton(get_message(user_id, 'done_adding'))
        btn_back = types.KeyboardButton(get_message(user_id, 'back'))
        markup.add(btn_more, btn_done, btn_back)

        msg = bot.send_message(message.chat.id, "📤 أرسل الصورة التالية:" if get_user_language(user_id) == 'ar' else
                              "📤 Send the next image:" if get_user_language(user_id) == 'en' else
                              "📤 تصویر بعدی را ارسال کنید:",
                              reply_markup=markup)
        bot.register_next_step_handler(msg, process_edit_multiple_collect)
        return
    
    
    bot.send_message(message.chat.id, get_message(user_id, 'no_image'))
    
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_more = types.KeyboardButton(get_message(user_id, 'add_another_image'))
    btn_done = types.KeyboardButton(get_message(user_id, 'done_adding'))
    btn_back = types.KeyboardButton(get_message(user_id, 'back'))
    markup.add(btn_more, btn_done, btn_back)
    
    msg = bot.send_message(message.chat.id, 
                          "⚠️ لم ترسل صورة. اختر خياراً:" if get_user_language(user_id) == 'ar' else
                          "⚠️ No image sent. Choose an option:" if get_user_language(user_id) == 'en' else
                          "⚠️ تصویری ارسال نشد. گزینه ای انتخاب کنید:",
                          reply_markup=markup)
    bot.register_next_step_handler(msg, process_edit_multiple_collect)
    return

def process_edit_multiple_prompt(message):
    user_id = message.from_user.id
    session = get_user_session(user_id)
    prompt = message.text
    
    
    if 'temp_images' not in session or len(session['temp_images']) == 0:
        bot.send_message(message.chat.id, get_message(user_id, 'no_image'))
        clear_user_session(user_id)
        show_main_menu(message)
        return
    
    
    if not prompt or len(prompt.strip()) < 3:
        bot.send_message(message.chat.id, get_message(user_id, 'prompt_too_short'))
        
        
        for img_path in session['temp_images']:
            if os.path.exists(img_path):
                os.remove(img_path)
        clear_user_session(user_id)
        show_main_menu(message)
        return
    
    
    bot.send_message(message.chat.id, get_message(user_id, 'processing_images'))
    
    
    def process_images_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            
            account = loop.run_until_complete(create_account_for_request(user_id))
            
            if not account:
                bot.send_message(message.chat.id, get_message(user_id, 'error'))
                
                for img_path in session['temp_images']:
                    if os.path.exists(img_path):
                        os.remove(img_path)
                clear_user_session(user_id)
                return
            
            
            image_urls = []
            for img_path in session['temp_images']:
                uploaded_url = upload_image(img_path)
                if uploaded_url:
                    image_urls.append(uploaded_url)
                
                
                if os.path.exists(img_path):
                    os.remove(img_path)
            
            if not image_urls:
                bot.send_message(message.chat.id, get_message(user_id, 'error'))
                clear_user_session(user_id)
                return
            
            
            task_id = create_or_edit_image(account['session_token'], prompt, image_urls)
            
            if task_id:
                image_url = check_status(task_id, account['session_token'])
                if image_url:
                    filename = download_image(image_url, task_id, account['email'])
                    if filename:
                        with open(filename, 'rb') as photo:
                            bot.send_photo(message.chat.id, photo, 
                                         caption=get_message(user_id, 'images_edited'))
                    else:
                        bot.send_message(message.chat.id, get_message(user_id, 'error'))
                else:
                    bot.send_message(message.chat.id, get_message(user_id, 'error'))
            else:
                bot.send_message(message.chat.id, get_message(user_id, 'error'))
        except Exception as e:
            bot.send_message(message.chat.id, get_message(user_id, 'error'))
        finally:
            loop.close()
            clear_user_session(user_id)
    
    thread = threading.Thread(target=process_images_thread)
    thread.start()

def handle_conversation_flow(message):

    user_id = message.from_user.id
    show_main_menu(message)


def show_admin_panel(message):
    user_id = message.from_user.id
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton(get_message(user_id, 'stats'))
    btn2 = types.KeyboardButton(get_message(user_id, 'accounts_list'))
    btn3 = types.KeyboardButton(get_message(user_id, 'broadcast'))
    btn4 = types.KeyboardButton(get_message(user_id, 'user_info'))
    btn5 = types.KeyboardButton(get_message(user_id, 'channels_management'))
    btn_back = types.KeyboardButton(get_message(user_id, 'back'))
    markup.add(btn1, btn2, btn3, btn4, btn5, btn_back)
    
    bot.send_message(message.chat.id, "👑 لوحة الإدارة / Admin Panel / پنل مدیریت", reply_markup=markup)

def show_stats(message):
    user_id = message.from_user.id
    
    users = load_users()
    accounts = load_accounts()
    channels = load_channels()
    
    total_users = len(users)
    total_accounts = len(accounts)
    total_channels = len(channels)
    avg_accounts = total_accounts / total_users if total_users > 0 else 0
    
    stats_msg = f"""
{get_message(user_id, 'total_users').format(total_users)}
{get_message(user_id, 'total_accounts').format(total_accounts)}
📢 عدد القنوات: {total_channels}
{get_message(user_id, 'accounts_per_user').format(avg_accounts)}
"""
    
    bot.send_message(message.chat.id, stats_msg)

def show_accounts_list(message):
    user_id = message.from_user.id
    accounts = load_accounts()
    
    if not accounts:
        bot.send_message(message.chat.id, "📭 لا توجد حسابات." if get_user_language(user_id) == 'ar' else
                        "📭 No accounts." if get_user_language(user_id) == 'en' else
                        "📭 حسابی وجود ندارد.")
        return
    
    
    users_data = {}
    for acc in accounts:
        uid = acc.get('user_id', 'unknown')
        if uid not in users_data:
            users_data[uid] = []
        users_data[uid].append(acc)
    
    response = "📋 قائمة الحسابات المجمعة:\n\n" if get_user_language(user_id) == 'ar' else \
              "📋 Accounts List (Grouped):\n\n" if get_user_language(user_id) == 'en' else \
              "📋 لیست حساب‌ها (گروه‌بندی شده):\n\n"
    
    for uid, acc_list in list(users_data.items())[:20]:
        user = get_user(uid)
        username = user.get('username', 'N/A') if user else 'N/A'
        response += f"👤 User: {username} (ID: {uid})\n"
        response += f"   📧 Accounts: {len(acc_list)}\n"
        response += f"   📅 Last created: {acc_list[-1].get('created_at', 'N/A')[:10]}\n"
        response += "   ───────────────\n"
    
    if len(users_data) > 20:
        response += f"\n... و {len(users_data)-20} مستخدم آخر" if get_user_language(user_id) == 'ar' else \
                   f"\n... and {len(users_data)-20} more users" if get_user_language(user_id) == 'en' else \
                   f"\n... و {len(users_data)-20} کاربر دیگر"
    
    bot.send_message(message.chat.id, response)

def ask_broadcast_message(message):
    user_id = message.from_user.id
    msg = bot.send_message(message.chat.id, get_message(user_id, 'enter_broadcast'),
                         reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_broadcast_message)

def process_broadcast_message(message):
    user_id = message.from_user.id
    broadcast_text = message.text
    
    users = load_users()
    sent_count = 0
    
    for user in users:
        try:
            uid = user.get('id')
            if uid:
                bot.send_message(uid, broadcast_text)
                sent_count += 1
                time.sleep(0.1)  
        except:
            continue
    
    bot.send_message(message.chat.id, 
                    get_message(user_id, 'broadcast_sent').format(sent_count))
    show_admin_panel(message)

def ask_user_id(message):
    user_id = message.from_user.id
    msg = bot.send_message(message.chat.id, get_message(user_id, 'enter_user_id'),
                         reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_user_info)

def process_user_info(message):
    user_id = message.from_user.id
    
    try:
        target_id = int(message.text)
        target_user = get_user(target_id)
        
        if not target_user:
            bot.send_message(message.chat.id, get_message(user_id, 'user_not_found'))
            show_admin_panel(message)
            return
        

        accounts = load_accounts()
        user_accounts = [acc for acc in accounts if acc.get('user_id') == target_id]
        
        user_info = f"""
{get_message(user_id, 'user_info')}
{get_message(user_id, 'user_id').format(target_user.get('id'))}
👤 Username: @{target_user.get('username', 'N/A')}
📛 Name: {target_user.get('first_name', '')} {target_user.get('last_name', '')}
{get_message(user_id, 'user_lang').format(LANGUAGES.get(target_user.get('language', 'ar'), 'Unknown'))}
{get_message(user_id, 'user_accounts').format(len(user_accounts))}
{get_message(user_id, 'user_requests').format(target_user.get('request_count', 0))}
📅 Created: {target_user.get('created_at', 'N/A')[:10]}
"""
        
        bot.send_message(message.chat.id, user_info)
    except ValueError:
        bot.send_message(message.chat.id, "❌ معرّف غير صالح. يجب أن يكون رقماً." if get_user_language(user_id) == 'ar' else
                        "❌ Invalid ID. Must be a number." if get_user_language(user_id) == 'en' else
                        "❌ شناسه نامعتبر. باید عدد باشد.")
    finally:
        show_admin_panel(message)

def run_bot_polling():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            time.sleep(10)

run_bot_polling()
