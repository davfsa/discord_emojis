#!/bin/sh
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
set -e

echo "Defined environment variables"
env | grep -oP "^[^=]+" | sort

if [ -z ${GITHUB_REF+x} ]; then echo "$GITHUB_REF environment variable is missing" && exit 1; fi
if [ -z "${GITHUB_REF}" ]; then echo "$GITHUB_REF environment variable is empty" && exit 1; fi
if [ -z ${GITHUB_TOKEN+x} ]; then echo "$GITHUB_TOKEN environment variable is missing" && exit 1; fi
if [ -z "${GITHUB_TOKEN}" ]; then echo "$GITHUB_TOKEN environment variable is empty" && exit 1; fi
if [ -z ${GITHUB_REPO_SLUG+x} ]; then echo "$GITHUB_REPO_SLUG environment variable is missing" && exit 1; fi
if [ -z "${GITHUB_REPO_SLUG}" ]; then echo "$GITHUB_REPO_SLUG environment variable is empty" && exit 1; fi

EMOJIS_VERSION=$(python -c "import discord_emojis; print(discord_emojis.EMOJIS_VERSION)")
VERSION=$(date +%Y.%0m.%0d)
BRANCH=${GITHUB_REF##*/}

# Commit all files
git config user.name "davfsa"
git config user.email "29100934+davfsa@users.noreply.github.com"

git add .
git commit -m "Discord Mapping Version $EMOJIS_VERSION"
git push

# Create release
post_data()
{
  cat <<EOF
{
  "tag_name": "$VERSION",
  "target_commitish": "$BRANCH",
  "name": "discord_emojis $VERSION",
  "draft": false,
  "prerelease": false
}
EOF
}

echo "Creating release $VERSION [branch: $BRANCH]"
curl \
  -d "$(post_data)" \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$GITHUB_REPO_SLUG/releases"
