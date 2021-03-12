from os.path import dirname, abspath
from pprint import pprint

from minindn.apps.application import Application

PYTHON_PATH = abspath(f"{dirname(__file__)}/../venv/bin/python")
SCRIPT_PATH = abspath(f"{dirname(__file__)}/../script/consumer.py")
DATASET_PATH = abspath(f"{dirname(__file__)}/../dataset/nasa_domain.csv")


# noinspection PyPep8Naming
class Consumer(Application):

    def __init__(self, node, logLevel='NONE'):
        Application.__init__(self, node)
        pprint(node.params)

        self.logLevel = node.params['params'].get('nfd-log-level', logLevel)
        self.logFile = 'consumer.log'
        self.sockFile = '/run/{}.sock'.format(node.name)
        self.ndnFolder = '{}/.ndn'.format(self.homeDir)
        self.clientConf = '{}/client.conf'.format(self.ndnFolder)
        self.target_prefix = node.params['params']["target_prefix"]
        try:
            self.consumer_id = f"--consumer_id {node.params['params']['consumer_id']} "
        except KeyError:
            self.consumer_id = ""
        try:
            self.n_consumers = f"--n_consumers {node.params['params']['n_consumers']} "
        except KeyError:
            self.n_consumers = ""
        try:
            self.zipf = f"-z {node.params['params']['zipf']} "
        except KeyError:
            self.zipf = ""
        try:
            self.range = f"-r {node.params['params']['range'][0]} {node.params['params']['range'][1]} "
        except KeyError:
            self.range = ""
        self.command = f"{PYTHON_PATH} {SCRIPT_PATH} -p {self.target_prefix} {self.zipf} {self.range} {self.consumer_id} {self.n_consumers} -- {DATASET_PATH}"

    def start(self, command=None, logfile=None, envDict=None):
        # Application.start(self, 'nfdc cs', logfile=self.logFile)
        if command is None:
            command = self.command
        if logfile is None:
            logfile = self.logFile
        Application.start(self, command=command, logfile=logfile, envDict=envDict)
