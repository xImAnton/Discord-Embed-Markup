from typing import Tuple

from .models import Embed, EmbedField


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


def parse(file) -> Embed:
    with open(file, "r") as f:
        data = f.readlines()

    embed = Embed()
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
            embed.title = strip_from_begin(line, "# ")
            context = embed
            continue

        # field title
        if line.startswith("## "):
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
            continue

        # set timestamp
        if line.startswith("?"):
            continue

        # add whitespace
        line = ("\n" if previous_line_empty else " ") + line

        if context:
            context.text += line

        previous_line_empty = new_previous_line_empty
    return embed
