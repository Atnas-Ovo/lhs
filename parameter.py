class Parameter:
    def __init__(self, id, data_type, min_value, max_value, enum_values):
        self.id = id
        self.data_type = data_type
        self.min = min_value
        self.max = max_value
        self.enum_values = enum_values