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

    def state(self):
        devices = {}
        for line in (l for l in open(self.file_path, 'rb').xreadlines() if l != ''):
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
