class LexisAnalyzer:
    def __init__(self, determinants):
        self.determinants = determinants

    def analyze(self, string):
        result = []

        for i in range(len(string)):
            result += [sum([d(string[i:]) for d in self.determinants], [])]

        return result
