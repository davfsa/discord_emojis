# discord_emojis

This library contains an up-to-date list of all valid Discord emojis.
It runs a cron job every day to check for a new version of Discord Emojis and,
if it finds one, will update the list and publish a new version of the package.

This package is mainly used by [hikari](https://github.com/hikari-py/hikari) to
validate emojis.

# Installation

Installation is as easy as `pip install -U discord_emojis`. This will fetch the
latest version of the package or update it if a new version is available.

# What does this package provide?

This package provides 3 variables:
- `EMOJIS_VERSION`: The version of the Discord emoji mapping used to
  generate the package.
- `EMOJIS`: A collection of all valid Discord Emojis.

# Acknowledgements

Thanks a lot to [Emzi0767](https://github.com/Emzi0767) for providing the
up-to-date Discord emoji mapping.
