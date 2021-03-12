from os.path import dirname, abspath

from minindn.apps.application import Application

PYTHON_PATH = abspath(f"{dirname(__file__)}/../venv/bin/python")
SCRIPT_PATH = abspath(f"{dirname(__file__)}/../script/producer.py")


# noinspection PyPep8Naming
class Producer(Application):

    def __init__(self, node, logLevel='NONE'):
        Application.__init__(self, node)

        self.logLevel = node.params['params'].get('nfd-log-level', logLevel)
        self.logFile = 'producer.log'
        self.sockFile = '/run/{}.sock'.format(node.name)
        self.ndnFolder = '{}/.ndn'.format(self.homeDir)
        self.clientConf = '{}/client.conf'.format(self.ndnFolder)
        self.prefix = f"/ndn/{node.name}-site/{node.name}/producer"
        self.command = f"{PYTHON_PATH} {SCRIPT_PATH} -p {self.prefix}"

    def start(self, command=None, logfile=None, envDict=None):
        # Application.start(self, 'nfdc cs', logfile=self.logFile)
        if command is None:
            command = self.command
        if logfile is None:
            logfile = self.logFile
        Application.start(self, command=command, logfile=logfile, envDict=envDict)
