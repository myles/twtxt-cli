#!/usr/bin/env python
"""
Copyright (c) 2014, Myles Braithwaite <me@mylesbraithwaite.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in
  the documentation and/or other materials provided with the
  distribution.

* Neither the name of the Monkey in your Soul nor the names of its
  contributors may be used to endorse or promote products derived
  from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import os
import configparser
from operator import itemgetter, attrgetter

import iso8601
import requests

from clint import resources

resources.init('myles', 'twtxt')

class TwTxt(object):
    def __init__(self):
        self.config_path = os.path.join(resources.user.path, 'config')

        raw_config = resources.user.read('config')
        self.config = configparser.ConfigParser()
        self.config.read_string(raw_config)

    def follow(self, nick, url, replace=False):
        if self.config.has_option('following', nick) and not replace:
            raise Exception('there is already a user by that nick')

        twtxt_file = requests.get(url)

        if not twtxt_file.ok:
            raise twtxt_file.raise_for_status()

        self.config.set('following', nick, url)

        with open(self.config_path, 'w') as f:
            self.config.write(f)

    def unfollow(self, nick):
        self.config.remove_option('following', nick)

        with open(self.config_path, 'w') as f:
            self.config.write(f)

    def following(self):
        config_section = 'following'
        config_following = self.config[config_section]

        following = []

        for nick in config_following:
            url = self.config.get(config_section, nick)
            following.append(Source(nick=nick, url=url))

        return following

    def view(self, nick, reverse=True):
        url = self.config.get('following', nick)
        return Source(nick, url)

    def me(self, reverse=True):
        source = Source(self.config.get('twtxt', 'nick'),
                        self.config.get('twtxt', 'twturl'))

        return source

    def timeline(self, reverse=True):
        tweets = []

        for s in self.following():
            source = Source(s.nick, s.url)
            tweets += source.get_tweets()

        tweets += self.me().get_tweets()

        return sorted(tweets, key=itemgetter('timestamp'), reverse=reverse)


class Source(object):
    """a twtxt source"""
    def __init__(self, nick, url):
        self.nick = nick
        self.url = url

    def get_tweets(self, reverse=True):
        if self.url.startswith('http'):
            twtxt_file = requests.get(self.url)

            if not twtxt_file.ok:
                raise twtxt_file.raise_for_status()
        elif os.path.exists(self.url):
            with open(os.path.expanduser(self.url), 'r') as f:
                twtxt_file = f.read()

        tweets = []

        for line in twtxt_file.text.split('\n'):
            try:
                time, text = line.split('\t')
                tweets.append({
                    'timestamp': iso8601.parse_date(time),
                    'text': text,
                    'nick': self.nick
                })
            except ValueError:
                pass

        return sorted(tweets, key=itemgetter('timestamp'), reverse=reverse)

