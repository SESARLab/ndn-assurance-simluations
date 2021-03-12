from minindn.apps.application import Application


# noinspection PyPep8Naming
class PingServer(Application):

    def __init__(self, node, logLevel='NONE'):
        Application.__init__(self, node)

        self.logLevel = node.params['params'].get('nfd-log-level', logLevel)
        self.logFile = 'example.log'
        self.sockFile = '/run/{}.sock'.format(node.name)
        self.ndnFolder = '{}/.ndn'.format(self.homeDir)
        self.clientConf = '{}/client.conf'.format(self.ndnFolder)
        self.prefix = f"/ndn/{node.name}-site/{node.name}"
        self.command = f"ndnpingserver {self.prefix}"

    def start(self, command=None, logfile=None, envDict=None):
        if command is None:
            command = self.command
        if logfile is None:
            logfile = self.logFile
        Application.start(self, command=command, logfile=logfile, envDict=envDict)
