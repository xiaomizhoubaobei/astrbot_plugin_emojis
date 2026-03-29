from astrbot.api.all import *
from .utils import EmojiUtils

# 这里保留 self_text 以便未来扩展，但核心逻辑已移至 EmojiUtils
# self_text 可在 EmojiUtils 中使用，此处引用保持一致
self_text = EmojiUtils.self_text