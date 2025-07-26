from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *

@register(name="PromptTimer", description="Automatically adds current time and elapsed time since last chat to your prompts.", version="0.1", author="huangdihd")
class PromptTimer(BasePlugin):

    def __init__(self, host: APIHost):
        super().__init__(host)

    @handler(PromptPreProcessing)
    async def _(self, ctx: EventContext):
        print(ctx.event.query.get_variables())

    # 插件卸载时触发
    def __del__(self):
        pass