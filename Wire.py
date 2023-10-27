class Wire:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    @property
    def length(self):
        return (self.end[1] - self.begin[1]) ** 2 + (self.end[0] - self.begin[0]) ** 2