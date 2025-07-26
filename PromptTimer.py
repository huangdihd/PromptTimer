import os.path
import datetime
import time

import yaml

from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *

@register(name="PromptTimer", description="Automatically adds current time and elapsed time since last chat to your prompts.", version="0.1", author="huangdihd")
class PromptTimer(BasePlugin):

    def __init__(self, host: APIHost):
        if not os.path.isdir('data/PromptTimer'):
            os.mkdir('data/PromptTimer')
        if not os.path.isfile('data/PromptTimer/last_message_times.yml'):
            with open('data/PromptTimer/last_messages_time.yml', 'w'):
                pass

        with open('data/PromptTimer/last_messages_time.yml', 'r') as f:
            self.last_messages_time = yaml.safe_load(f)

        if self.last_messages_time is None or not isinstance(self.last_messages_time, dict):
            self.last_messages_time = {}

        super().__init__(host)

    @handler(PromptPreProcessing)
    async def prompt_preprocessor(self, ctx: EventContext):
        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        additional_prompt = str(now.strftime('现在的时间是:%c, 时区为%Z'))
        session_id = ctx.event.query.get_variable('session_id')

        if session_id in self.last_messages_time:
            additional_prompt += f", 距离上次对话已经过去了{time.time() - self.last_messages_time.get(session_id)}秒"

        print(type(ctx.event.default_prompt[0]).__qualname__)

    # 插件卸载时触发
    def __del__(self):
        with open('data/PromptTimer/last_messages_time.yml', 'w') as f:
            yaml.dump(self.last_messages_time, f)