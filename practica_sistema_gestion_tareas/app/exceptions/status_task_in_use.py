class StatusTaskInUseException(Exception):
    def __init__(self, message="The status of the task is currently in use and cannot be deleted."):
        super().__init__(message)