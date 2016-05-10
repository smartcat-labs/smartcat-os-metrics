import reporter
import click
import logging
import sys

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] %(name)-12s: %(message)s')


log = logging.getLogger(__name__)


@click.command()
@click.version_option(version=reporter.__version__)
@click.option('--host', '-h', type=click.STRING, default='localhost',
              envvar='RIEMANN_HOST', help='Riemann server hostname.')
@click.option('--port', '-p', type=click.INT, default=5555,
              envvar='RIEMANN_PORT', help='Riemann server port.')
@click.option('--interval', '-i', type=click.INT, default=1,
              help='Interval for sending os metrics in SECONDS.')
@click.option('--debug', '-d', flag_value='debug',
              help='Debug mode for printing out log')
def main(host, port, interval, debug):
    log.info("Starting metrics reporter")
    log.info("Reporting to host:port at %s:%s" % (host, port))
    log.info("Sending at interval of %s seconds" % interval)
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        log.debug("Debug mode is enabled")
    sender = reporter.MetricsReporter(host, port, interval)
    sender.run()

if __name__ == '__main__':
    main()
