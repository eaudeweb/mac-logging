from factory.alchemy import SQLAlchemyModelFactory

from clocking import models


class PersonMacFactory(SQLAlchemyModelFactory):

    class Meta:
        model = models.PersonMac
        sqlalchemy_session = models.db.session

    mac = 'ff:ff:ff:ff:ff:ff'
    last_name = 'l'
    first_name = 'f'
