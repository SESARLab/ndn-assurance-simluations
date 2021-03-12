from minindn.apps.application import Application
from minindn.apps.nfd import Nfd as OrigNfd


class Nfd(OrigNfd):
    def start(self):
        Application.start(self, f"nfd --config {self.confFile}", logfile=self.logFile)
