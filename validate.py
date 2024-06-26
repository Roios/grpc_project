class Error(ValueError):

    def __init__(self, field, reason):
        super().__init__(f'{field}: {reason}')
        self.field = field
        self.reason = reason


def start_request(request):
    if not request.client_id:
        raise Error('client_id', 'empty')
