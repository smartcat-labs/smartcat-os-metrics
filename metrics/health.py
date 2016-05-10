from subprocess import check_output
import re


class Health(object):
    def __init__(self):
        self.old_cpu = None
        self.cores = self.get_cores()
        if self.cores is None:
            self.cores = 1

    def disk(self):
        df = check_output("df -P --exclude-type=iso9660", shell=True)

        result = {}
        for line in (l for l in df.split('\n') if l != ''):
            f = line.split()
            if f[0] == 'Filesystem':
                continue
            if not f[0].startswith('/'):
                continue

            drive = f[5]
            # Calculate capacity
            percent = float(f[4].replace('%', ''))/100

            result[drive] = percent

        return result

    def get_cores(self):
        file_path = '/proc/cpuinfo'

        cores = 0;
        for line in (l for l in open(file_path, 'rb').xreadlines() if l != ''):
            if line.lower().startswith(b'processor'):
                cores += 1

        if cores == 0:
            search = re.compile('cpu\d')
            for line in (l for l in open('/proc/stat', 'rb').xreadlines() if l != ''):
                line = line.split(' ')[0]
                if search.match(line):
                    cores += 1

        if cores == 0:
            return None

        return cores

    def linux_cpu(self):
        file_path = '/proc/stat'

        with open(file_path, 'rb') as f:
            cpu_line = f.readline()
            if cpu_line == '':
                raise ValueError("There is no cpu line")

            data = cpu_line.split()
            u2 = int(data[1])
            n2 = int(data[2])
            s2 = int(data[3])
            i2 = int(data[4])

            if self.old_cpu:
                u1, n1, s1, i1 = self.old_cpu

                used = (u2+n2+s2) - (u1+n1+s1)
                total = used + i2-i1
                fraction = float(used) / total

                return fraction

            self.old_cpu = [u2, n2, s2, i2]

    def linux_load(self):
        file_path = '/proc/loadavg'

        with open(file_path, 'rb') as f:
            load_line = f.readline()
            parts = load_line.split()
            result = float(parts[0])/self.cores

            return result

    def linux_memory(self):
        file_path = '/proc/meminfo'

        data = {}
        with open(file_path, 'rb') as f:
            for line in (l for l in f if l != ''):
                parts = line.split()
                data[parts[0].replace(':', '')] = int(parts[1])

        free = data['MemFree'] + data['Buffers'] + data['Cached']
        total = data['MemTotal']

        fraction = 1 - (float(free) / total)

        return fraction
