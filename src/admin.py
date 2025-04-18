import os
from flask_admin import Admin
from models import db, Users, Peoples, Planets, Species, Favorites
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')


### NOTA para el Joan del futuro:
# para inicializar el back tenes que darle los siguientes comandos en la consola:
# pipenv run migrate
# pipenv run upgrade 
# pipenv run start
###    
    # Add your models here, for example this is how we add a the User model to the admin
    
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Peoples, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Species, db.session))
    admin.add_view(ModelView(Favorites, db.session))
    
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))