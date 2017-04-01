import re

def normalize_text(text):
    text = re.sub(r'[^-;,.a-zA-Z ]', '', text).lower().strip()
    text = re.sub(r' +', ' ', text)
    return text

def cleanup_text(text):
    text = re.sub(r'[^->!?;.,a-zA-Z ]', '', text).lower().strip()
    text = re.sub(r'(^|\s|[!?;.,])[^a-zA-Z0-9]+(\s|$|[!?;.,])', ' ', text)
    text = re.sub(r' +', ' ', text)
    text = text.strip()
    return text

def deduplicate_text_blocks(text_blocks):
    seen = {}
    new_blocks = []
    for t in text_blocks:
        text = t.get_text()
        norm = normalize_text(text)
        cleaned_up = cleanup_text(text)
        if not seen.get(norm) and len(cleaned_up) > 1:
            seen[norm] = True
            t.text = cleaned_up
            new_blocks.append(t)

    return new_blocks

def filter_tree(root):
    if root.text_blocks:
        root.text_blocks = deduplicate_text_blocks(root.text_blocks)

    for c in root.children:
        filter_tree(c)
