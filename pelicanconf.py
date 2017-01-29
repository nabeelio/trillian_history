#

AUTHOR = ''
SITENAME = 'trillian logs'
SITEURL = 'index.html'

# options are taken/set from there as well
THEME = 'pelican/themes/pelican-elegant-1.3'
# CUSTOM_CSS = 'main.css'

PATH = 'tmp/'

# general settings
MAIN_MENU = True
TYPOGRIFY = True
TIMEZONE = 'US/Central'
USE_FOLDER_AS_CATEGORY = True
DELETE_OUTPUT_DIRECTORY = False

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True

PLUGIN_PATHS = ['pelican/plugins']
PLUGINS = ['autopages', 'tipue_search', 'sitemap']

# FORMATTED_FIELDS = [
#     'summary'
# ]

# default theme: https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3
# this theme allows you to chose a sub-theme
# http://bootswatch.com
# THEME = '../pelican-themes/pelican-bootstrap3'
# BOOTSTRAP_THEME = 'flatly'

# use the fluid layout
# BOOTSTRAP_FLUID = True
# SHOW_ARTICLE_AUTHOR = False
# SHOW_ARTICLE_CATEGORY = False

