import re
from collections import Counter
from pathlib import Path

message_id_regex = re.compile(r'msgid \"(.+)\"', re.MULTILINE)
empty_message_regex = re.compile(r'msgid \"(.+)\"\nmsgstr \"\"\n[^\"]')

for po in Path('resources/locales').glob('**/LC_MESSAGES/texts.po'):
    text = po.read_text()

    message_ids = message_id_regex.findall(text)
    print(f'messages count: {len(message_ids)}')

    for message_id, count in Counter(message_ids).items():
        if count > 1:
            print(f'Duplicate message_id: {message_id} == {count}')

    empty_message_ids = empty_message_regex.findall(text)

    if empty_message_ids:
        print('\n'.join(empty_message_ids))
