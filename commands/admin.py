import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def مسح(self, ctx, amount: int):
        """مسح عدد معين من الرسائل"""
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"🗑 تم مسح {amount} رسالة!", delete_after=5)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def حظر(self, ctx, member: discord.Member, *, reason="لا يوجد سبب"):
        """حظر عضو من السيرفر"""
        await member.ban(reason=reason)
        await ctx.send(f"🚫 تم حظر {member.mention} | السبب: {reason}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def طرد(self, ctx, member: discord.Member, *, reason="لا يوجد سبب"):
        """طرد عضو من السيرفر"""
        await member.kick(reason=reason)
        await ctx.send(f"👢 تم طرد {member.mention} | السبب: {reason}")

# هذه الدالة هي السبب في المشكلة، يجب أن تكون موجودة
async def setup(bot):
    await bot.add_cog(Admin(bot))
