import json

from flask import url_for

from clocking.models import PersonMac
from .factories import PersonMacFactory


def test_first_page(client):
    resp = client.get(url_for('api.clocking'))
    assert resp.status_code == 200

def test_people(client):
    resp = client.get(url_for('api.people'))
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


def test_edit_person_mac(client):
    person_mac = PersonMacFactory()
    resp = client.post(url_for('api.edit', person_id=1), dict(
        last_name='test',
        first_name='test',
        mac='00:00:00:00:00:00'))
    assert resp.status_code == 200
    assert len(PersonMac.query.all()) == 1
    person_mac = PersonMac.query.get(1)
    assert person_mac.last_name == 'test'
    assert person_mac.first_name == 'test'
    assert person_mac.mac == '00 00 00 00 00 00'
