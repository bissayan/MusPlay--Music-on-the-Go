from .database import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from flask_security import UserMixin, RoleMixin, AsaList

class User(db.Model,UserMixin):
  __tablename__ = 'user'    
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  user_name=db.Column(db.String, nullable=False)  
  email_id=db.Column(db.String, unique=True, nullable=False)
  password=db.Column(db.String, unique=True, nullable=False)  
  login_time=db.Column(db.DateTime,nullable=False)
  logout_time=db.Column(db.DateTime,nullable=True)
  #
  active = db.Column(db.Boolean())
  fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
  roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))
  #  
  user=db.Column(db.Integer,nullable=False)
  creator=db.Column(db.Integer,nullable=False)
  usflag=db.Column(db.Integer,nullable=True)

#  
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(MutableList.as_mutable(AsaList()), nullable=True)
#
      
class Album(db.Model):
  __tablename__ = 'album'
  sl_no=db.Column(db.Integer,primary_key=True,autoincrement=True)
  album_id=db.Column(db.Integer, nullable=False, autoincrement=True)
  album_name=db.Column(db.String, nullable=False)
  agenre=db.Column(db.String,nullable=False)
  artist=db.Column(db.String, nullable=False)
  asong_id=db.Column(db.Integer,nullable=True)
  
  

class Song(db.Model):
  __tablename__ = 'song'
  song_id=db.Column(db.Integer, primary_key=True,  autoincrement=True)
  song_name=db.Column(db.String, nullable=False)
  sgenre=db.Column(db.String,nullable=False)
  artist=db.Column(db.String, nullable=False)
  artist_name=db.Column(db.String, nullable=False)  
  lyrics=db.Column(db.String,nullable=True)  
  date_created=db.Column(db.DateTime,nullable=True)  
  sofile_id=db.Column(db.String,nullable=True)
  soflag=db.Column(db.Integer,nullable=True)
  listen_count=db.Column(db.Integer,nullable=True)
  rating=db.Column(db.Integer,nullable=True)

class Playlist(db.Model):
  __tablename__ = 'playlist'
  sl_no=db.Column(db.Integer,primary_key=True,autoincrement=True)
  playist_id=db.Column(db.Integer, nullable=False)
  playlist_name=db.Column(db.String, nullable=False)
  psong_id=db.Column(db.Integer, nullable=True)   
  pgenre=db.Column(db.String,nullable=False)
  puser_id=db.Column(db.String,  nullable=False)
  pdate_created=db.Column(db.DateTime,nullable=False)