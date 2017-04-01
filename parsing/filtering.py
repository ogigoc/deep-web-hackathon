import re

def normalize_text(text):
    text = re.sub(r'[^-;,.a-zA-Z ]', '', text).lower().strip()
    text = re.sub(r' +', ' ', text)
    return text

def cleanup_text(text):
    text = re.sub(r'[^->!?;.,a-zA-Z ]', '', text).lower().strip()
    text = re.sub(r' +', ' ', text)
    return text

def deduplicate_text_blocks(text_blocks):
    seen = {}
    new_blocks = []
    for t in text_blocks:
        norm = normalize_text(t.get_text())
        if not seen.get(norm):
            seen[norm] = True
            t.text = cleanup_text(t.text)
            new_blocks.append(t)

    return new_blocks

def filter_tree(root):
    if root.text_blocks:
        root.text_blocks = deduplicate_text_blocks(root.text_blocks)

    for c in root.children:
        filter_tree(c)
