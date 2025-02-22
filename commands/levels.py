import discord
from discord.ext import commands
import sqlite3
import random

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("database/database.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS xp (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1
            )
        """)
        self.conn.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        """إضافة XP عند إرسال رسالة"""
        if message.author.bot:
            return

        user_id = message.author.id
        self.cur.execute("SELECT xp, level FROM xp WHERE user_id=?", (user_id,))
        result = self.cur.fetchone()

        if result is None:
            xp, level = 0, 1
            self.cur.execute("INSERT INTO xp (user_id, xp, level) VALUES (?, ?, ?)", (user_id, xp, level))
        else:
            xp, level = result
            xp += random.randint(5, 15)  
            next_level_xp = level * 100  

            if xp >= next_level_xp:
                level += 1
                await message.channel.send(f"🎉 {message.author.mention} لقد وصلت إلى المستوى {level}!")

            self.cur.execute("UPDATE xp SET xp=?, level=? WHERE user_id=?", (xp, level, user_id))

        self.conn.commit()

    @commands.command()
    async def مستوى(self, ctx, member: discord.Member = None):
        """عرض مستوى المستخدم"""
        member = member or ctx.author
        self.cur.execute("SELECT xp, level FROM xp WHERE user_id=?", (member.id,))
        result = self.cur.fetchone()

        if result is None:
            await ctx.send(f"🔹 {member.mention} لم يحصل على أي XP بعد.")
        else:
            xp, level = result
            await ctx.send(f"🔹 {member.mention} | المستوى: {level} | XP: {xp}")

async def setup(bot):
    await bot.add_cog(Levels(bot))
