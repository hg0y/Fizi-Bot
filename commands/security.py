import discord
from discord.ext import commands

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """منع إرسال الروابط داخل السيرفر"""
        if message.author.bot:
            return
        
        if "http://" in message.content or "https://" in message.content:
            await message.delete()
            await message.channel.send(f"🚫 {message.author.mention} لا يُسمح بإرسال الروابط!")

# 🔹 هذه الدالة ضرورية لتحميل `security.py` بشكل صحيح
async def setup(bot):
    await bot.add_cog(Security(bot))
