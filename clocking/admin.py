from flask_admin import Admin
from clocking.api import view
from clocking.models import Role, User, Person, Address, Entry, db

admin = Admin(name='Clocking',
              base_template='my_master.html',
              template_mode='bootstrap3')

admin.add_view(view.ProtectedModelView(Role, db.session))
admin.add_view(view.ProtectedModelView(User, db.session))
admin.add_view(view.ProtectedModelView(Person, db.session))
admin.add_view(view.ProtectedModelView(Address, db.session))
admin.add_view(view.ProtectedModelView(Entry, db.session))
