import discord
from discord.ext import commands
import os
from flask import Flask, request, jsonify

# استيراد الإعدادات من config.py
from config import TOKEN

# تفعيل جميع الـ Intents (هامة لبعض الميزات مثل الترحيب)
intents = discord.Intents.all()

# إنشاء البوت مع بادئة الأوامر !
bot = commands.Bot(command_prefix="!", intents=intents)

# تحميل الأوامر من مجلد commands
@bot.event
async def on_ready():
    print(f"✅ تم تسجيل الدخول كبوت {bot.user}")
    await bot.change_presence(activity=discord.Game(name="ProBot Clone"))

    # تحميل جميع الأوامر الموجودة في مجلد commands
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.load_extension(f"commands.{filename[:-3]}")
            print(f"✔️ تم تحميل {filename}")

# تشغيل البوت باستخدام التوكن
bot.run(TOKEN)
