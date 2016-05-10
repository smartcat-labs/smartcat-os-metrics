from riemann_client.client import *
from riemann_client.transport import *
from metrics import *

import time
import sys
import logging


log = logging.getLogger(__name__)


class MetricsReporter(object):
    def __init__(self, host="localhost", port=5555, interval=1):
        self.host = host
        self.port = port
        self.interval = interval
        self.client = AutoFlushingQueuedClient(UDPTransport(self.host, self.port))
        self.client.transport.connect()

        self.diskstats = Diskstats()
        self.health = Health()
        self.netstats = Netstats()

    def add_event(self, state, service, metric):
        self.client.event(state=state, service=service, metric_f=metric, ttl=10)

    def run(self):
        while True:
            try:
                self.measure()
                time.sleep(self.interval)
            except KeyboardInterrupt:
                log.info('BYE BYE!!!')
                sys.exit()

    def measure(self):
        for device, stats in self.diskstats.state().iteritems():
            for name, stat in stats.iteritems():
                self.add_event("ok", "diskstats %s %s" % (device, name), stat)
                log.debug("diskstats %s %s" % (device, name) + " " + str(stat))

        for interface, stats in self.netstats.state().iteritems():
            for name, stat in stats.iteritems():
                self.add_event("ok", "%s %s" % (interface, name), stat)
                log.debug("%s %s" % (interface, name) + " " + str(stat))

        cpu = self.health.linux_cpu()
        if cpu is not None:
            self.add_event("ok", "cpu", cpu)
            log.debug("%s %s" % ("cpu", cpu))

        load = self.health.linux_load()
        self.add_event("ok", "load", load)
        log.debug("%s %s" % ("load", load))

        memory = self.health.linux_memory()
        self.add_event("ok", "memory", memory)
        log.debug("%s %s" % ("memory", memory))
