#!/usr/bin/env python3
from os.path import abspath, dirname

from minindn.apps.app_manager import AppManager
from minindn.apps.nlsr import Nlsr
from minindn.helpers.ip_routing_helper import IPRoutingHelper
from minindn.minindn import Minindn
from minindn.util import MiniNDNCLI
from mininet.log import setLogLevel, info

from applications.consumer import Consumer
from applications.nfd import Nfd
from applications.pingserver import PingServer
from applications.producer import Producer

TOPOLOGY_FILE = abspath(f"{dirname(__file__)}/topology.conf")

if __name__ == '__main__':
    setLogLevel('debug')

    Minindn.cleanUp()
    Minindn.verifyDependencies()

    ndn = Minindn(topoFile=TOPOLOGY_FILE)

    traffic_generators = {host.name: host for host in ndn.net.hosts if host.name != "b"}
    traffic_generators["a"].params["params"].update({
        "consumer_id": 0,
        "n_consumers": 2,
        "range": (0, 3500),
        "target_prefix": "/ndn/c-site/c/producer",
        "zipf": 1.2
    })
    traffic_generators["c"].params["params"].update({
        "consumer_id": 1,
        "n_consumers": 2,
        "range": (0, 3500),
        "target_prefix": "/ndn/a-site/a/producer",
        "zipf": 1.2
    })

    ndn.start()

    info('Starting NFD on nodes\n')
    nfds = AppManager(ndn, ndn.net.hosts, Nfd)

    Minindn.sleep(2)

    info('Starting NLSR on nodes\n')
    nlsrs = AppManager(ndn, ndn.net.hosts, Nlsr)

    Minindn.sleep(2)

    info('Starting NDN ping server on nodes\n')
    ping_servers = AppManager(ndn, ndn.net.hosts, PingServer)
    info('Starting producer on nodes\n')
    producers = AppManager(ndn, traffic_generators.values(), Producer)
    info('Starting consumers on nodes\n')
    consumers = AppManager(ndn, traffic_generators.values(), Consumer)

    # Calculate all routes for IP routing
    IPRoutingHelper.calcAllRoutes(ndn.net)
    info("IP routes configured, start ping\n")

    ndn.net.pingAll()

    MiniNDNCLI(ndn.net)

    ndn.stop()
