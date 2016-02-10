#!/usr/bin/env python
"""
The MIT License (MIT)

Copyright (c) 2016 Myles Braithwaite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import configparser
from operator import itemgetter

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
