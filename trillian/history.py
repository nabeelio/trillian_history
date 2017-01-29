#
import os
import re
from os import scandir

from trillian.app import App
from trillian.lib.singleton import Singleton

from trillian.lib import reader
from trillian.lib import writer


class TrillianHistory(metaclass=Singleton):

    def __init__(self):
        """ """
        self.app = App()

        self.writers = {}
        self.log_files = {}
        self.log_root = os.path.join(
            self.app.args.logs_source,
            '_CLOUD'
        )

        self.me = writer.Contact(username='me', print_name='me')

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
                        contact = writer.Contact(username=username,
                                                 print_name=username)

                        self.log_files[username] = {
                            'contact': contact,
                            'files': [],
                        }

                    self.log_files[username]['files'].append(entry.path)

        scan_dir(self.log_root)

    def _parse_file(self, writer, file):
        """
        :type writer: trillian.lib.writer.Writer
        """
        xml = reader.Reader(file)
        lines = [line for line in xml.read_lines()]

        writer.write_lines(lines)

    def run(self):
        """ """

        self._find_all_xmls(self.log_root)

        for username, details in self.log_files.items():
            if username not in self.writers:
                self.writers[username] = writer.Writer(
                    self.me,
                    details['contact']
                )

            for file in details['files']:
                self._parse_file(
                    self.writers[username],
                    file
                )


