from factory.alchemy import SQLAlchemyModelFactory

from clocking.models import db, Person, Address


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
