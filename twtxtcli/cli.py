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

import argparse

from clint.textui import puts, indent, colored, columns

import humanize

from . import (__project_name__, __project_link__, __project_usage__,
               __version__)
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


def timeline(reverse):
    timeline = twtxt.timeline(reverse=reverse)

    for tweet in timeline:
        tweet.process_text()

        puts(columns(
            [colored.black(tweet.source.nick, bold=True), 10],
            [colored.magenta(humanize.naturaldate(tweet.timestamp)), 10],
            [tweet.text, 59]
        ))


def view(nick, reverse):
    source = twtxt.view(nick, reverse=reverse)

    puts("@{0} - {1}".format(colored.black(source.nick, bold=True),
                             source.url))

    for tweet in source.get_tweets():
        puts(columns(
            [colored.magenta(humanize.naturaldate(tweet.timestamp)), 10],
            [tweet.text, 69]
        ))


def info(nick):
    info = twtxt.view(nick)

    puts("@{0} - {1}".format(colored.black(info.nick, bold=True),
                             info.url))


def tweet(tweet):
    twtxt.tweet(tweet)


def main():
    parser = argparse.ArgumentParser(usage=__project_usage__,
                                     description=__project_link__,
                                     prog="{0} v{1}.".format(__project_name__,
                                                             __version__))

    subparsers = parser.add_subparsers()

    parser_timeline = subparsers.add_parser('timeline',
                                            help="retrieve your personal "
                                                 " timeline")
    parser_timeline.set_defaults(which='timeline')
    parser_timeline.add_argument('-r', '--reverse',
                                 dest='timeline_reverse', action='store_false',
                                 help="view in decending order")

    parser_view = subparsers.add_parser('view',
                                        help="view the timeline of one of "
                                             "your sources")
    parser_view.set_defaults(which='view')
    parser_view.add_argument('nick', type=str)
    parser_view.add_argument('-r', '--reverse', dest='view_reverse',
                             action='store_false', help="view in decending "
                                                        "order")

    parser_follow = subparsers.add_parser('follow',
                                          help="add a new source to your "
                                               "followings")
    parser_follow.set_defaults(which='follow')
    parser_follow.add_argument('-n', '--nick', dest='follow_nick',
                               required=True, type=str)
    parser_follow.add_argument('-u', '--url', dest='follow_url',
                               required=True, type=str)

    parser_following = subparsers.add_parser('following',
                                             help="return the list of sources "
                                                  "you are following")
    parser_following.set_defaults(which='following')

    parser_unfollow = subparsers.add_parser('unfollow',
                                            help="unfollow an existing source")
    parser_unfollow.set_defaults(which='unfollow')
    parser_unfollow.add_argument('nick', type=str)

    parser_info = subparsers.add_parser('info',
                                        help="get infomration about a source")
    parser_info.set_defaults(which='info')
    parser_info.add_argument('nick', type=str)

    parser_tweet = subparsers.add_parser('tweet',
                                         help="tweet a status message")
    parser_tweet.set_defaults(which='tweet')
    parser_tweet.add_argument('tweet', type=str)

    args = parser.parse_args()

    if args.which == 'timeline':
        timeline(args.timeline_reverse)

    if args.which == 'follow':
        follow(args.follow_nick, args.follow_url)

    if args.which == 'following':
        following()

    if args.which == 'unfollow':
        unfollow(args.nick)

    if args.which == 'view':
        view(args.nick, args.view_reverse)

    if args.which == 'info':
        info(args.nick)

    if args.which == 'tweet':
        tweet(args.tweet)
