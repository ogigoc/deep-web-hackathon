class TextBlock:
    def __init__(self, element, weight, parent, date = None):
        self.text = None
        self.element = element
        self.weight = weight
        self.parent = parent
        self.date = date

    def get_text(self):
        if not self.text:
            self.text = self.element.get_text(" ").strip()
        return self.text

    def equals(self, other):
        return self.element == other.element
