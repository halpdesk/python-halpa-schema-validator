import pytest


# Global setup for all tests (runs once)
def pytest_configure(config):
    config.addinivalue_line('markers', 'validator')
    config.addinivalue_line('markers', 'decorator')
