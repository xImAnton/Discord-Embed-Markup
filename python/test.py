import discordembedmarkup as dem
import discord
import dctoken


client = discord.Client()
dem.parse_blueprint("../test.dem")


@client.event
async def on_message(msg):
    if not msg.content.startswith("?test"):
        return
    embed = discord.Embed.from_dict(dem.load_blueprint("test").to_json())
    await msg.channel.send(embed=embed)


if __name__ == '__main__':
    client.run(dctoken.token)
