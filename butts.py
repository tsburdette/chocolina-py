import discord
from discord.ext import commands

class Butts():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def butts(self):
        """Talks about how great butts are."""
        await self.bot.say('Butts are great!')

def setup(bot):
    bot.add_cog(Butts(bot))
