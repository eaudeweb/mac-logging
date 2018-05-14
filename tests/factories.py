from factory.alchemy import SQLAlchemyModelFactory

from clocking.models import db, Person, Address, User, Role


class AddressFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Address
        sqlalchemy_session = db.session

    mac = '00 00 00 00 00 00'
    device = 'mobile'
    person_id = 1
    deleted = False


class PersonFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Person
        sqlalchemy_session = db.session

    last_name = 'l'
    first_name = 'f'


class RoleFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Role
        sqlalchemy_session = db.session

    name = 'user'


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    email = 'email@example.com'
    password = 'password'
    active = True
    roles = []
