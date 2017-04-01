class OutputTextBlock:
    def __init__(self, text, time, weight):
        self.text = text
        self.time = time
        self.weight = weight

    def __str__(self):
        return '"{0}"'.format(self.text)
