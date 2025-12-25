import logging

logging.basicConfig(level=logging.WARNING, force=True)

logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("discord.client").setLevel(logging.WARNING)
logging.getLogger("discord.gateway").setLevel(logging.WARNING)

from mimimi_bot.bot_factory import create_bot
from mimimi_bot.config import load_config


def main():
    config = load_config()
    bot = create_bot()
    bot.run(config.token)


if __name__ == "__main__":
    main()
