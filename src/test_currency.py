#!/usr/bin/env python
# encoding: utf-8

"""Tests for currency exchange rate fetching."""

from __future__ import print_function

import logging

import pytest

import currency
from config import currency_requires_openx


def test_currency_requires_openx_free_tier():
    """Common fiat currencies work without APP_KEY."""
    assert not currency_requires_openx('eur')
    assert not currency_requires_openx('USD')
    assert currency_requires_openx('AFN')
    assert currency_requires_openx('XAU')


def test_fetch_exchange_rates_tolerates_crypto_failure(monkeypatch):
    """Fiat rates are returned even if cryptocurrency fetch fails."""
    log = logging.getLogger('test_currency')
    currency.log = log
    currency.wf = None

    monkeypatch.setattr(currency, 'load_active_currencies', lambda: {'EUR', 'ETH'})
    monkeypatch.setattr(currency, 'load_xra_rates',
                        lambda symbols: {'EUR': 0.87})
    monkeypatch.setattr(currency, 'load_cryptocurrency_rates',
                        lambda symbols: (_ for _ in ()).throw(RuntimeError('nope')))

    rates = currency.fetch_exchange_rates()
    assert rates == {'EUR': 0.87}


if __name__ == '__main__':  # pragma: no cover
    pytest.main([__file__])
