env = 1
if env:
    bot_token = "7711319167:AAF9c7J9NeFuH16sO_HIrbDSWMuExYxEuks"
    api_id = 28482138
    api_hash = "cdcd9c0f111f85feaafac50d1bc3d6a5"
    proxy = False
    proxy_address = ("socks5", "127.0.0.1", 2080)
    admins = [5415792594, 198937863]
    channel_id = "crypto_newsir"
else:
    bot_token = "7199432861:AAEe39s9aImUk6Vf2md7tkIYqkQb3FC87ko"
    api_id = 28482138
    api_hash = "cdcd9c0f111f85feaafac50d1bc3d6a5"
    proxy = True
    proxy_address = ("socks5", "127.0.0.1", 2080)
    admins = [5415792594, 198937863]
    channel_id = "hoooosseinbot"


bot_text = {
    "start": "به ربات خوش آمدید",
    "show_text": "مشاهده متن فعلی",
    "edit_text": "ویرایش متن",
    "text_info": "متن: {text}",
    "select": "لطفا یک دکمه را انتخاب کنید",
    "enter_text": "متن جدید را وارد کنید:\nتوجه کنید متن قبلی حذف خواهد شد",
    "back": "بازگشت",
    "canceled": "با موفقیت کنسل شد",
    "saved": "با موفقیت ذخیره شد"
}