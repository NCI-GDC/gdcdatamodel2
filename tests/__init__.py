class MockSubmissionEntity:
    def __init__(self):
        self.errors = []
        self.node = None
        self.doc = {}

    def record_error(self, message, **kwargs):
        self.errors.append(dict(message=message, **kwargs))
