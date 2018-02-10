class TooBigNumbersError(Exception):
    def __init__(self, function_index):
        self.function_index = function_index
