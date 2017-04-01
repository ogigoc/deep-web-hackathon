from Levenshtein import distance

from .TextBlock import TextBlock

class PathNode:
    def __init__(self, tag, cls, id):
        self.id = id
        self.cls = cls
        self.tag = tag
        self.children = []
        self.text_blocks = []

    def shallow_matches(self, node):
        if self.id != node.id:
            return False

        if self.tag != node.tag:
            return False

        if self.cls:
            if not node.cls:
                return False

            ok = False
            for c in self.cls:
                if c in node.cls:
                    ok = True
                    break

            if not ok:
                return False

        return True

    def add_text_block(self, text_block):
        for t in self.text_blocks:
            if text_block.equals(t):
                return

        self.text_blocks.append(text_block)

    def add_child(self, child):
        self.children.append(child)

    def find_path(self, node):
        if not self.children and not node:
            return [self]

        applicable = []
        for c in self.children:
            # consider only those children that shallow match the given node
            if not c.shallow_matches(node):
                continue

            if not c.children and not node.children:
                # if no children on both the current child and the other node,
                # we have a leaf, so we can add it to the list
                applicable.append(c)
            else:
                # add all children that may result in a good path
                for other_c in node.children:
                    result = c.find_path(other_c)
                    if result:
                        applicable += result

        return applicable

    def find_leaf(self):
        if not self.children:
            return self
        else:
            return self.children[0].find_leaf()

    def add_path(self, nodes):
        if not nodes:
            return self

        for c in self.children:
            if c.shallow_matches(nodes[0]):
                return c.add_path(nodes[1:])

        self.children.append(nodes[0])
        return nodes[0].find_leaf()

    def __str__(self):
        string = "{0} class=[\"{1}\"] id=\"{2}\"".format(self.tag,
                '","'.join(self.cls if self.cls else []), self.id)

        for c in self.children:
            st = str(c).split("\n")
            child_str = "|---" + st[0] + "\n" + "\n".join([("|   " + s) for s in st[1:]])
            string += "\n" + child_str

        if self.text_blocks:
            for t in self.text_blocks:
                ts = t.get_text()
                string += "\n|---text \"" + t.get_text() + "\""

        return string
