import os
import unittest

from twtxtcli.twtxt import *

FIXTURE_PATH = os.path.dirname(os.path.realpath(__file__))


class TestTwTxt(unittest.TestCase):

    def setUp(self):
        self.twtxt = TwTxt(os.path.join(FIXTURE_PATH,
                                        'fixtures/example_config.ini'))

    def test_follow(self):
        self.twtxt.follow('myles', 'https://twtxt.mylesb.ca/')
        self.assertTrue(self.twtxt.config.has_option('following', 'myles'))

    def test_unfollow(self):
        self.twtxt.unfollow('myles')
        self.assertFalse(self.twtxt.config.has_option('following', 'myles'))

    def test_following(self):
        self.assertEquals(self.twtxt.following(), [])
