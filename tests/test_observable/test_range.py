import unittest

from rx import Observable
from rx.testing import TestScheduler, ReactiveTest

send = ReactiveTest.send
close = ReactiveTest.close
throw = ReactiveTest.throw
subscribe = ReactiveTest.subscribe
subscribed = ReactiveTest.subscribed
disposed = ReactiveTest.disposed
created = ReactiveTest.created


class TestRange(unittest.TestCase):
    def test_range_zero(self):
        scheduler = TestScheduler()

        def create():
            return Observable.range(0, 0)

        results = scheduler.start(create)
        assert results.messages == [close(200)]

    def test_range_one(self):
        scheduler = TestScheduler()

        def create():
            return Observable.range(0, 1)
        results = scheduler.start(create)

        assert results.messages == [send(200, 0), close(200)]

    def test_range_five(self):
        scheduler = TestScheduler()

        def create():
            return Observable.range(10, 15)

        results = scheduler.start(create)

        assert results.messages == [send(200, 10),
                                    send(200, 11),
                                    send(200, 12),
                                    send(200, 13),
                                    send(200, 14),
                                    close(200)]

    def test_range_dispose(self):
        scheduler = TestScheduler()

        def create():
            return Observable.range(-10, 5)

        results = scheduler.start(create, disposed=200)
        assert results.messages == []

    def test_range_double_subscribe(self):
        scheduler = TestScheduler()
        obs = Observable.range(1, 4)

        results = scheduler.start(lambda: obs.concat(obs))
        assert results.messages == [send(200, 1), send(200, 2),
                                    send(200, 3), send(200, 1),
                                    send(200, 2), send(200, 3),
                                    close(200)]

    def test_range_only_start(self):
        scheduler = TestScheduler()

        def create():
            return Observable.range(5)

        results = scheduler.start(create)
        assert results.messages == [send(200, 0),
                                    send(200, 1),
                                    send(200, 2),
                                    send(200, 3),
                                    send(200, 4),
                                    close(200)]

    def test_range_step_also(self):
        scheduler = TestScheduler()

        def create():
            return Observable.range(0, 10, 2)

        results = scheduler.start(create)
        assert results.messages == [send(200, 0),
                                    send(200, 2),
                                    send(200, 4),
                                    send(200, 6),
                                    send(200, 8),
                                    close(200)]
