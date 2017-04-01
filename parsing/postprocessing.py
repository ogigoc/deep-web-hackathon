from Levenshtein import distance

NODE_LAST_LEVEL = [ 'a', 'span', 'i', 'b', 'strong', 'em', 'u' ]
USELESS_KEYWORDS = [ 'header', 'footer', 'menu', 'navbar', 'navlinks',
        'breadcrumb', 'navigation' ]

MAX_DISTANCE = 0

elements_cache = {}

def get_all_elements(path_root):
    if elements_cache.get(path_root):
        return elements_cache[path_root]

    elems = [x.element for x in path_root.text_blocks]
    for c in path_root.children:
        elems += get_all_elements(c)

    elements_cache[path_root] = elems
    return elems

def remove_redundant_elements(path_root):
    for c in path_root.children:
        remove_redundant_elements(c)

    my_elems = [x.element for x in path_root.text_blocks]
    elems_underneath = get_all_elements(path_root)
    for e in elems_underneath:
        if e in my_elems:
            e.extract()

def flatten(path_root):
    to_remove = []
    for c in path_root.children:
        if c.tag in NODE_LAST_LEVEL:
            to_remove.append(c)
        else:
            flatten(c)

    path_root.children = [c for c in path_root.children if c not in to_remove]

def has_useful_text_blocks(elem):
    for t in elem.text_blocks:
        if len(t.get_text()) > 1:
            return True

    return False

def prune_empty_elements(path_root):
    for c in path_root.children:
        prune_empty_elements(c)

    to_remove = []
    for c in path_root.children:
        if not c.children and not has_useful_text_blocks(c):
            to_remove.append(c)

    path_root.children = [c for c in path_root.children if c not in to_remove]
    path_root.text_blocks = [t for t in path_root.text_blocks if
            len(t.get_text()) > 1]

def prune_useless_elements(path_root):
    to_remove = []
    for c in path_root.children:
        for useless in USELESS_KEYWORDS:
            if c.id and (distance(c.id, useless) <= MAX_DISTANCE or useless in c.id):
                #print('Removing {0} because of id {1}'.format(c, useless))
                to_remove.append(c)

            if c.cls:
                for cl in c.cls:
                    if distance(cl, useless) <= MAX_DISTANCE or useless in cl:
                        #print('Removing {0} because of class name {1}'.format(c, cl))
                        to_remove.append(c)

    path_root.children = [c for c in path_root.children if c not in to_remove]
    for c in path_root.children:
        prune_useless_elements(c)

def postprocess_path(path_root):
    flatten(path_root)
    remove_redundant_elements(path_root)
    prune_useless_elements(path_root)
    prune_empty_elements(path_root)
