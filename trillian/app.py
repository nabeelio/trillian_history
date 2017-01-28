#
import os
import yaml
import logging
import argparse
from os import path
from addict import Dict

from .lib.singleton import Singleton

logging.basicConfig(format='%(asctime)s - '
                           '%(name)s:%(lineno)d - '
                           '%(levelname)s - %(message)s',
                    level=logging.INFO)

LOG = logging.getLogger(__name__)


class App(object, metaclass=Singleton):

    def __init__(self):
        self._args = None
        self._config = None

    @property
    def args(self):
        """
        """
        if self._args:
            return self._args

        parser = argparse.ArgumentParser()
        parser.add_argument('--conf', default='config.yml')
        parser.add_argument('--log-level', default='DEBUG')
        parser.add_argument('--test-mode', default=False, action='store_true')

        parser.add_argument('--logs-source', default=None)
        parser.add_argument('--dest', default='tmp/')

        self._args = parser.parse_args()
        return self._args

    @property
    def config(self):
        """
        :rtype: dict
        """
        if self._config:
            return self._config

        file = self.args.conf
        LOG.info('Looking for %s' % file)

        # search each directory going up one dir at a time
        dirs = path.split(path.abspath(__file__))
        dirs = path.split(dirs[0])
        while dirs:
            if dirs[0] == '/' and not dirs[1]:
                break

            fpath = '/'.join(dirs) + '/' + file
            dirs = path.split(dirs[0])

            try:
                with open(fpath) as f:
                    config = yaml.load(f)
                    self._config = Dict(config)
                    LOG.info('Config %s loaded' % fpath)
                    break
            except NotADirectoryError:
                continue
            except FileNotFoundError:
                continue
            except Exception as e:
                LOG.exception(e)
                exit(-1)

        return self._config

    def run(self):
        """ application entry point """
        LOG.info(self.args)
        LOG.info(self.config)

        # set the proper log level
        self.args.log_level = self.args.log_level.upper()
        LOG.setLevel(getattr(logging, self.args.log_level))

        self.args.logs_source = os.path.expanduser(self.args.logs_source)
        if not os.path.exists(self.args.logs_source):
            print('Log directory does not exist!')
            exit(-1)

        from trillian.history import TrillianHistory
        history = TrillianHistory()
        history.run()


def main():
    a = App()
    a.run()
