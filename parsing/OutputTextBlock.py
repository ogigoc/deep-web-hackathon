class OutputTextBlock:
    def __init__(self, text, date, weight):
        self.text = text
        self.date = date
        self.weight = weight

    def __str__(self):
        return '"{0}"'.format(self.text)
