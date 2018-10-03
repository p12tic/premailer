from __future__ import absolute_import, unicode_literals
import unittest

from premailer.cache import function_cache
from nose.tools import raises


class TestCache(unittest.TestCase):

    @raises(TypeError)
    def test_expected_max_entries_raise(self):
        def test_func():
            pass

        cache_decorator = function_cache()
        wrapper = cache_decorator(test_func)
        wrapper(max_cache_entries='testing')

    def test_auto_turn_off(self):
        test = {'call_count': 0}

        def test_func(*args, **kwargs):
            test['call_count'] += 1

        cache_decorator = function_cache()
        wrapper = cache_decorator(test_func)
        wrapper(1, 1, t=1, max_cache_entries=2)
        wrapper(1, 2, t=1, max_cache_entries=2)
        # turn off
        wrapper(1, 3, t=1, max_cache_entries=2)
        # call 10 more times
        for _ in range(10):
            wrapper(1, 3, t=1, max_cache_entries=2)

        self.assertEqual(test['call_count'], 13)

    def test_does_not_clear_cache_on_off(self):
        test = {'call_count': 0}

        def test_func(*args, **kwargs):
            test['call_count'] += 1

        cache_decorator = function_cache()
        wrapper = cache_decorator(test_func)
        wrapper(1, 1, t=1, max_cache_entries=2)
        wrapper(1, 2, t=1, max_cache_entries=2)
        # turn off
        wrapper(1, 3, t=1, max_cache_entries=2)
        # call 10 more times
        for _ in range(10):
            wrapper(1, 2, t=1, max_cache_entries=2)

        self.assertEqual(test['call_count'], 3)

    def test_cache_hit(self):
        test = {'call_count': 0}

        def test_func(*args, **kwargs):
            test['call_count'] += 1

        cache_decorator = function_cache()
        wrapper = cache_decorator(test_func)
        wrapper(1, 1, t=1, max_cache_entries=20)
        wrapper(1, 2, t=1, max_cache_entries=20)
        wrapper(1, 3, t=1, max_cache_entries=20)
        # call 10 more times
        for _ in range(10):
            wrapper(1, 3, t=1, max_cache_entries=20)
            self.assertEqual(test['call_count'], 3)
