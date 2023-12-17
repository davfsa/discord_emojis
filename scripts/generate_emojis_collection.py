# -*- coding: utf-8 -*-
# Copyright (c) 2021 davfsa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""A script to generate a python file containing a mapping of all valid Discord Emojis.

This script takes as a first argument the template which includes the copyright and any
other info and, as a second argument, the location to output the file.
"""
import os
import shutil
import sys
import typing

import requests

sys.path.append(".")

from discord_emojis import utils

DISCORD_EMOJI_MAPPING_URL = "https://emzi0767.gl-pages.emzi0767.dev/discord-emoji/discordEmojiMap-canary.min.json"


def fetch_discord_emojis() -> typing.Tuple[str, typing.List[str]]:
    response = requests.get(DISCORD_EMOJI_MAPPING_URL)
    response.encoding = "utf-8-sig"
    response_json = response.json()

    version = response_json["version"]
    emojis = [utils.normalize_emoji(emoji_json["surrogates"]) for emoji_json in response_json["emojiDefinitions"]]

    return version, emojis


def create_emoji_file(*, template_file: str, output_file: str, version: str, emojis: typing.List[str]) -> None:
    try:
        os.remove(output_file)
    except FileNotFoundError:
        pass
    shutil.copy(template_file, output_file)

    with open(output_file, "a") as fp:
        fp.write("# File generated using scripts/generate_emojis_collection.py\n")
        fp.write(f"# Emoji count: {len(emojis)}\n")
        fp.write("import typing\n\n")

        fp.write('__all__: typing.Sequence[str] = ("EMOJIS", "EMOJIS_VERSION")\n\n')

        fp.write(f'EMOJIS_VERSION: typing.Final[str] = "{version}"\n')
        fp.write("EMOJIS: typing.Set[str] = {\n")

        for emoji in emojis:
            fp.write(f'    "{emoji}",\n')

        fp.write("}\n")


def main() -> None:
    if len(sys.argv) < 3:
        print("Missing arguments")
        exit(1)

    if len(sys.argv) > 3:
        print("Too many arguments")
        exit(1)

    version, emojis = fetch_discord_emojis()

    template_file = sys.argv[1]
    output_file = sys.argv[2]
    create_emoji_file(
        template_file=template_file,
        output_file=output_file,
        version=version,
        emojis=emojis,
    )

    print(f"Generated emoji list file under: {output_file}")


if __name__ == "__main__":
    main()
