import discordembedmarkup as dem
import timeit
import discord


dem.parse("../test.dem")


test_parsing = """
a = discord.Embed.from_dict(dem.load_embed("test"))
"""


if __name__ == '__main__':
    print(timeit.timeit(stmt=test_parsing, globals=globals(), number=10000))
