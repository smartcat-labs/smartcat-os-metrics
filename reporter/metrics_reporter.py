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
        self.client = Client(TCPTransport(self.host, self.port))

        self.diskstats = Diskstats(self.interval)
        self.health = Health()
        self.netstats = Netstats(self.interval)

    def add_event(self, state, service, metric):
        self.client.event(state=state, service=service, metric_f=metric, ttl=10)

    def run(self):
        while True:
            if not self.is_connected():
                self.try_connect()

            try:
                self.measure()
            except (socket.error, struct.error):
                log.error('Failed to report measurement')
                self.client.transport.disconnect()
                self.client = None
            time.sleep(self.interval)

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

    def try_connect(self):
        if self.client is None:
            self.client = Client(TCPTransport(self.host, self.port))

        while not self.is_connected():
            log.info('Trying to connect')
            try:
                self.client.transport.connect()
            except socket.error:
                log.info('Failed to connect. Sleeping 10 seconds')
                time.sleep(10)

        log.info('Connected to server')

    def is_connected(self):
        try:
            self.client.transport.socket.type
            return True
        except (AttributeError, RuntimeError, socket.error):
            return False
