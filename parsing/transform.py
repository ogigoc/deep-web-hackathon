from .OutputTextBlock import OutputTextBlock
import datetime

def append_text_blocks(root, text_blocks):
    if root.text_blocks:
        text_blocks.append([OutputTextBlock(t.get_text(), datetime.datetime.now(), t.weight) for t
            in root.text_blocks])

def transform_tree(root, text_blocks = None):
    if text_blocks == None:
        text_blocks = []
    append_text_blocks(root, text_blocks)

    for c in root.children:
        transform_tree(c, text_blocks)

    return text_blocks
