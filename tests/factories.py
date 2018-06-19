from factory.alchemy import SQLAlchemyModelFactory

from clocking.models import db, Person, Address, User, Role, Departament


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

    id = 1
    last_name = 'l'
    first_name = 'f'


class RoleAdminFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Role
        sqlalchemy_session = db.session

    name = 'superuser'


class DepartamentFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Departament
        sqlalchemy_session = db.session

    id = 1
    name = 'Departament'


class RoleUserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Role
        sqlalchemy_session = db.session

    name = 'user'


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    email = 'example@email.com'
    password = 'password'
    person_id = None
    active = True
    roles = []
