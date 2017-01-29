# -*- coding: utf-8 -*-

import os
import arrow
import codecs
import logging
import shutil
from trillian.app import App
from trillian.templates import Templates
from collections import namedtuple

LOG = logging.getLogger('trillian.lib.writer')

Contact = namedtuple('Contact', ['username', 'print_name'])
Line = namedtuple('Line', ['type', 'text', 'time'])


class Writer(object):

    def __init__(self, me, contact):
        """  """
        self.me = me
        self.contact = contact
        self.args = App().args
        self.config = App().config

        if not getattr(self.contact, 'print_name'):
            self.contact.print_name = self.contact.username

        self.fp = None
        self.tpl = Templates()

    def _open_fp(self, file_path, mode='a+'):
        newly_opened = False
        if not self.fp or self.fp.name != file_path:
            try:
                self.fp.close()
            except AttributeError:
                pass

            LOG.info('Writing log to %s' % file_path)

            newly_opened = True
            self.fp = codecs.open(file_path, mode, encoding='utf8')

        return self.fp, newly_opened

    def _get_filename(self, tpl, line):
        """
        figure out the file that this line should go into
        if the file doesn't exist, write an initial header
        """
        new_file = False

        dt = arrow.get(float(line.time) / 1e3)
        dt = dt.to(self.config.general.timezone)

        wdir = '{wd}/content/category/{cli}'.format(
            wd=self.config.general.working_dir,
            cli=self.contact.username,
        )

        os.makedirs(wdir, exist_ok=True)

        if '.htm' in tpl:
            ext = 'htm'
        elif '.rst' in tpl:
            ext = 'rst'
        elif '.md' in tpl:
            ext = 'md'

        filename = dt.format('YYYY-MM-DD') + '.' + ext
        filename = '{wd}/{filename}'.format(
            wd=wdir, filename=filename
        )

        if not os.path.exists(filename):
            new_file = True
            tpl = self.tpl.render('header.rst.j2',
                                  contact=self.contact,
                                  chat_date=dt.format('YYYY-MM-DD'))
            with open(filename, 'w') as fp:
                fp.writelines(tpl)

        return filename, new_file

    def write_lines(self, lines):
        """  """
        tpl = 'line.rst.j2'

        fname, new_file = self._get_filename(tpl, lines[0])
        fp, newly_opened = self._open_fp(fname)

        lines = self.tpl.render(tpl,
                                contact=self.contact,
                                lines=lines,
                                me=self.me)
        fp.writelines(lines)
        fp.close()

    def write_media(self, media_path, file_name):

        wdir = '{wd}/{cli}/media'.format(
            cli=self.contact.username,
            wd=self.config.general.working_dir,
        )

        os.makedirs(wdir, exist_ok=True)

        try:
            LOG.debug('Moving %s to %s' % (media_path, wdir))
            file_path = '%s/%s' % (wdir, file_name)

            base_name = os.path.basename(media_path)
            name, ext = base_name.split('.')
            file_path = '%s.%s' % (file_path, ext)

            shutil.move(media_path, file_path)
        except:
            # delete the original file
            os.remove(media_path)
            pass
