from subprocess import check_output


def stat():
    return None


def disk():
    df = check_output("df -P --exclude-type=iso9660", shell=True)

    result = {}
    for line in (l for l in df.split('\n') if l != ''):
        f = line.split()
        if f[0] == 'Filesystem':
            continue
        if not f[0].startswith('/'):
            continue

        print f
        drive = f[5]
        # Calculate capacity
        percent = float(f[4].replace('%', ''))/100

        result[drive] = percent

    return result


# def linux_cpu():
#     new = File.read('/proc/stat')
#     unless new[/cpu\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)/]
#         alert 'cpu', :unknown, nil, "/proc/stat doesn't include a CPU line"
#         return false
#     end
#     u2, n2, s2, i2 = [$1, $2, $3, $4].map { |e| e.to_i }
#
#     if @old_cpu
#         u1, n1, s1, i1 = @old_cpu
#
#         used = (u2+n2+s2) - (u1+n1+s1)
#         total = used + i2-i1
#         fraction = used.to_f / total
#
#         report_pct :cpu, fraction, "user+nice+system\n\n#{`ps -eo pcpu,pid,comm | sort -nrb -k1 | head -10`.chomp}"
#     end
#
#     @old_cpu = [u2, n2, s2, i2]
# end
def linux_cpu():
    file_path = '/proc/stat'

    stat = open(file_path, 'rb')
    cpu_line = stat.readline()
    if cpu_line == '':
        raise ValueError("There is no cpu line")

    u2 = cpu_line[1]
    n2 = cpu_line[2]
    s2 = cpu_line[3]
    i2 = cpu_line[4]


def linux_load():
    file_path = '/proc/loadavg'

    result = float(0)
    for line in (l for l in open(file_path, 'rb').xreadlines() if l != ''):
        parts = line.split()
        result = float(parts[0])

    return result


def linux_memory():
    file_path = '/proc/meminfo'

    data = {}
    for line in (l for l in open(file_path, 'rb').xreadlines() if l != ''):
        parts = line.split()
        data[parts[0].replace(':', '')] = int(parts[1])

    free = data['MemFree'] + data['Buffers'] + data['Cached']
    total = data['MemTotal']

    fraction = 1 - (float(free) / total)

    return fraction
