#
import html
import urllib
from xml.etree import cElementTree
import xml.sax.saxutils as saxutils

from trillian.lib.writer import Line


class Reader(object):

    def __init__(self, file):
        """ """
        self.file = file
        with open(file, 'r') as file:
            text = file.read()

        text = '<messages>{xml}</messages>'.format(
            xml=text
        )

        self.tree = cElementTree.fromstring(text)

    def _clean_text(self, text):
        text = html.unescape(text)
        text = urllib.parse.unquote(text)

        # if '*' in text:
        #     text = text.replace('*', '\*')

        return text

    def read_lines(self):
        """ """
        metadata = self.tree.find('history')
        week = metadata.attrib['week']
        year = metadata.attrib['year']

        for message in self.tree.findall('message'):
            text = self._clean_text(message.attrib['text'])
            line = Line(type=message.attrib['type'],
                        time=message.attrib['time'],
                        text=text)
            yield line
