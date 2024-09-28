from flask import Flask
from flask import request,render_template,redirect,flash,jsonify, request, make_response, url_for,Response
from sqlalchemy import desc
import matplotlib.pyplot as plt
import os
from flask_bcrypt import Bcrypt

from datetime import datetime ,timedelta

from flask_security import Security, SQLAlchemyUserDatastore



import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from flask_security import *
from werkzeug.security import *

from flask_cors import CORS
from flask_bcrypt import Bcrypt

import redis
from flask_caching import Cache


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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



app=Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client})



app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path,  'say2vue', 'public', 'static', 'song_store')
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///22f3001500-MAD-1.sqlite3'
app.config['SECRET KEY']='thisasecretkey'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['JSON_AS_ASCII'] = False



db.init_app(app)
app.app_context().push()
CORS(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


from flask import current_app as app

bcrypt = Bcrypt(app)
jwt = JWTManager(app)


#from flask import Flask, request, jsonify
#import os


#app = Flask(__name__)

# Utility function to split text into chunks
def split_text(text, max_length=500):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(word)
        current_length += len(word) + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

@app.route('/generate', methods=['POST','GET'])
def generate_song():
    data = request.json
    text_input = data.get('text')

    if not text_input:
        return jsonify({'error': 'Text input is required'}), 400

    try:
        # Split text into chunks
        text_chunks = split_text(text_input)

        # Generate and concatenate audio for each chunk
        audio_arrays = []
        for chunk in text_chunks:
            audio_array = generate_audio(chunk)
            audio_arrays.append(audio_array)

        # Concatenate audio arrays
        combined_audio = np.concatenate(audio_arrays)

        # Save the combined audio to a file
        temp_audio_file = NamedTemporaryFile(delete=False, suffix=".wav")
        temp_audio_file_path = temp_audio_file.name
        sf.write(temp_audio_file_path, combined_audio, 22050)  # Assuming 22.05 kHz sample rate

        return jsonify({'audio_url': f'/download/{os.path.basename(temp_audio_file_path)}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_audio(filename):
    return app.send_static_file(filename)

'''if __name__ == '__main__':
    app.run(debug=True)'''



# controller for login user
@app.route("/api/login", methods=["GET","POST"])
def login_dev():
    if request.method == "GET":
        existing_emails = User.query.with_entities(User.email_id).all()        
        email_addresses = [email[0] for email in existing_emails]            
        return make_response(jsonify({'message': 'Login Loaded'},email_addresses), 200)
    if request.method == "POST":
            logdata=request.get_json()
            email_id = logdata["email_id"]
            password = logdata["password"]
            user = user_datastore.find_user(email_id=email_id)    
        
            if bcrypt.check_password_hash(user.password, password):
                user.login_time=datetime.now()
                db.session.commit()

                access_token = create_access_token(
                identity=user.id, expires_delta=timedelta(days=1))
                user_info = {
                    'user_id': user.id,
                    'user_name': user.user_name,
                    'usflag': user.usflag,                    
                    'role': [role.name for role in user.roles],
                }

                return jsonify({'access_token': access_token, 'user': user_info}), 200
            else:
                flash("Wrong Password")
                return make_response(jsonify({'message': 'You entered wrong password'}), 400)



@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        existing_emails = User.query.with_entities(User.email_id).all()        
        email_addresses = [email[0] for email in existing_emails]
        print(existing_emails)             
        return make_response(jsonify(email_addresses), 200)
        
    if request.method == "POST":
                data=request.get_json()
                email = data["email_id"]        
                password = data["password"]         
                user_name=data['user_name']              
                hashed_password = bcrypt.generate_password_hash(password)               
                login_time=datetime.now()               
                user=1
                creator=0
                new_user = user_datastore.create_user(user_name=user_name,email_id=email, password=hashed_password,login_time=login_time,user=user,creator=creator)
                db.session.add(new_user)
                user_datastore.add_role_to_user(new_user, 'user')
                db.session.commit()
                return make_response(jsonify({'message': 'User has been registered successfully'}), 200)
    
        
# controller to change password for user
@app.route("/forget_password",methods=["GET","POST"])
def forget_password():
    if request.method == "GET":
        existing_emails = User.query.with_entities(User.email_id).all()        
        email_addresses = [email[0] for email in existing_emails]
        print(existing_emails)             
        return make_response(jsonify(email_addresses), 200)
    if request.method == "POST":
                data=request.get_json()
                email = data["email_id"]
                existing_user = User.query.filter_by(email_id=email).first()
        
                new_password = data["password"]            
                hashed_password = bcrypt.generate_password_hash(new_password)
                existing_user.password = hashed_password
                db.session.commit()
                flash("Password changed,Login with new.")
                #return redirect('/login')
                return make_response(jsonify({'message': 'Your password has been changed successfully'}), 200)
            
        

#--------------------------------------------------------Search------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/search/<string:query>", methods=["GET","POST"])
@jwt_required()
def search(query):           
    if request.method == "GET":
        id_type=1 #request.form['ID']               
        #search_request = request.form['search_request']  
        search_request=query      
        query = "%" + search_request + "%"
        
        print(query)
        # pull search result for Songs
        
        song_names_matched = []
        songs_results = Song.query.filter(Song.song_name.like(query)).all()
        if songs_results:
            for result in songs_results:
                if result.soflag==0:
                    song_names_matched.append(result)

        # pull search result for Genre
        
        genre_matched = []
        genre_results = Song.query.filter(Song.sgenre.like(query)).all()
        if genre_results:
            for result in genre_results:
                if result.soflag==0:
                  genre_matched.append(result)
        album_genre_matched = []
        genre_results = Album.query.filter(Album.agenre.like(query)).all()
        if genre_results:
            for result in genre_results :
                  if result.asong_id==None:
                      album_genre_matched.append(result)

        # pull search result for Rating        
        
        songsrated_results = Song.query.filter(Song.rating.like(query)).all()
        if songsrated_results:
            for result in songsrated_results:
                if result.soflag==0:
                  song_names_matched.append(result)

        # pull search result for Albums
        
        album_names_matched = []
        album_results = Album.query.filter(Album.album_name.like(query)).all()
        if album_results:
            for result in album_results:
                if result.asong_id==None:
                   album_names_matched.append(result)

        # pull search result for Artists
        
        artist_names_matched = []        
        artist_fresults = User.query.filter(User.user_name.like(query)).all()        
        for fresult in artist_fresults:
            if fresult.usflag==None:
              artist_names_matched.append(fresult) 

        artist_names_matched=set(artist_names_matched)
        song_names_matched=set(song_names_matched)
        album_genre_matched=set(album_genre_matched)
        genre_matched=set(genre_matched)
        album_names_matched=set(album_names_matched)

        album_genre_matchedA=[]
        song_names_matchedA=[]
        genre_matchedA=[]
        artist_names_matchedA=[]
        album_names_matchedA=[]

        for i in genre_matched:                
                    song_info = {
                        'song_id': i.song_id,
                        'song_name': i.song_name,
                        'artist_name': i.artist_name,
                        'artist': i.artist,
                        'rating': i.rating,
                        'sofile_id': url_for('static', filename='song_store/' + i.sofile_id),                        
                    }
                    genre_matchedA.append(song_info)

        for i in song_names_matched:                
                    song_info = {
                        'song_id': i.song_id,
                        'song_name': i.song_name,
                        'artist_name': i.artist_name,
                        'artist': i.artist,
                        'rating': i.rating,
                        'sofile_id': url_for('static', filename='song_store/' + i.sofile_id),                        
                    }
                    song_names_matchedA.append(song_info)

        for i in album_genre_matched:                
                    album_info = {
                        'album_id': i.album_id,
                        'artist': i.artist,
                        'album_name': i.album_name,                                                
                    }
                    album_genre_matchedA.append(album_info)

        for i in artist_names_matched:                
                    artist_info = {
                        'artist': i.id,
                        'user_name': i.user_name,                                                
                    }
                    artist_names_matchedA.append(artist_info)

        for i in album_names_matched:                
                    album_info = {
                        'album_id': i.album_id,
                        'album_name': i.album_name,
                        'artist': i.artist,                                                
                    }
                    album_names_matchedA.append(album_info)        
        return make_response(jsonify(album_genre_matchedA,genre_matchedA,artist_names_matchedA,song_names_matchedA,album_names_matchedA),200)

@app.route('/user_creator/<int:value>',methods=['GET','POST'])
@cache.cached(timeout=2)
@jwt_required()
def user_creator(value):
  if request.method == "GET":
        user_id = get_jwt_identity()
        print(user_id)
        uc=User.query.filter_by(id=user_id).first()
        songs=Song.query.order_by(desc(Song.date_created)).all()    
        albums=Album.query.all()   
        ply1=Playlist.query.all()
        l=[]
        ll=[]
        m=[]
        song_filtered=[]
        for s in songs:
            if s.soflag==0:
                song_filtered.append(s)
        for d in ply1:
            if d.psong_id==None: 
                if int(d.puser_id)==int(user_id):
                    l.append(d)
        for d in albums:
            if d.asong_id==None:
                ll.append(d)
        songs_export=[]        
        for song in song_filtered:                    
                        song_info = {
                            'song_id': song.song_id,
                            'song_name': song.song_name,
                            'artist_name': song.artist_name,
                            'artist': song.artist,
                            'rating': song.rating,
                            'sofile_id': url_for('static', filename='song_store/' + song.sofile_id),                        
                        }
                        songs_export.append(song_info)        
        albums_export=[]        
        for album in ll:                   
                        album_info = {
                            'album_id': album.album_id,
                            'album_name': album.album_name,                                                
                        }
                        albums_export.append(album_info)  
        playlists_export=[]        
        for playlist in l:                   
                        playlist_info = {
                            'playist_id': playlist.playist_id,
                            'playlist_name': playlist.playlist_name,                                                
                        }
                        playlists_export.append(playlist_info)  
        return make_response(jsonify(songs_export,albums_export,playlists_export), 200)
  else:        
        rate_it=Song.query.filter_by(song_id=value).first()
        if rate_it.listen_count==None:
             rate_it.listen_count=0 
        if rate_it.rating==None:
             rate_it.rating=0 
        l=rate_it.listen_count
        data=request.get_json()
        rated= data['rate']
        rate=int(rated)         
        rate_it.rating = ( (rate_it.rating*l) + rate )/(l+1)
        rate_it.listen_count=l+1
        db.session.commit()
        return make_response(jsonify(" Rated It "), 200) 

@app.route('/creator',methods=['GET','POST'])
@jwt_required()
def creator():
  if request.method == "GET":
        user_id = get_jwt_identity()
        user=User.query.filter_by(id=user_id).first()
        print(user)
        son1=Song.query.order_by(desc(Song.date_created)).all()      
        l=[]
        sgnm=[]
        lisco=[]
        for i in Song.query.filter_by(artist=user_id).all():
            sgnm.append(i.song_name)
            lisco.append(i.listen_count)
        for d in Album.query.all():
                if d.asong_id==None:
                    l.append(d)
        rate=Song.query.filter_by(artist=user_id).all()
        rating=0
        for r in rate:
            if r.rating==None:
                rating=rating + 0 
            else:
                rating=rating + int(r.rating)   
        song_filtered=[]
        m=[]     
        for s in son1:
            if int(s.artist)==int(user_id):
                    song_filtered.append(s)
        for i in l:
            if int(i.artist)==int(user_id):              
                        m.append(i)
        if len(song_filtered)==0:
            g=1
        else:
            g=len(song_filtered)
        songs_export=[]        
        for song in song_filtered:                    
                        song_info = {
                            'song_id': song.song_id,
                            'song_name': song.song_name,
                            'artist_name': song.artist_name,
                            'artist': song.artist,
                            'rating': song.rating,
                            'sofile_id': url_for('static', filename='song_store/' + song.sofile_id),                        
                        }
                        songs_export.append(song_info)        
        albums_export=[]        
        for album in m:                   
                        album_info = {
                            'album_id': album.album_id,
                            'album_name': album.album_name,                                                
                        }
                        albums_export.append(album_info)
        if user.usflag!=1:            
            usered={
                 'user_name': user.user_name,
                 'usflag': user.usflag
            }
            monitor = {            
            'Songs': len(song_filtered),
            'Albums': len(m),
            'Rating': int((rating)/g)
        }
            return make_response(jsonify(songs_export,albums_export,monitor,usered,sgnm,lisco), 200)
        



#   To become creator
@app.route('/user/creator',methods=['GET','POST'])
@jwt_required()
def become_creator():    
  user_id = get_jwt_identity()
  user=User.query.filter_by(id=user_id).first()
  roller=RolesUsers.query.filter_by(user_id=user_id).first()
  if request.method=='GET':      
      user.creator=1
      roller.role_id=(Role.query.filter_by(name='creator').first()).id
      db.session.commit()
  return make_response(jsonify({'message': 'Updated as Creator'}), 200)

#----------------------------------------------------Song---------------------------------------------------------------------------------
import json
@app.route('/song/create', methods=['GET','POST'])
@jwt_required()
def Song_Creation():
    user_id = get_jwt_identity()
    uc=User.query.filter_by(id=user_id).first()
    if request.method=='POST':        
        song = json.loads(request.form['data'])        
        song_music = request.files['file']
        
        if song_music:
          sofile_id = song_music.filename
          print(sofile_id)
          song_music.save(os.path.join(app.config['UPLOAD_FOLDER'], sofile_id))        

        song_id=song.get('song_id','').strip()
        print(song_id)
        song_name=song.get('songName','').strip()
        print(song.get('song_name',''))
        sgenre=song.get('sgenre','').strip()
        artist=user_id
        lyrics=song.get('lyrics','').strip() 

        artist_name= uc.user_name
        date_created=datetime.now()
        sofile_id=sofile_id
        i_song=Song( song_name=song_name,artist_name=artist_name, sgenre=sgenre, artist=artist, lyrics=lyrics,  date_created=date_created,sofile_id=sofile_id,soflag=0)            
        db.session.add(i_song)
        db.session.commit()
        son1=Song.query.all()
        k=[]
        for s in son1:
           if int(s.artist)==int(user_id):
              k.append(s)
        return make_response(jsonify({'message': 'Song Created'}), 200)       
    else:
        return make_response(jsonify({'message': 'More datapoints required'}), 200)
    
#----------------------------------------------------Album--------------------------------------------------------------------------------------------------------------

@app.route('/album/create', methods=['GET','POST'])
@jwt_required()
def Album_Creation():
    user_id = get_jwt_identity()
    uc=User.query.filter_by(id=user_id).first()
    alb1=Album.query.all()
    albm_id_counter=[0]
    for d in alb1:
         if d.asong_id==None:
            albm_id_counter.append(d.album_id)
    if request.method=='POST':
        album=request.get_json()        
        album_id= max(albm_id_counter) + 1
        album_name=album['album_name']
        agenre=album['agenre']
        artist=user_id        
        i_album=Album(album_id=album_id, album_name=album_name, agenre=agenre, artist=artist)        
        db.session.add(i_album)
        db.session.commit()        
        return make_response(jsonify({'message': 'Album Created'}), 200)              
    else:       
       return render_template('Album_Creation.html',s=uc) 


@app.route('/playlist/create', methods=['GET','POST'])
@jwt_required()
def Playlist_Creation():
    user_id = get_jwt_identity()
    uc=User.query.filter_by(id=user_id).first()
    ply1=Playlist.query.all()
    ply_id_counter=[0]
    for d in ply1:
         if d.psong_id==None:
            ply_id_counter.append(d.playist_id)
    if request.method=='POST':
        playlist=request.get_json()        
        playist_id= max(ply_id_counter) + 1
        playlist_name=playlist['playlist_name']
        pgenre=playlist['pgenre']
        puser_id=user_id        
        i_ply=Playlist(playist_id=playist_id, playlist_name=playlist_name, pgenre=pgenre, puser_id=puser_id,pdate_created=datetime.now())        
        db.session.add(i_ply)
        db.session.commit() 
        return make_response(jsonify({'message': 'Playlist Created'}), 200)       
    else:       
       return render_template('Playlist_Creation.html',s=uc) 


@app.route('/song/<string:song_id>/<int:value>/add', methods=["GET","POST"])
@jwt_required()
def add_song(song_id,value):
    user_id = get_jwt_identity()
    uc=User.query.filter_by(id=user_id).first()
    if len(song_id) > 2:
        asong_id=int(song_id.split("::")[1])
        ku=Song.query.filter_by(song_id=asong_id).first()
    else:
        ku=Song.query.filter_by(song_id=song_id).first()
    song=ku 
    print(song)
    if value == 2:
       alb1=Album.query.all()          
       l=[]
       for d in alb1:
         if d.asong_id==None:
            if int(d.artist)==user_id:
               l.append(d)
             
       if request.method == "GET":        
            song_info = {
                            'song_id': song.song_id,
                            'song_name': song.song_name,
                            'artist_name': song.artist_name,
                            'rating': song.rating,
                            'lyrics': song.lyrics,
                            'sofile_id': url_for('static', filename='song_store/' + song.sofile_id),
                            'value':2                       
                        }
            albums=[]
            for song in l:                
                    show_info = {
                        'album_id': song.album_id,
                        'album_name': song.album_name,                                                
                    }
                    albums.append(show_info)           
            return make_response(jsonify(song_info,albums), 200)          
       else:          
          album_id= int(song_id.split("::")[0])              
          count=(Album.query.filter_by(album_id=album_id).first()).sl_no                  
          ak=Album.query.filter_by(sl_no=count).first()                
          i_add=Album(album_id=album_id, album_name=ak.album_name, agenre=ak.agenre, artist=user_id,asong_id=asong_id)          
          db.session.add(i_add)
          db.session.commit()
          return make_response(jsonify({'message': 'Song added to Album'}), 200)    
    else:
       play1=Playlist.query.all()    
       ll=[]
       # Look into It       
       for d in play1:
         if d.psong_id==None:
            if int(d.puser_id)==user_id:
               ll.append(d)
               
       if request.method == "GET":
            song_info = {
                            'song_id': song.song_id,
                            'song_name': song.song_name,
                            'artist_name': song.artist_name,
                            'rating': song.rating,
                            'lyrics': song.lyrics,
                            'sofile_id': url_for('static', filename='song_store/' + song.sofile_id),
                            'value':1                       
                        }
            playlists=[]
            for song in ll:                
                    show_info = {
                        'playlist_id': song.playist_id,
                        'playlist_name': song.playlist_name,                                                
                    }
                    playlists.append(show_info)           
            return make_response(jsonify(song_info,playlists), 200)
       else:
          playist_id=int(song_id.split("::")[0])     
          count=(Playlist.query.filter_by(playist_id=playist_id).first()).sl_no        
          ap=Playlist.query.filter_by(sl_no=count).first()      
          i_add=Playlist(playist_id=playist_id, playlist_name=ap.playlist_name, pgenre=ap.pgenre, puser_id=user_id,psong_id=asong_id,pdate_created=datetime.now())
          db.session.add(i_add)
          db.session.commit()
          return make_response(jsonify({'message': 'Song added to Playlist'}), 200)
       
#---------------------------------------------------Delete-----------------------------------------------------------------------------------
@app.route('/user/<string:id>/<string:code>/delete', methods=["GET","POST","DELETE"])
@jwt_required()
def delete(id,code):   
   if request.method == "GET":
        print(id,code[:3])
        if code[:1] =="u":
            user_id=int(id)
            db.session.delete(User.query.filter_by(id=user_id).one())
            sgd=Song.query.filter_by(artist=user_id).all()
            for i in sgd:
                db.session.delete(i)
            ply=Playlist.query.filter_by(puser_id=user_id).all()
            for j in ply:
                db.session.delete(j)
            db.session.commit()       
            albd=Album.query.filter_by(artist=user_id).all()
            for j in albd:
                db.session.delete(j)
            db.session.commit()
            if code[-2:]=="ad":
                return make_response(jsonify({'message': 'Admin deleted User'}), 200)
            else:
                return make_response(jsonify({'message': 'User deleted Account'}), 200)
           
        elif code[:2] == "sl":
            l=(Song.query.filter_by(song_id=int(id)).first())
            l.lyrics=""
            db.session.commit()
            if code[-2:]=="ad":
                return make_response(jsonify({'message': 'Song lyrics deleted by Admin'}), 200)
            else:
                return make_response(jsonify({'message': 'Song lyrics deleted by Creator'}), 200)
        
        elif code[:2] == "sf":
            k=Song.query.filter_by(song_id=int(id)).first()       
            db.session.delete(k)
            db.session.commit()
            if code[-2:]=="ad":
                return make_response(jsonify({'message': 'Song deleted by Admin'}), 200)
            else:
                return make_response(jsonify({'message': 'Song deleted by Creator'}), 200)
       
        elif code[:3] == "alb":
            albd=Album.query.filter_by(album_id=id).all()
            for j in albd:           
                db.session.delete(j)
            db.session.commit()
            if code[-2:]=="ad":                
                return make_response(jsonify({'message': 'Album deleted by Admin'}), 200)
            else:
                return make_response(jsonify({'message': 'Album deleted by Creator'}), 200)
        elif code[:3] == "als":
            #print(code)
            albs=Album.query.filter_by(album_name=id,asong_id=int(code[3:])).first()       
            db.session.delete(albs)
            db.session.commit()
            if code[-2:]=="ad":                
                return make_response(jsonify({'message': 'Song in Album deleted by Admin'}), 200)
            else:                
                return make_response(jsonify({'message': 'Song in Album deleted by Creator'}), 200)
        elif code[:3] == "pls":            
            plys=Playlist.query.filter_by(playlist_name=id,psong_id=int(code[3:])).first()
            db.session.delete(plys)
            db.session.commit()            
            return make_response(jsonify({'message': 'Song in Playlist deleted by User'}), 200)
        else:
            play=Playlist.query.filter_by(playlist_name=id).all()
            for j in play:          
                db.session.delete(j)
            db.session.commit()
            #return redirect('/')
            return make_response(jsonify({'message': 'Playlist deleted by User'}), 200)
       

#---------------------------------------------------Edit-----------------------------------------------------------------------
@app.route('/user/<int:id>/<string:code>/edit',methods=["GET","POST"])
@jwt_required()
def edit(id,code):
   print(id,code) 
   if request.method=='GET':
       if code=="s":
           songs=[]
           sgd=Song.query.filter_by(song_id=id).first()
           song_info = {
                        'song_id': sgd.song_id,
                        'song_name': sgd.song_name,
                        'artist_name': sgd.artist_name,
                        'sgenre': sgd.sgenre,
                        'lyrics': sgd.lyrics,
                                                
                    }
           songs.append(song_info)
           print(songs)
           return make_response(jsonify(songs))
              
   if request.method=='POST':       
       if code=='s':
        sgd=Song.query.filter_by(song_id=id).first()
        print(sgd)
        song = json.loads(request.form['data'])
        print(song)
        # issue from here about current_user and frontend integration
        song_music = request.files['file']
        
        if song_music:
          sofile_id = song_music.filename
          print(sofile_id)
          song_music.save(os.path.join(app.config['UPLOAD_FOLDER'], sofile_id))
        
        sgd.song_name=sgd.song_name
        print(song.get('song_name',''))
        sgd.sgenre=song.get('sgenre','').strip()
        sgd.artist_name=song.get('artist','').strip() 
        sgd.artist=get_jwt_identity()
        sgd.lyrics=song.get('lyrics','').strip()
        sgd.sofile_id=sofile_id     
                  
        db.session.commit()
        #return redirect('/user_creator/2')
        return make_response(jsonify({'message': 'Song has been edited'}), 200)

@app.route('/user/<int:id>/<string:code>/edit_album',methods=["GET","POST"])
@jwt_required()
def edit_album(id,code):
    if request.method=='POST':
        editdata=request.get_json()
        agd=Album.query.filter_by(album_id=id).all()           
        nmchng=editdata['album_name']
        for i in agd:
            i.album_name=nmchng
        db.session.commit()
           #return redirect('/user_creator/2')
        return make_response(jsonify({'message': 'Album has been edited'}), 200)
    if request.method == 'GET':    
        albums = []
        l = Album.query.filter_by(album_id=id).all()
        print(l)
        for i in l:
            if i.asong_id == None:
                show_info = {
                        'album_id': i.album_id,
                        'album_name': i.album_name,                                                
                    }
        albums.append(show_info)    
        return make_response(jsonify(albums ), 200)


#--------------------------------------------------------View----------------------------------------------------------------------------------------------          
@app.route('/album/<int:id>/<int:value>/view', methods=["GET","POST"])
@jwt_required()
def view(id,value):
    user=User.query.filter_by(id=get_jwt_identity()).first() 
    if request.method=='GET':
        if value==1:
            albsong=[]
            songs_export=[]
            agd=Album.query.filter_by(album_id=id).all()
            for i in agd:
                if i.asong_id!=None:
                    albsong.append((Song.query.filter_by(song_id=i.asong_id,soflag=0).first()))
                if i.asong_id==None:
                    album_name=i.album_name                 
            
            albsong_filtered = [item for item in albsong if item is not None]
            albsong=set(albsong_filtered)
            
            for song in albsong:                                                         
                        song_info = {
                            'song_id': song.song_id,
                            'song_name': song.song_name,
                            'artist_name': song.artist_name,
                            'artist': song.artist,
                            'rating': song.rating,
                            'sofile_id': url_for('static', filename='song_store/' + song.sofile_id),                                                    
                        }
                        songs_export.append(song_info)                      
            alb_name={ 'album_name': album_name}
            return make_response(jsonify(songs_export,alb_name))
        else:            
            albsong=[]
            songs_export=[]
            agd=Playlist.query.filter_by(playist_id=id).all()
            for i in agd:
                if i.psong_id!=None:
                   albsong.append((Song.query.filter_by(song_id=i.psong_id,soflag=0).first()))
                if i.psong_id==None:
                    album_name=i.playlist_name
            albsong_filtered = [item for item in albsong if item is not None]
            albsong=set(albsong_filtered)
            for song in albsong:                                           
                        song_info = {
                            'song_id': song.song_id,
                            'song_name': song.song_name,
                            'artist_name': song.artist_name,
                            'artist': song.artist,
                            'rating': song.rating,
                            'sofile_id': url_for('static', filename='song_store/' + song.sofile_id),                        
                        }
                        songs_export.append(song_info)            
            alb_name={ 'album_name': album_name}
            code={ 'code': 'pls'}            
            return make_response(jsonify(songs_export,alb_name,code))            

#_______________________________________A__D__M__I__N________________________________________________________________________________________________________________________________________________________________________________________________________

@app.route("/api/admin", methods=["GET"])
@jwt_required()
def admin():
    sg = Song.query.all()
    us = User.query.filter_by(user=1).all()
    usc = User.query.filter_by(creator=1).all()
    alb = Album.query.filter_by(asong_id=None).all()   

    g = []
    sgnm = []
    lisco = []
    for i in sg:
        if i.sgenre not in g:
            g.append(i.sgenre)
    for i in sg:
        sgnm.append(i.song_name)
        lisco.append(i.listen_count)

    if lisco:
        monitor = {
            'Users': len(us),
            'Creators': len(usc),
            'Songs': len(sg),
            'Albums': len(alb),
            'Genres': len(g)
        }
        return make_response(jsonify(monitor,sgnm,lisco), 200)
    return make_response(jsonify({}), 200)   
             

#--------------------------------------------------Admin Support-------------------------------------------------------------------------------------------------------------------------------------------   
@app.route("/admin_support", methods=["GET","POST"])
@jwt_required()
def admin_support():
    if request.method == "GET":
        artist_names_flaggedA=User.query.filter_by(usflag=1).all()
        song_names_flaggedA=Song.query.filter_by(soflag=1).all()
        artist_names_matchedA=User.query.filter_by(usflag=None).all()
        song_names_matchedA=Song.query.filter_by(soflag=0).all()
        album_names_matchedA=Album.query.filter_by(asong_id=None).all() 

        song_names_flagged=[]
        song_names_matched=[]
        artist_names_flagged=[]
        artist_names_matched=[]
        album_names_matched=[]

        for i in song_names_flaggedA:                
                    song_info = {
                        'song_id': i.song_id,
                        'song_name': i.song_name,
                        'artist_name': i.artist_name,
                        'rating': i.rating,
                        'sofile_id': url_for('static', filename='song_store/' + i.sofile_id),                        
                    }
                    song_names_flagged.append(song_info)

        for i in song_names_matchedA:                
                    song_info = {
                        'song_id': i.song_id,
                        'song_name': i.song_name,
                        'artist_name': i.artist_name,
                        'rating': i.rating,
                        'sofile_id': url_for('static', filename='song_store/' + i.sofile_id),                        
                    }
                    song_names_matched.append(song_info)

        for i in artist_names_flaggedA:                
                    artist_info = {
                        'artist': i.id,
                        'user_name': i.user_name,                                                
                    }
                    artist_names_flagged.append(artist_info)

        for i in artist_names_matchedA:                
                    artist_info = {
                        'artist': i.id,
                        'user_name': i.user_name,                                                
                    }
                    artist_names_matched.append(artist_info)

        for i in album_names_matchedA:                
                    album_info = {
                        'album_id': i.album_id,
                        'album_name': i.album_name,                                                
                    }
                    album_names_matched.append(album_info)

        return make_response(jsonify(artist_names_flagged,song_names_flagged,artist_names_matched,song_names_matched,album_names_matched),200)
#------------------------------------------------------Policy----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/policy", methods=["GET","POST"])
@jwt_required()
def policy():
    if request.method=="GET":
        return make_response(jsonify({'message': 'This is the Policy Page'}), 200)

#---------------------------------------------------Flag_Unflag--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
@app.route("/flag_unflag/<string:code>/<int:id>", methods=["GET","POST","PUT"])
@jwt_required()
def flag_unflag(code,id):
    if request.method=="GET":    
        if code=="s":            
            flagger=Song.query.filter_by(song_id=id).first()        
            flagger.soflag=1
            db.session.commit()
        if code == "u" :
            flagger=User.query.filter_by(id=id).first()
            flagger.usflag=1
            db.session.commit()
        if code == "ufs":
            flagger=Song.query.filter_by(song_id=id).first()
            flagger.soflag=0
            db.session.commit()
        if code == "ufa":
            flagger=User.query.filter_by(id=id).first()
            flagger.usflag=None
            db.session.commit()
    return make_response(jsonify({'message': 'Action Performed'}), 200)


@app.route("/logout",methods=["GET","POST"])
@jwt_required()
def logout():
    if request.method=='POST':    
        user=User.query.filter_by(id=get_jwt_identity()).first()        
        print(user)
        user.logout_time=datetime.now()
        db.session.commit()        
        return make_response(jsonify({'message': 'Logged out Successfully'}), 200)



@app.route('/export/report', methods=['POST'])
@jwt_required()
def export_songs():    
    user_id = get_jwt_identity()
    if request.method=='POST':
        try:

            from backend_jobs import export_song_details_as_csv

            csv_data = export_song_details_as_csv(user_id)
            response = make_response(csv_data)
            response.headers["Content-Disposition"] = "attachment; filename=song_report.csv"
            response.headers["Content-type"] = "text/csv"
            print(response)
            return response

        except Exception as e:
            return jsonify({'error': str(e)}), 500




def create_roles():
    # Define roles and their permissions
    roles_permissions = {
        'admin': 'admin-access',
        'user': 'user-access',
        'creator':'creator-access'
    }
    # Iterate over each role
    for role_name, role_permissions in roles_permissions.items():
        # Check if the role already exists
        role = Role.query.filter_by(name=role_name).first()
        # If the role does not exist, create it
        if not role:
            role = Role(name=role_name, description=role_permissions)
            # Add the new role to the session
            db.session.add(role)
    # Commit the session to save the changes
    db.session.commit()

def admin_create():
    # Get the admin role
    admin_role = Role.query.filter_by(name='admin').first()
    # Check if there is already a user with the admin role
    admin_user = User.query.filter(User.roles.any(id=admin_role.id)).first()

    # If there is no admin user, create one
    if not admin_user:
        # Define the admin email and password
        admin_email = 'musplayadmin@gmail.com'  # Change this email as needed
        admin_password = '6789'
        # Hash the password
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

        # Create the admin user
        admincr = user_datastore.create_user(user_name="ADMIN",email_id=admin_email, password=hashed_password,login_time=datetime.now(),user=-1,creator=-1,usflag=-1000)
        # Add the admin role to the user
        user_datastore.add_role_to_user(admincr, 'admin')
        # Commit the session to save the changes
        db.session.commit()
        return True
    return False

with app.app_context():
    db.create_all()
    create_roles()
    admin_create()

if __name__ == "__main__":
    
    app.secret_key = 'super secret key'     
    app.run(debug=True)