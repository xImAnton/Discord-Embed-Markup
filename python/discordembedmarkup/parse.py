from __future__ import annotations
from typing import List
from .util import NonEmptyValueDict

from typing import Tuple
import os.path
import pathlib


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


class EmbedTemplate:
    def __init__(self, dir_context: str):
        super(EmbedTemplate, self).__init__()
        self.dir_ctx: str = dir_context
        self.url: str = ""
        self.color: int = 0
        self.timestamp: int = 0
        self.author_name: str = ""
        self.author_icon: str = ""
        self.author_url: str = ""
        self.footer_text: str = ""
        self.footer_icon: str = ""
        self.thumbnail: str = ""

    def set_color(self, arg):
        rgb = [int(c) for c in arg.split(",")]
        if len(rgb) == 1:
            self.color = rgb_to_int(rgb[0], rgb[0], rgb[0])
        if len(rgb) == 3:
            self.color = rgb_to_int(*rgb)
        else:
            raise ValueError(f"{arg} could not be converted into a color")

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
            try:
                template_path = os.path.join(self.dir_ctx, f"{argument}.template.dem")
                e = parse(template_path, True)
            except FileNotFoundError:
                print(f"could not load template: {argument}")
                return True
            self.apply_template(e)
        elif name == "color":
            self.set_color(argument)
        else:
            return False
        return True

    def apply_template(self, template: EmbedTemplate):
        if template.color:
            self.color = template.color
        if template.url:
            self.url = template.url
        if template.author_url:
            self.author_url = template.author_url
        if template.author_icon:
            self.author_icon = template.author_icon
        if template.author_name:
            self.author_name = template.author_name
        if template.thumbnail:
            self.thumbnail = template.thumbnail
        if template.footer_icon:
            self.footer_icon = template.footer_icon
        if template.footer_text:
            self.footer_text = template.footer_text
        if template.timestamp:
            self.timestamp = template.timestamp


class Embed(EmbedTemplate, Context):
    def __init__(self, dir_context: str):
        super(Embed, self).__init__(dir_context)
        self.fields: List[EmbedField] = []
        self.image: str = ""

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


def rgb_to_int(r: int, g: int, b: int) -> int:
    return (r << 16) + (g << 8) + b


def strip_comments(line: str) -> Tuple[str, bool]:
    """
    strips all comments from the line
    a comment starts with a : and goes to the end of the line
    colons can be used in text using \:
    :param line: the line to strip
    :return: the line without comments and a bool indicating whether a comment was removed
    """
    # try to find a colon
    if line.startswith("@"):
        return line, False
    try:
        colon = line.index(":")
    except ValueError:
        return line, False

    # when the colon is escaped
    if colon > 0 and line[colon - 1] == "\\":
        return line[:colon - 1] + line[colon:], True

    # remove anything behind the colon
    return line[:colon], True


def strip_from_begin(line: str, substring: str) -> str:
    return line[len(substring):]


def split_command(command: str) -> Tuple[str, str]:
    space = command.index(" ")
    return command[1:space], command[space + 1:]


def parse(file, template: bool = False) -> Embed:
    with open(file, "r") as f:
        data = f.readlines()

    directory_ctx = str(pathlib.Path(file).parent.absolute())

    embed = EmbedTemplate(directory_ctx) if template else Embed(directory_ctx)
    context = None
    previous_line_empty = False
    for line in data:
        line, has_comment = strip_comments(line)
        line = line.strip()
        new_previous_line_empty = (not previous_line_empty and not has_comment and line) or \
                                  (previous_line_empty and not has_comment and line) or \
                                  (previous_line_empty and has_comment and line)
        # embed title
        if line.startswith("# "):
            if template:
                raise ValueError(f"you can set text inside a template, found {line}")
            embed.title = strip_from_begin(line, "# ")
            context = embed
            continue

        # field title
        if line.startswith("## "):
            if template:
                raise ValueError(f"you can set text inside a template, found {line}")
            context = EmbedField()
            context.title = strip_from_begin(line, "## ")
            embed.fields.append(context)
            continue

        # command
        if line.startswith("@"):
            command, argument = split_command(line)
            if not embed.command(command, argument):
                raise NameError("unsupported command: " + command)
            continue

        # set color
        if line.startswith("%"):
            embed.set_color(line[1:])

        # set timestamp
        if line.startswith("?"):
            continue

        if template:
            continue

        # add whitespace
        line = ("\n" if previous_line_empty else " ") + line

        if context:
            context.text += line

        previous_line_empty = new_previous_line_empty
    return embed
