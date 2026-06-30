# apps/authentication/events.py

class UserCreated:
    def __init__(self, user):
        self.user = user

class UserUpdated:
    def __init__(self, user):
        self.user = user

class UserDeactivated:
    def __init__(self, user):
        self.user = user

class EventDispatcher:
    @staticmethod
    def dispatch(event):
        # منطق إرسال الحدث عبر الـ Event-Driven Bus (إن وجد)
        pass