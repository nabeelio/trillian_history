#
import os
import re
from os import scandir

from trillian.app import App
from trillian.lib import writer
from trillian.lib.singleton import Singleton


class TrillianHistory(metaclass=Singleton):

    def __init__(self):
        """ """
        self.app = App()

        self.log_files = {}
        self.log_root = os.path.join(
            self.app.args.logs_source,
            '_CLOUD'
        )

    def _find_all_xmls(self, log_root):
        """
        recursive look down the log path and find all the xmls
        order them in a dict, with the key being
        """
        def scan_dir(dir):
            for entry in scandir(dir):
                if entry.is_dir():
                    scan_dir(entry.path)
                    continue

                # what to skip?
                if entry.name.startswith('.'):
                    continue

                if '.xml' in entry.name:
                    parts = re.split('-|\.', entry.name)
                    service, username, _ = parts
                    if username not in self.log_files:
                        self.log_files[username] = {
                            'contact': writer.Contact(username=username,
                                                      print_name=username),
                            'files': []
                        }

                    self.log_files[username]['files'].append(entry.path)

        scan_dir(self.log_root)

    def run(self):
        """ """
        self._find_all_xmls(self.log_root)

        for username, details in self.log_files.items():
            pass
