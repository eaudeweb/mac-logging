from flask import url_for

from tests.factories import (PersonFactory, AddressFactory, UserFactory,
                             RoleAdminFactory, DepartamentFactory)
from clocking.models import Person, Address, Departament, Entry


def login_admin(client):
    role = RoleAdminFactory()
    user = UserFactory()
    user.roles.append(role)
    client.post(url_for('security.login'),
                dict(email=user.email, password=user.password))
    return user


def test_login(client):
    role = RoleAdminFactory()
    user = UserFactory()
    user.roles.append(role)
    resp = client.post(url_for('security.login'),
                       dict(email=user.email, password=user.password))
    assert resp.status_code == 302


def test_first_page(client):
    resp = client.get(url_for('api.clocking'),
                      dict(start_date='01/01/2017', end_date='01/01/2017'))
    assert resp.status_code == 200


def test_people(client):
    login_admin(client)
    resp = client.get(url_for('api.people'))
    assert resp.status_code == 200


def test_add_person(client):
    login_admin(client)
    dept = DepartamentFactory()
    resp = client.post(url_for('api.add_person'),
                       dict(last_name='l', first_name='f', dept=dept.id))
    assert resp.status_code == 200
    assert len(Person.query.all()) == 1
    person = Person.query.first()
    assert person.last_name == 'l'
    assert person.first_name == 'f'
    Person.query.delete()
    assert Person.query.count() == 0


def test_add_address(client):
    login_admin(client)
    person = PersonFactory()
    resp = client.post(url_for('api.add_mac'),
                       dict(mac='00:00:00:00:00:00', device='mobile',
                            person=1, priority='2'))
    assert resp.status_code == 200
    assert len(Address.query.all()) == 1
    address = Address.query.first()
    assert address.mac == '00 00 00 00 00 00'
    assert address.device == 'mobile'


def test_edit_person_mac(client):
    login_admin(client)
    dept = DepartamentFactory()
    person = PersonFactory()
    resp = client.post(url_for('api.edit', person_id=person.id),
                       dict(last_name='l_test', first_name='f_test', dept=dept.id))
    assert resp.status_code == 200
    assert len(Person.query.all()) == 1
    person = Person.query.first()
    assert person.last_name == 'l_test'
    assert person.first_name == 'f_test'


def test_get_delete_person_mac(client):
    login_admin(client)
    resp = client.get(
        url_for('api.delete_mac', mac_address='00 00 00 00 00 00'))
    assert resp.status_code == 200


def test_delete_person_mac(client):
    login_admin(client)
    person = PersonFactory()
    address = AddressFactory()
    resp = client.post(url_for('api.delete_mac', mac_address='00 00 00 00 00 00'))
    assert resp.status_code == 200
    assert address.deleted is True


def test_about(client):
    resp = client.get(url_for('api.about'))
    assert resp.status_code == 200


def test_manual_clocking(client):
    user = login_admin(client)
    person = PersonFactory()
    address = AddressFactory()
    address.person_id = person.id
    user.person_id = person.id
    resp = client.get(url_for('api.manual_clocking'))
    assert resp.status_code == 200


def test_post_manual_clocking(client):
    user = login_admin(client)
    address = AddressFactory()
    resp = client.post(url_for('api.manual_clocking'),
                       dict(mac=address, time_in='10:15', time_out='19:00'))
    assert resp.status_code == 302
    assert len(Entry.query.all()) == 1
