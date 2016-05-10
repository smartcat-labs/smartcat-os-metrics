class Netstats(object):
    file_path = '/proc/net/dev'

    columns_net = ['rx bytes',
                   'rx packets',
                   'rx errs',
                   'rx drop',
                   'rx fifo',
                   'rx frame',
                   'rx compressed',
                   'rx multicast',
                   'tx bytes',
                   'tx packets',
                   'tx errs',
                   'tx drops',
                   'tx fifo',
                   'tx colls',
                   'tx carrier',
                   'tx compressed']

    def __init__(self):
        self.old_interfaces = None

    def state(self):
        with open(self.file_path, 'rb') as f:
            header = f.readline()
            if not header.count('|'):
                raise ValueError("Header was not in the expected format")
            label = f.readline().strip("\n")

            interfaces = {}
            for info in f.readlines():
                info = info.strip("\n")

                # split the data into interface name and counters
                (name, data) = info.split(":", 1)

                # clean them up
                name = name.strip()
                if name == 'lo':
                    continue
                values = dict(zip(self.columns_net, data.split()))

                interfaces[name] = dict((k, int(v)) for k, v in values.iteritems())

            return interfaces
