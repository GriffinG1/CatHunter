import discord
from discord.ext import commands
from datetime import datetime


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print(f"Loaded {self.__class__.__name__} cog.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Log joins
        embed = discord.Embed(title="Member Joined", colour=discord.Colour.green())
        embed.add_field(name="Member", value=f"{member.mention} | {member}", inline=False)
        embed.add_field(name="Joined At", value=discord.utils.format_dt(member.joined_at, style="F"), inline=False)
        await self.bot.join_logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Log leaves
        embed = discord.Embed(title="Member Left", colour=discord.Colour.red())
        embed.add_field(name="Member", value=f"{member.mention} | {member}", inline=False)
        embed.add_field(name="Joined At", value=discord.utils.format_dt(member.joined_at, style="F"), inline=False)
        embed.add_field(name="Left At", value=discord.utils.format_dt(datetime.now(), style="F"), inline=False)
        await self.bot.join_logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            embed = discord.Embed(title="DM Received")
            embed.add_field(name="Author", value=f"{message.author} ({message.author.mention})")
            embed.add_field(name="Message", value=message.content, inline=False)
            await self.bot.dm_logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if isinstance(message.channel, discord.abc.GuildChannel) or isinstance(message.channel, discord.threads.Thread) and message.author.id != self.bot.user.id:
            if not message.content or message.type == discord.MessageType.pins_add:
                return
            embed = discord.Embed(title="Message Deleted")
            if message.reference is not None:
                ref = message.reference.resolved
                embed.add_field(name="Replied To", value=f"[{'@' if len(message.mentions) > 0 and ref.author in message.mentions else ''}{ref.author}]({ref.jump_url}) ({ref.author.id})")
            if isinstance(message.channel, discord.threads.Thread):
                embed.add_field(name="Thread Location", value=f"{message.channel.parent.mention} ({message.channel.parent.id})", inline=False)
            embed.add_field(name="Author", value=f"{message.author} ({message.author.mention})")
            embed.add_field(name="Channel", value=f"{message.channel.mention}")
            embed.add_field(name="Message", value=message.content, inline=False)
            await self.bot.deleted_logs_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Events(bot))
