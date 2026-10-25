"""Participant UI translations; authored survey text is never auto-translated."""
import json
from pathlib import Path

MESSAGES = json.loads(Path(__file__).with_name('locale-messages.json').read_text())
LANGUAGES = ('en', 'ko', 'zh-CN', 'zh-TW')

def translate(language, message):
    if language not in LANGUAGES:
        raise ValueError('Choose en, ko, zh-CN or zh-TW for greedyq.language.')
    return message if language == 'en' or message not in MESSAGES else MESSAGES[message][LANGUAGES.index(language)-1]
