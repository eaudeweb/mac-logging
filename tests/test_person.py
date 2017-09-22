import json

from flask import url_for

from clocking.models import PersonMac
from .factories import PersonMacFactory


def test(client):
    resp = client.get(url_for('api.index'))
    assert resp.status_code == 200


def test_add_person_mac(client):
    resp = client.post(url_for('api.add'), dict(
        last_name='l', first_name='f',
        mac1='ff:ff:ff:ff:ff:ff', mac2='', mac3=''))
    assert resp.status_code == 200
    assert len(PersonMac.query.all()) == 1
    assert PersonMac.query.first().mac == 'FF FF FF FF FF FF'
    PersonMac.query.delete()
    assert PersonMac.query.count() == 0
