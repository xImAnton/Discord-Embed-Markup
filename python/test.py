import discordembedmarkup as dem
import json


if __name__ == '__main__':
    print(json.dumps({"embed": dem.parse("../test.dem").to_json()}, indent=4))
