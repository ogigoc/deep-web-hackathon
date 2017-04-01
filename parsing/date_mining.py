import datefinder
import re

def get_date_for_node(text):
    matches = datefinder.find_dates(text, strict=True)
    if matches:
        for m in matches:
            return m
    else:
        return None

def precompute_date_occurences(node, cache):
    date = None
    for c in node.find_all(recursive=False):
        this_date = precompute_date_occurences(c, cache)
        if this_date and not date:
            date = this_date

    if not date:
        date = cache.get(node)

    if not date:
        text = node.get_text('').strip()
        text = re.sub(r'[^- ,/.:0-9a-zA-Z]', '', text)
        text = re.sub(r'Reply [0-9]+ ?(on)?', 'Reply ', text)
        text = re.sub(r' +', ' ', text)

        date = get_date_for_node(text)

    cache[node] = date
    return date

def find_first_date(node, cache):
    date = cache.get(node)
    if not date:
        for p in node.parents:
            parent_date = cache.get(p)
            if parent_date:
                date = parent_date
                break

    return date

def build_text_block_map(root, text_block_map):
    for t in root.text_blocks:
        text_block_map[t.element] = t

    for c in root.children:
        build_text_block_map(c, text_block_map)

def propagate_dates(node, cache, text_block_map, date = None):
    my_date = cache.get(node) or date
    text_block = text_block_map.get(node)
    if text_block:
        text_block.date = my_date

    for c in node.find_all(recursive=False):
        propagate_dates(c, cache, text_block_map, my_date)

def populate_text_block_dates_from_cache(root, cache, alt_cache):
    for t in root.text_blocks:
        if not alt_cache.get(t.element):
            t.date = find_first_date(t.element, cache)
            alt_cache[t.element] = True

    for c in root.children:
        populate_text_block_dates_from_cache(c, cache, alt_cache)

def add_dates_to_tree(root, html_root):
    date_cache = {}
    precompute_date_occurences(html_root, date_cache)

    text_block_map = {}
    build_text_block_map(root, text_block_map)
    propagate_dates(html_root, date_cache, text_block_map)
