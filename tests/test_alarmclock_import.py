import importlib


def test_alarmclock_module_imports():
    module = importlib.import_module('alarmclock.main')
    assert hasattr(module, 'main')
