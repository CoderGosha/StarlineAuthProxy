import base64
import json


class SyncLogs:
    def __init__(self, app_name, request_id, logs):
        self.logs = logs
        self.request_id = request_id
        self.app_name = app_name

    def __get_logs_from_base_64__(self):
        if self.logs is not None and len(self.logs) > 0:
            try:
                base64_bytes = self.logs.encode('utf8')
                message_bytes = base64.b64decode(base64_bytes)
                message = message_bytes.decode('utf8')
                return json.loads(message)
            except:
                return self.logs

    def __str__(self):
        return f"{self.request_id} - {self.app_name} with logs: {self.__get_logs_from_base_64__()}"
