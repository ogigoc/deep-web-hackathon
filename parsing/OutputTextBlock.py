class OutputTextBlock:
    def __init__(self, text, date, weight, time):
        self.text = text
        self.date = date
        self.weight = weight
        self.time = time

    def __str__(self):
        return '"{0}"'.format(self.text)
