from flask import url_for

from tests.factories import PersonFactory, AddressFactory
from clocking.models import Person, Address


def test_first_page(client):
    resp = client.get(url_for('api.clocking'),
                      dict(start_date='01/01/2017', end_date='01/01/2017'))
    assert resp.status_code == 200


def test_people(client):
    resp = client.get(url_for('api.people'))
    assert resp.status_code == 200


def test_add_person(client):
    resp = client.post(url_for('api.add'),
                       dict(last_name='l', first_name='f'))
    assert resp.status_code == 200
    assert len(Person.query.all()) == 1
    person = Person.query.first()
    assert person.last_name == 'l'
    assert person.first_name == 'f'
    Person.query.delete()
    assert Person.query.count() == 0


def test_add_address(client):
    person = PersonFactory()
    resp = client.post(url_for('api.add_mac'),
                       dict(mac='00:00:00:00:00:00', device='mobile',
                            person=1))
    assert resp.status_code == 200
    assert len(Address.query.all()) == 1
    address = Address.query.first()
    assert address.mac == '00 00 00 00 00 00'
    assert address.device == 'mobile'


def test_edit_person_mac(client):
    person = PersonFactory()
    resp = client.post(url_for('api.edit', person_id=1),
                       dict(last_name='l_test', first_name='f_test'))
    assert resp.status_code == 200
    assert len(Person.query.all()) == 1
    person = Person.query.first()
    assert person.last_name == 'l_test'
    assert person.first_name == 'f_test'


def test_get_delete_person_mac(client):
    resp = client.get(
        url_for('api.delete_mac', mac_address='00 00 00 00 00 00'))
    assert resp.status_code == 200


def test_delete_person_mac(client):
    person = PersonFactory()
    address = AddressFactory()
    resp = client.post(url_for('api.delete_mac', mac_address='00 00 00 00 00 00'))
    assert resp.status_code == 200
    assert address.deleted is True


def test_about(client):
    resp = client.get(url_for('api.about'))
    assert resp.status_code == 200


def test_get_login_page(client):
    resp = client.get(url_for('api.login'))
    assert resp.status_code == 200
