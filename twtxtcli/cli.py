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

import argparse

from clint.textui import puts, indent, colored, columns

import humanize

from . import __project_name__, __version__
from .twtxt import TwTxt


twtxt = TwTxt()


def follow(nick, url):
    twtxt.follow(nick, url)
    puts(colored.green('followed {0}'.format(nick)))


def following():
    sources = twtxt.following()

    for source in sources:
        puts(colored.blue(source.nick))

        with indent(2):
            puts(source.url)


def unfollow(nick):
    twtxt.unfollow(nick)
    puts(colored.red('unfollowed {0}'.format(nick)))


def timeline():
    timeline = twtxt.timeline()

    for tweet in timeline:
        puts(columns(
            [colored.black(tweet['nick'], bold=True), 10],
            [colored.magenta(humanize.naturaldate(tweet['timestamp'])), 10],
            [tweet['text'], 59]
        ))


def view(nick):
    source = twtxt.view(nick)

    puts("@{0} - {1}".format(colored.black(source.nick, bold=True),
                             source.url))

    for tweet in source.get_tweets():
        puts(columns(
            [colored.magenta(humanize.naturaldate(tweet['timestamp'])), 10],
            [tweet['text'], 69]
        ))


def main():
    parser = argparse.ArgumentParser(prog="{0} v{1}.".format(__project_name__,
                                                             __version__))

    subparsers = parser.add_subparsers()

    parser_timeline = subparsers.add_parser('timeline',
                                            help="retrieve your personal "
                                                 " timeline")
    parser_timeline.set_defaults(which='timeline')

    parser_view = subparsers.add_parser('view',
                                        help="view the timeline of one of "
                                             "your sources")
    parser_view.set_defaults(which='view')
    parser_view.add_argument('nick', type=str)

    parser_follow = subparsers.add_parser('follow',
                                          help="add a new source to your "
                                               "followings")
    parser_follow.set_defaults(which='follow')
    parser_follow.add_argument('--nick', dest='follow_nick', required=True)
    parser_follow.add_argument('--url', dest='follow_url', required=True)

    parser_following = subparsers.add_parser('following',
                                             help="return the list of sources "
                                                  "you are following")
    parser_following.set_defaults(which='following')

    parser_unfollow = subparsers.add_parser('unfollow',
                                            help="unfollow an existing source")
    parser_unfollow.set_defaults(which='unfollow')
    parser_unfollow.add_argument('nick', type=str)

    args = parser.parse_args()

    if args.which == 'timeline':
        timeline()

    if args.which == 'follow':
        follow(args.follow_nick, args.follow_url)

    if args.which == 'following':
        following()

    if args.which == 'unfollow':
        unfollow(args.nick)

    if args.which == 'view':
        view(args.nick)
