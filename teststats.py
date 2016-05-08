from metrics import diskstats
from metrics import netstats
from metrics import health


def main():
    # for device, stats in diskstats.state().iteritems():
    #     print device
    #     for name, stat in stats.iteritems():
    #         print '    %s: %s' % (name, stat)
    #
    # for interface, stats in netstats.state().iteritems():
    #     print interface
    #     for name, stat in stats.iteritems():
    #         print '    %s: %s' % (name, stat)
    # for disk, percent in health.disk().iteritems():
    #     print 'disk %s is %s full' % (disk, percent)
    # health.linux_memory()
    print health.linux_load()

if __name__ == '__main__':
    main()

