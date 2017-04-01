import readability
import re
from bs4 import BeautifulSoup

from .TextBlock import TextBlock
from .PathNode import PathNode
from .postprocessing import postprocess_path
from .filtering import filter_tree
from .transform import transform_tree

NODE_BLACKLIST = [ 'script', 'style', 'head' ]

def get_path(node):
    pass

def sanitize_id_or_class(id_or_class):
    return re.sub(r'[^-_a-zA-Z]', '', id_or_class.lower())

def create_pathnode(node):
    class_attr = node.get('class')
    cls = None
    if class_attr:
        seen_class = set()
        class_attr = [sanitize_id_or_class(c) for c in class_attr]
        cls = [c for c in class_attr if not (c in seen_class or
            seen_class.add(c))]

    id = None
    id_attr = node.get('id')
    if id_attr:
        id = sanitize_id_or_class(id_attr)

    tag = node.name

    return PathNode(tag, cls, id)

def add_to_path(path_root, node):
    parents = reversed(list(node.parents))

    current = None
    root = None
    path = []
    for p in parents:
        if not current:
            current = create_pathnode(p)
            root = current
            path.append(root)
        else:
            new = create_pathnode(p)
            path.append(new)
            current.add_child(new)
            current = new

    new = create_pathnode(node)
    current.add_child(new)
    path.append(new)

    found_path_leaf = path_root.find_path(root)
    leaf = None
    if found_path_leaf:
        leaf = found_path_leaf[0]
    else:
        leaf = path_root.add_path(path)

    leaf.add_text_block(TextBlock(node, 1.0, leaf))

def parse_html(html):
    # extract text under repeated html paths
    soup = BeautifulSoup(html, 'lxml')
    path_root = PathNode('pathroot', [], None)

    for node in soup.find_all():
        if node.name in NODE_BLACKLIST:
            node.extract()

    for node in soup.find_all():
        add_to_path(path_root, node)

    postprocess_path(path_root)
    filter_tree(path_root)

    return transform_tree(path_root)
