from subprocess import check_output


class Health(object):
    def __init__(self):
        self.old_cpu = None

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

    def linux_cpu(self):
        file_path = '/proc/stat'

        stat = open(file_path, 'rb')
        cpu_line = stat.readline()
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

        result = float(0)
        for line in (l for l in open(file_path, 'rb').xreadlines() if l != ''):
            parts = line.split()
            result = float(parts[0])

        return result

    def linux_memory(self):
        file_path = '/proc/meminfo'

        data = {}
        for line in (l for l in open(file_path, 'rb').xreadlines() if l != ''):
            parts = line.split()
            data[parts[0].replace(':', '')] = int(parts[1])

        free = data['MemFree'] + data['Buffers'] + data['Cached']
        total = data['MemTotal']

        fraction = 1 - (float(free) / total)

        return fraction
