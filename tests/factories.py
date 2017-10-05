from factory.alchemy import SQLAlchemyModelFactory

from clocking.models import db, Person


class PersonFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Person
        sqlalchemy_session = db.session

    last_name = 'l'
    first_name = 'f'
