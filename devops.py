import random
try:
    from urllib import urlencode
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urlencode, urljoin

from errbot import BotPlugin, botcmd

import requests
from pyquery import PyQuery


class DevOpsReactions(BotPlugin):

    @botcmd
    def devops(self, msg, args):
        """Return a gif based on search

        Return a random gif if no search query is specified.

        Example:
        !devops live migration
        !devops oops-wrong-cable
        !devops
        """

        base = 'http://devopsreactions.tumblr.com/'
        if args:
            q = urlencode({'q': args})
            path = '?' + q
        else:
            path = 'random'
        url = urljoin(base, path)
        r = requests.get(url)
        self.log.debug('url sent: {}'.format(r.url))

        if r.ok:
            dom = PyQuery(r.content)
            results = dom('div[class=post_title] a')
            self.log.debug('results found: {}'.format(len(results)))
        else:
            results = []

        if results:
            item = random.choice(results)
            img = item.get('href')
            response = img
        else:
            response = 'No results found.'

        self.send(msg.frm,
                  response,
                  message_type=msg.type,
                  in_reply_to=msg,
                  groupchat_nick_reply=True)
