class Diskstats(object):
    file_path = '/proc/diskstats'

    columns_disk = ['reads reqs',
                    'reads merged',
                    'reads sector',
                    'reads time',
                    'writes reqs',
                    'writes merged',
                    'writes sector',
                    'writes time',
                    'io reqs',
                    'io time',
                    'io weighted']

    def __init__(self, interval):
        self.old_devices = None
        self.interval = interval

    def measure(self):
        devices = {}
        with open(self.file_path, 'rb') as f:
            for line in (l for l in f if l != ''):
                parts = line.split()
                device = parts[2]
                parts = parts[3:]
                data = dict(zip(self.columns_disk, parts))

                if 'ram' in device:
                    continue
                elif 'loop' in device:
                    continue

                devices[device] = dict((k, int(v)) for k, v in data.iteritems())

        return devices

    def state(self):
        state = self.measure()
        if self.old_devices is not None:
            delta_state = state.copy()
            for device, stats in state.iteritems():
                for service, metric in stats.iteritems():
                    delta = metric - self.old_devices[device][service]

                    if 'io reqs' in service:
                        continue
                    if 'io time' in service:
                        delta_state[device][service] = float(delta) / (self.interval * 1000)
                        continue
                    delta_state[device][service] = float(delta) / self.interval

            return delta_state

        self.old_devices = state
        return state
