import reporter
import click


@click.command()
@click.version_option(version=reporter.__version__)
@click.option('--host', '-h', type=click.STRING, default='localhost',
              envvar='RIEMANN_HOST', help='Riemann server hostname.')
@click.option('--port', '-p', type=click.INT, default=5555,
              envvar='RIEMANN_PORT', help='Riemann server port.')
@click.option('--interval', '-i', type=click.INT, default=1,
              help='Interval for sending os metrics in SECONDS.')
def main(host, port, interval):
    print("Starting metrics reporter")
    print("Reporting to host:port at %s:%s" % (host, port))
    print("Sending at interval of %s seconds" % interval)
    sender = reporter.MetricsReporter(host, port, interval)
    sender.run()

if __name__ == '__main__':
    main()
