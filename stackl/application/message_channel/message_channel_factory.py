import logging

from utils.general_utils import get_config_key
from utils.stackl_singleton import Singleton

logger = logging.getLogger("STACKL_LOGGER")


class MessageChannelFactory(metaclass=Singleton):
    def __init__(self):
        self.message_channel_type = get_config_key('MESSAGE_CHANNEL')

        logger.info(
            f"[MessageChannelFactory] Creating Message Channel with type: {self.message_channel_type}"
        )
        self.message_channel = None

        if self.message_channel_type == "Redis":
            from message_channel.redis_queue import RedisQueue
            self.message_channel = RedisQueue()
        else:  # default to Redis
            from message_channel.redis_queue import RedisQueue
            self.message_channel = RedisQueue()

    def get_message_channel(self):
        logger.info(
            "[MessageChannelFactory] Giving message channel with type '{self.message_channel_type}' and id '{self.message_channel}'"
        )
        return self.message_channel
