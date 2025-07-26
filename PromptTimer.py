import os.path
import datetime
import time

import yaml

from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.provider.entities import Message
from pkg.plugin.events import *

@register(name="PromptTimer", description="Automatically adds current time and elapsed time since last chat to your prompts.", version="1.0.0", author="huangdihd")
class PromptTimer(BasePlugin):

    def __init__(self, host: APIHost):
        if not os.path.isdir('data/PromptTimer'):
            os.mkdir('data/PromptTimer')
        if not os.path.isfile('data/PromptTimer/last_messages_time.yml'):
            with open('data/PromptTimer/last_messages_time.yml', 'w'):
                pass

        with open('data/PromptTimer/last_messages_time.yml', 'r') as f:
            self.last_messages_time = yaml.safe_load(f)

        if self.last_messages_time is None or not isinstance(self.last_messages_time, dict):
            self.last_messages_time = {}

        super().__init__(host)

    def save(self):
        with open('data/PromptTimer/last_messages_time.yml', 'w') as f:
            yaml.dump(self.last_messages_time, f)


    @handler(PromptPreProcessing)
    async def prompt_preprocessor(self, ctx: EventContext):
        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        additional_prompt = str(now.strftime('现在的时间是:%c, 时区为%Z'))
        session_id = ctx.event.query.get_variable('session_id')

        if session_id in self.last_messages_time:
            additional_prompt += f", 距离上次对话已经过去了{time.time() - self.last_messages_time.get(session_id)}秒"

        ctx.event.default_prompt.append(Message(role='system', content=additional_prompt))

    @handler(NormalMessageResponded)
    async def handle_response(self, ctx: EventContext):
        session_id = ctx.event.query.get_variable('session_id')
        self.last_messages_time[session_id] = time.time()
        self.save()

    def __del__(self):
        self.save()