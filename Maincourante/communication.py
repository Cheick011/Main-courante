from .synchronisation import SyncManager
from .multicast import MulticastReceiver, MulticastSender


class CommunicationModule:

    def __init__(self):
        self.sync = SyncManager()
        self.receiver = MulticastReceiver(self.sync)

    def start(self):
        self.receiver.start()
        print(" Module de communication démarré")

    def send_update(self, action, table, payload):
        MulticastSender.send_update(action, table, payload)

    def request_full_sync(self):
        MulticastSender.request_full_sync()
