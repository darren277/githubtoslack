""""""
from flask import render_template_string


def format_block(block, **data):
    if block['type'] == 'section':
        block['text'] = format_block(block['text'], **data)
        return block
    elif block['type'] == 'mrkdwn':
        block['text'] = render_template_string(block['text'], **data)
        return block



class SlackCommentTemplate:
    def __init__(self, *blocks: dict):
        self.blocks = list(blocks)

    def format(self, **data):
        # Copy each block to prevent overwriting
        return [format_block(block.copy(), **data) for block in self.blocks]


