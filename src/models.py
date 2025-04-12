from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites_characters: Mapped[list["FavoriteCharacters"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    favorites_planets: Mapped[list["FavoritePlanets"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    favorites_starships: Mapped[list["FavoriteStarships"]] = relationship(back_populates="user", cascade="all, delete-orphan")

#-------------------------------

class Characters(db.Model):
    __tablename__= "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)
    favorite_characters_by: Mapped[list["FavoriteCharacters"]] = relationship(back_populates="characters", cascade='all, delete-orphan')

class FavoriteCharacters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorites_characters")
    characters_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    characters: Mapped["Characters"] = relationship(back_populates="favorite_characters_by")

#---------------------------------

class Planets(db.Model):
    __tablename__="planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)
    favorite_planets_by: Mapped[list["FavoritePlanets"]] = relationship(back_populates="planets", cascade='all, delete-orphan')


class FavoritePlanets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorites_planets")
    planets_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    planets: Mapped["Planets"] = relationship(back_populates="favorite_planets_by")


#-------------------------

class Starships(db.Model):
    __tablename__= "starships"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)
    favorite_starships_by: Mapped[list["FavoriteStarships"]] = relationship(back_populates="starships", cascade='all, delete-orphan')

class FavoriteStarships(db.Model):
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorites_starships")
    starships_id: Mapped[int] = mapped_column(ForeignKey("starships.id"))
    starships: Mapped["Starships"] = relationship(back_populates="favorite_starships_by")



   # def serialize(self):
    #    return {
     #       "id": self.id,
      #      "email": self.email,
            # do not serialize the password, its a security breach
       # }
