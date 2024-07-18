
from . import db
from datetime import datetime

class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password = password
        self.is_active = is_active

    def __repr__(self):
        return f'<User {self.username}>'

class LogData:
    def __init__(self, username, logtype):
        self.username = username
        self.timestamp = datetime.utcnow()
        self.logtype = logtype

    def __repr__(self):
        return f'<LogData {self.username} {self.logtype} at {self.timestamp}>'
