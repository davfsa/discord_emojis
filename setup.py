# -*- coding: utf-8 -*-
# Copyright (c) 2020 Nekokatt
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

import os
import re

import setuptools


def get_version():
    with open(os.path.join("discord_emojis", "_version.py")) as fp:
        match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fp.read(), re.MULTILINE)

    if not match:
        raise RuntimeError("__version__ is not set!")

    return match.group(1)


def long_description():
    with open("README.md") as fp:
        return fp.read()


setuptools.setup(
    name="discord_emojis",
    version=get_version(),
    description="An up-to-date collection of all valid Discord emojis",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="davfsa",
    author_email="davfsa@hikari-py.dev",
    license="MIT",
    url="https://github.com/davfsa/discord_emojis",
    project_urls={
        "Source (GitHub)": "https://github.com/davfsa/discord_emojis",
        "Discord": "https://discord.gg/hikari",
        "Issue Tracker": "https://github.com/davfsa/discord_emojis/issues",
        "CI": "https://github.com/davfsa/discord_emojis/actions",
    },
    packages=["discord_emojis"],
    package_data={"discord_emojis": ["py.typed"]},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
)
