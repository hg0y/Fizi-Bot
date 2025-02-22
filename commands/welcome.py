import discord
from discord.ext import commands
from config import WELCOME_CHANNEL_ID # تأكد من أن هذا المتغير موجود في config.py

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """إرسال رسالة ترحيب عند دخول عضو جديد"""
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            await channel.send(f"👋 مرحبًا بك {member.mention} في السيرفر! 🎉")

# 🔹 تأكد من وجود هذه الدالة في نهاية الملف
async def setup(bot):
    await bot.add_cog(Welcome(bot))
