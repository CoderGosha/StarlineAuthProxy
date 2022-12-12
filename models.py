class SyncLogs:
    def __init__(self, app_name, request_id, logs):
        self.logs = logs
        self.request_id = request_id
        self.app_name = app_name

    def __str__(self):
        return f"{self.request_id} - {self.app_name} with logs: {self.logs}"
