# -*- coding: utf-8 -*-
# Copyright (c) 2021-present davfsa
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

This script takes in the following arguments:
    1) The template to use as a preamble for the emojis
    2) The location to place the output file
    3) The location of the _version.py file
"""
import datetime
import json
import os
import re
import shutil
import sys
import typing
import urllib.request

sys.path.append(".")

from discord_emojis import emojis_collection
from discord_emojis import utils

DISCORD_EMOJI_MAPPING_URL = "https://emzi0767.mzgit.io/discord-emoji/discordEmojiMap-canary.min.json"


def fetch_discord_emojis() -> typing.Tuple[int, typing.List[str]]:
    with urllib.request.urlopen(DISCORD_EMOJI_MAPPING_URL) as request:
        response_json = json.loads(request.read())

    version = int(response_json["version"])
    emojis = [utils.normalize_emoji(emoji_json["surrogates"]) for emoji_json in response_json["emojiDefinitions"]]

    return version, emojis


def create_emoji_file(*, template_file: str, output_file: str, emojis: typing.List[str]) -> None:
    try:
        os.remove(output_file)
    except FileNotFoundError:
        pass

    shutil.copy(template_file, output_file)
    with open(output_file, "a") as fp:
        fp.write("# File generated using scripts/generate_emojis_collection.py\n")
        fp.write(f"# Emoji count: {len(emojis)}\n")
        fp.write("from __future__ import annotations\n\n")
        fp.write("import typing\n\n")

        fp.write('__all__: typing.Sequence[str] = ("EMOJIS",)\n\n')

        fp.write("EMOJIS: typing.Final[typing.Set[str]] = {\n")

        for emoji in emojis:
            fp.write(f'    "{emoji}",\n')

        fp.write("}\n")


def get_emoji_version(version_file: str) -> int:
    with open(version_file, "r") as fp:
        match = re.search(r'^__emojis_version__\s*=\s*"([^\'"]*)"', fp.read(), re.MULTILINE)
        if not match:
            raise RuntimeError("__emojis_version__ not found!")

        return int(match.group(1))


def set_emoji_version(*, version_file: str, version: int) -> None:
    with open(version_file, "r") as fp:
        content = fp.read()

    new_package_version = datetime.datetime.now().strftime("%Y.%m.%d")
    content = re.sub(
        r'^__version__\s*=\s*"([^\'"]*)"', f'__version__ = "{new_package_version}"', content, flags=re.MULTILINE
    )
    content = re.sub(
        r'^__emojis_version__\s*=\s*"([^\'"]*)"', f'__emojis_version__ = "{version}"', content, flags=re.MULTILINE
    )

    with open(version_file, "w") as fp:
        fp.write(content)


def main() -> int:
    if len(sys.argv) < 4:
        print(f"Missing arguments (received {len(sys.argv) - 1} expected 3)")
        return 1

    if len(sys.argv) > 4:
        print(f"Too many arguments (received {len(sys.argv) - 1}, expected 3)")
        return 1

    template_file = sys.argv[1]
    output_file = sys.argv[2]
    version_file = sys.argv[3]

    version, emojis = fetch_discord_emojis()

    emojis_set = set(emojis)
    if emojis_set == emojis_collection.EMOJIS:
        print(f"Emoji list up to date!")
        return 0

    added_count = len(emojis_set.difference(emojis_collection.EMOJIS))
    removed_count = len(emojis_collection.EMOJIS.difference(emojis_set))
    print(f"New emoji list version (version {version}; {added_count} added; {removed_count} removed)")

    create_emoji_file(template_file=template_file, output_file=output_file, emojis=emojis)
    set_emoji_version(version_file=version_file, version=version)

    print(f"Generated emoji list file under {output_file!r}")


if __name__ == "__main__":
    exit(main())
