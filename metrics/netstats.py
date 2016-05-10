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

    def state(self):
        net = open(self.file_path, 'rb')
        header = net.readline()
        if not header.count('|'):
            raise ValueError("Header was not in the expected format")
        label = net.readline().strip("\n")

        interfaces = {}
        for info in net.readlines():
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
