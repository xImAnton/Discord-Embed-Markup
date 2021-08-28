import discordembedmarkup
import discord
import importlib
from token import token


client = discord.Client()


@client.event
async def on_message(msg):
    if not msg.content.startswith("?test"):
        return
    importlib.reload(discordembedmarkup)
    embed = discord.Embed.from_dict(discordembedmarkup.parse("../test.dem").to_json())
    await msg.channel.send(embed=embed)


if __name__ == '__main__':
    client.run(token)
