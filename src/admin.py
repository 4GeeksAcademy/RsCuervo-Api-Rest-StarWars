import os
from flask_admin import Admin
from models import db, User, Characters, FavoriteCharacters, Planets, FavoritePlanets, Starships, FavoriteStarships
from flask_admin.contrib.sqla import ModelView


# ------------------------------------

class FavoriteCharactersModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla
    column_list = ['id', 'user', 'characters', 'characters_id', 'user_id']


class CharactersModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla
    column_list = ['id', 'name', 'comment_text', 'favorite_characters_by']

# ------------------------------


class FavoritePlanetsModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla
    column_list = ['id', 'user', 'planets', 'user_id', 'planets_id']


class PlanetsModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla
    column_list = ['id', 'name', 'comment_text', 'favorite_planets_by']

# ------------------------------


class FavoriteStarshipsModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla
    column_list = ['id', 'user', 'starships', 'user_id', 'starships_id']


class StarshipsModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla
    column_list = ['id', 'name', 'comment_text', 'favorite_starships_by']

# ---------------------------------


class UserModelView(ModelView):
    column_auto_select_related = True
    # Columnas y relationships de mi tabla
    column_list = ['id', 'email', 'password', 'favorite_characters',
                   'favorite_planets', 'favorite_starships', 'is_active']

# --------------------------------


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
   
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharactersModelView(Characters, db.session))
    admin.add_view(FavoriteCharactersModelView(FavoriteCharacters, db.session))
    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(FavoritePlanetsModelView(FavoritePlanets, db.session))
    admin.add_view(StarshipsModelView(Starships, db.session))
    admin.add_view(FavoriteStarshipsModelView(FavoriteStarships, db.session))
    
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
