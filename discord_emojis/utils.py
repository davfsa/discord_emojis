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
"""Utilities to deal with Discord emojis."""


def normalize_emoji(emoji: str) -> str:
    """Normalize an emoji to later check with `discord_emojis.EMOJIS`.

    Parameters
    ----------
    emoji: str
        The emoji to normalize.

    Returns
    -------
    str
        The normalized emoji.
    """
    codepoints = [ord(c) for c in emoji]

    # It looks like the rule is to delete character #2 if the value
    # of this is 0xfe0f and the character is 4 characters long.
    # The gay-pride flag is an outlier, for god knows what reason.
    if codepoints[1:2] == [0xFE0F] and len(codepoints) <= 4 and codepoints != [0x1F3F3, 0xFE0F, 0x200D, 0x1F308]:
        codepoints = [codepoints[0], *codepoints[2:]]

    return "".join(chr(c) for c in codepoints)
