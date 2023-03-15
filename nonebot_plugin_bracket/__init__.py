from nonebot import on_message
from nonebot.typing import T_State
from nonebot.params import EventPlainText
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="括号补全",
    description="补全消息中的括号，治愈强迫症",
    usage="",
)

bracket_pairs = {
    "(": ")",
    "（": "）",
    "[": "]",
    "【": "】",
    "{": "}",
}


async def check_brackets(state: T_State, text: str = EventPlainText()) -> bool:
    brackets = []
    for char in text:
        for open_bracket, close_bracket in bracket_pairs.items():
            if char == open_bracket:
                brackets.append(close_bracket)
            elif char == close_bracket:
                if not brackets or brackets.pop() != close_bracket:
                    return False
    if not brackets:
        return False
    state["brackets"] = "".join(brackets)
    return True


bracket = on_message(check_brackets, priority=13, block=True)


@bracket.handle()
async def _(state: T_State):
    await bracket.finish(state["brackets"])
