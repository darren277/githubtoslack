""""""
from flask import render_template_string


def format_block(block, **data):
    # Avoid mutating the original block
    new_block = block.copy()

    if new_block['type'] == 'section':
        new_block['text'] = format_block(new_block['text'], **data)
        return new_block
    elif new_block['type'] == 'mrkdwn':
        new_block['text'] = render_template_string(new_block['text'], **data)
        return new_block



class SlackCommentTemplate:
    def __init__(self, *blocks: dict):
        self.blocks = list(blocks)

    def format(self, **data):
        # Copy each block to prevent overwriting
        return [format_block(block.copy(), **data) for block in self.blocks]


