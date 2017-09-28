from datetime import timedelta
from sqlalchemy import extract

from flask import render_template, request
from flask.views import MethodView

from clocking.models import PersonMac, Person, MacAddress, db
from clocking.api.forms import AddForm, EditForm, SelectForm


class PersonAddView(MethodView):

    def get(self):
        form = AddForm()
        return render_template('add.html', form=form)

    def post(self):
        form = AddForm(request.form)
        if form.validate():
            form.save()
            persons = PersonMac.query.order_by(PersonMac.last_name)
            return render_template('people.html', persons=persons,
                                   success="You've successfully added a person")

        return render_template('add.html', form=form)


class PersonEditView(MethodView):

    def get(self, person_id):
        person = db.session.query(PersonMac).get(person_id)
        form = EditForm()
        return render_template('edit.html', form=form, person=person)

    def post(self, person_id):
        person = db.session.query(PersonMac).get(person_id)
        form = EditForm(request.form)
        if form.validate():
            form.save(person_id)
            persons = PersonMac.query.order_by(PersonMac.last_name)
            return render_template('people.html', persons=persons,
                                   success="You've successfully edited a person")

        return render_template('edit.html', form=form, person=person)


class PersonListView(MethodView):

    def get(self):
        persons = PersonMac.query.order_by(PersonMac.last_name)
        return render_template('people.html', persons=persons)


class PersonClockingView(MethodView):
    def get_persons_by_interval(self, start_date, end_date):
        persons = Person.query
        if start_date and end_date:
            return persons.filter(Person.startdate.between(start_date, end_date)).order_by(Person.startdate)
        else:
            return persons.all()

    def get(self):
        form = SelectForm()

        start_date, end_date = None, None
        if request.args:
            form = SelectForm(request.args)
            if form.validate():
                start_date = form.data.get('start_date')
                end_date = form.data.get('end_date')

        persons = self.get_persons_by_interval(start_date, end_date)

        return render_template('clocking.html', form=form, persons=persons)


class IndexView(MethodView):

    def get(self):
        return render_template('index.html')
