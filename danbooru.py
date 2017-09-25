import discord
from discord.ext import commands
from pybooru import Danbooru

class DanbooruSearcher():
    def __init__(self, bot):
        self.bot = bot
        self.danbooru_client = Danbooru('danbooru')
        self.safe_channels = [
                "general",
                "robot-shop"
                ]
        self.blacklisted_tags = set()

    @commands.group(pass_context = True)
    async def react(self, ctx, *tags : str):
        if len(tags)==0:
            tags = ('trap',)
        safe_search_enabled = str(ctx.message.channel.name) in self.safe_channels
        if len(tags) > 2:
            await self.bot.say('Sorry. Danbooru only lets me search for two tags at a time. You searched for \'{}\'. If this channel is SFW, you can only search for one tag at a time.'.format(', '.join(tags)))
            return
        print('Seeking image for ' + ' '.join(tags))
        try:
            posts = await self.safe_search(ctx, tags) if safe_search_enabled else await self.search(tags)
            if posts:
                url = 'https://danbooru.donmai.us' + posts[0]['file_url']
                await self.bot.say(url)
            else:
                return
        except Exception as e:
            print('{} : {}'.format(type(e).__name__, e))
            await self.bot.say('Sorry. I couldn\'t find any images using these tags: ' + ' '.join(tags))

    async def search(self, tags : str):
        return self.danbooru_client.post_list(tags=' '.join(tags), random=True, limit=1)

    async def safe_search(self, ctx, tags : str):
        print('This is a SFW channel! Adding non-explicit rating tag!')
        tags = tags + ('rating:safe',)
        posts = await self.search(tags)
        attempts = 0
        while self.blacklisted_tags & set(posts[0]['tag_string_general'].split(' ')) and attempts < 5:
            posts = await self.search(tags)
            attempts = attempts + 1
        if attempts >= 5:
            await self.bot.say('Couldn\'t find any clean images.')
            await self.bot.send_file(ctx.message.channel, 'images/guess_ill_die.jpg')
            return None
        return posts

    @commands.group(pass_context=True)
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Blacklisted tags are: {}'.format(', '.join(self.blacklisted_tags)))

    @blacklist.command()
    async def add(self, *tags : str):
        await self.bot.say('Adding tag(s) \'{}\' to blacklist')
        for tag in tags:
            self.blacklisted_tags.add(tag)

def setup(bot):
    bot.add_cog(DanbooruSearcher(bot))
