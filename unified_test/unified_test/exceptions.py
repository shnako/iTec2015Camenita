# Exception used to signal that an error has occurred in the processing
# of a request and that the specified message should be handled.
# Can also specify the response_code and **will default to 400 Bad Request if response_code not specified**.
class UnifiedTestRequestException(Exception):
    # Need to specify the message as well, otherwise the message will be interpreted as the response_code.
    def __init__(self, message="", response_code=400):
        self.message = message
        self.response_code = response_code