# discord_emojis

This library contains an up-to-date list of all valid Discord emojis.
It runs a cron job every day to check for a new version of Discord Emojis and,
if it finds one, will update the list and publish a new version of the package.

# Installation

Installation is as easy as `pip install -U discord_emojis`. This will fetch the
latest version of the package or update it if a new version is available.

# What does this package provide?

This tiny package provides `discord_emojis.EMOJIS`, a set of all valid Discord emojis.

The version of the package and emojis can be checked with `discord_emojis.__version__`
and `discord_emojis.__emojis_version__` respectively.

Additionally, `discord_emojis.utils` provides additional utilities to help
dealing with emojis.

# Acknowledgements

Thanks a lot to [Emzi0767](https://github.com/Emzi0767) for providing the
up-to-date Discord emoji mapping.
