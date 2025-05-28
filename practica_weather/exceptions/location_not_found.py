class LocationNotFoundException(Exception):
    def __init__(self, message="The location for the specific city could not be calculated."):
        super().__init__(message)