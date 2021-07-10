from typing import List
from .util import NonEmptyValueDict


class Context:
    """
    represents a context that normal text is appended to
    """
    def __init__(self):
        self.text: str = ""
        self.title: str = ""

    def to_json(self) -> dict:
        """
        returns a json representation of this component as dict
        :return: the json as dict
        """
        return {}

    def assert_filled(self):
        if not self.title.strip():
            raise ValueError("title cannot be empty")
        if not self.text.strip():
            raise ValueError("field text cannot be empty")


class EmbedField(Context):
    def to_json(self) -> dict:
        self.assert_filled()

        text = self.text.strip()
        inline = False
        if text.endswith("&") and not text.endswith("\\&"):
            inline = True
            text = text[:-1]

        return NonEmptyValueDict({
            "name": self.title,
            "value": text,
            "inline": inline
        })


class Embed(Context):
    def __init__(self):
        super(Embed, self).__init__()
        self.url: str = ""
        self.color: int = 0
        self.timestamp: int = 0
        self.author_name: str = ""
        self.author_icon: str = ""
        self.author_url: str = ""
        self.fields: List[EmbedField] = []
        self.image: str = ""
        self.thumbnail: str = ""
        self.footer_text: str = ""
        self.footer_icon: str = ""

    def command(self, name, argument) -> bool:
        """
        mutates this embed depending on the command
        :param name: the name of the command, see the docs for reference
        :param argument: the command argument
        :return: whether the command execution was successful
        """
        if name == "author":
            self.author_name = argument
        elif name == "author&":
            self.author_icon = argument
        elif name == "author?":
            self.author_url = argument
        elif name == "url" or name == "?":
            self.url = argument
        elif name == "thumbnail":
            self.thumbnail = argument
        elif name == "footer":
            self.footer_text = argument
        elif name == "footer&":
            self.footer_icon = argument
        elif name == "template":
            print("template support coming soon")
        else:
            return False
        return True

    def to_json(self) -> dict:
        self.assert_filled()

        return NonEmptyValueDict({
            "title": self.title,
            "description": self.text.strip(),
            "url": self.url,
            "timestamp": self.timestamp,
            "color": self.color,
            "footer": NonEmptyValueDict({
                "text": self.footer_text.strip(),
                "icon_url": self.footer_icon
            }),
            "fields": [f.to_json() for f in self.fields],
            "image": NonEmptyValueDict({"url": self.image}),
            "thumbnail": NonEmptyValueDict({"url": self.thumbnail}),
            "author": NonEmptyValueDict({
                "name": self.author_name,
                "url": self.author_url,
                "icon_url": self.author_icon
            })
        })
