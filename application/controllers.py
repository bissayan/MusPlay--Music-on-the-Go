from flask import request,render_template,redirect,flash,jsonify, request, make_response, url_for
from sqlalchemy import desc
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
from flask_bcrypt import Bcrypt
from datetime import datetime ,timedelta
#from flask_security import  login_user, logout_user, current_user
#from flask_security import *
#from werkzeug.security import *
#from flask_security import roles_required, auth_token_required 
#from flask_security.utils import verify_password, hash_password
from app import user_datastore

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from .models import db,User, Album, Playlist, Song
from flask import current_app as app

bcrypt = Bcrypt(app)

jwt = JWTManager(app)

#from flask_cors import CORS
#CORS(app)





# landing page
@app.route('/')

def index():    
    return redirect("/user_creator/1")


# controller for login user
@app.route("/api/login", methods=["GET","POST"])
def login_dev():
    if request.method == "GET":
        #existing_emails = User.query.with_entities(User.email_id).all()        
        #email_addresses = [email[0] for email in existing_emails]
        #print(existing_emails) 
        return make_response(jsonify({'message': 'Login Loaded'}), 200)            
        #return make_response(jsonify(email_addresses), 200)
    if request.method == "POST":
            logdata=request.get_json()
            email_id = logdata["email_id"]
            password = logdata["password"]
            user = user_datastore.find_user(email_id=email_id)
            print(user, password)
            #print(dcrypt(user.password))
            #print( email,password)
            #user = User.query.filter_by(email_id=email_id).first()     
        
            if bcrypt.check_password_hash(user.password, password):
                #login_user(user)
                user.login_time=datetime.now() 
                #db.session.commit()
                #auth_token = user.get_auth_token()
                print(user)
                db.session.commit()

                access_token = create_access_token(
                identity=user.id, expires_delta=timedelta(days=1))
                user_info = {
                    'user_id': user.id,
                    'user_name': user.user_name,                    
                    'role': [role.name for role in user.roles],
                }

                return jsonify({'access_token': access_token, 'user': user_info}), 200


                #return make_response(jsonify({'message': 'User logged in successfully', 'auth_token': auth_token, 'id': current_user.id,'email': current_user.email_id,'roles': [role.name for role in current_user.roles]}), 200)
                                               
                #return redirect('/test')
            else:
                flash("Wrong Password")
                return make_response(jsonify({'message': 'You entered wrong password'}), 400)
            
                #return redirect("/login")
        
        
            #return redirect("/login")


# controller to register user
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
        #existing_email = User.query.filter_by(email_id = email).first()
        #if existing_email:
            #flash("email already register")
            #return redirect("/login")
        #else:
                password = data["password"]
            #confirm_password=data['confirm_password']
            #if bool(confirm_password!=password):
                #return redirect("/login")
            #else:
                print(email,password)
                user_name=data['user_name']              
                hashed_password = bcrypt.generate_password_hash(password)               
                login_time=datetime.now()               
                user=1
                creator=0
                new_user = user_datastore.create_user(user_name=user_name,email_id=email, password=hashed_password,login_time=login_time,user=user,creator=creator)
                #new_user= User(email_id=email,password = hashed_password,user=user,user_name=user_name,login_time=login_time, creator=creator )
                db.session.add(new_user)
                user_datastore.add_role_to_user(new_user, 'user')
                db.session.commit()
                #flash("You are now registered, Please Login.")
                #return redirect("/login")
                return make_response(jsonify({'message': 'User has been registered successfully'}), 200)
    #return "register endpoint is working", 200
        
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
        #if existing_user:
                new_password = data["password"]
            #con_password = data["con_password"]
            #if con_password==new_password:
                hashed_password = bcrypt.generate_password_hash(new_password)
                existing_user.password = hashed_password
                db.session.commit()
                flash("Password changed,Login with new.")
                #return redirect('/login')
                return make_response(jsonify({'message': 'Your password has been changed successfully'}), 200)
            #else:
                flash("Passwords did not Match . Enter Again")
                #return redirect('/forget_password')
                return make_response(jsonify({'message': 'Your passwords did not match'}), 400)
        #else:
           # flash("You are not registered. Register Now!")
            #return redirect('/register')
            #return make_response(jsonify({'message': 'Your not registered'}), 404)

#--------------------------------------------------------Search------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/search/<string:query>", methods=["GET","POST"])
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
                        'rating': i.rating,
                        'sofile_id': url_for('static', filename='song_store/' + i.sofile_id),                        
                    }
                    genre_matchedA.append(song_info)

        for i in song_names_matched:                
                    song_info = {
                        'song_id': i.song_id,
                        'song_name': i.song_name,
                        'artist_name': i.artist_name,
                        'rating': i.rating,
                        'sofile_id': url_for('static', filename='song_store/' + i.sofile_id),                        
                    }
                    song_names_matchedA.append(song_info)

        for i in album_genre_matched:                
                    album_info = {
                        'album_id': i.album_id,
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
                    }
                    album_names_matchedA.append(album_info)

        return make_response(jsonify(album_genre_matchedA,genre_matchedA,artist_names_matchedA,song_names_matchedA,album_names_matchedA),200)










        
        
        if len(song_names_matched)==len(artist_names_matched)==len(album_names_matched)==len(genre_matched)==len(album_genre_matched)==0:
          fonof=12           
        return render_template("search.html",song_names_matched=song_names_matched,artist_names_matched=artist_names_matched,album_names_matched=album_names_matched,genre_matched=genre_matched,songre_names_matched=0,album_genre_matched=album_genre_matched,code=id_type,fonof=0,query=query[1:-1])
                         
#--------------------------------------------------User/Creator------------------------------------------------------------------------------

@app.route('/user_creator/<int:value>',methods=['GET','POST'])

#@cache.cached(timeout=10)
#@roles_accepted('user')
#@auth_token_required
def user_creator(value):
  if request.method == "GET":
        user_id = 1 #current_user.id
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
        #return render_template('page_user.html' ,user=uc, songs=song,albums=ll,playlist=l)
        #return song
        songs_export=[]        
        for song in song_filtered:                    
                        song_info = {
                            'song_id': song.song_id,
                            'song_name': song.song_name,
                            'artist_name': song.artist_name,
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
        return make_response(jsonify(songs_export,albums_export), 200)
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
        #return redirect("/user_creator/1")
        return make_response(jsonify(" Rated It "), 200) 
  
#_________________________________________Creator____________________________________________________
      
@app.route('/creator',methods=['GET','POST'])

#@cache.cached(timeout=10)
#@roles_required('creator')
#@auth_token_required
def creator():
  if request.method == "GET":
        user_id =1 #current_user.id
        user=User.query.filter_by(id=user_id).first()
        son1=Song.query.order_by(desc(Song.date_created)).all()    
        alb1=Album.query.all()
        l=[]
        for d in alb1:
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
                            'rating': song.rating,
                            'sofile_id': url_for('static', filename='song_store/' + song.sofile_id),                        
                        }
                        songs_export.append(song_info)        
        albums_export=[]        
        for album in l:                   
                        album_info = {
                            'album_id': album.album_id,
                            'album_name': album.album_name,                                                
                        }
                        albums_export.append(album_info)
        if user.usflag!=1:
            print(m)
            usered={
                 'user_name': user.user_name,
                 'usflag': user.usflag
            }
            #flag=user.usflag
            monitor = {
            #'Users': len(us),
            #'Creators': len(usc),
            'Songs': len(song_filtered),
            'Albums': len(l),
            'Rating': int((rating)/g)
        }
            #return render_template('page_creator.html' , user=uc,songs=k,albums=m,j=l,sg=len(k),albms=len(l))
            return make_response(jsonify(songs_export,albums_export,monitor,usered), 200)
        else:
            return redirect("/policy/0")



#   To become creator
@app.route('/user/creator',methods=['GET','POST'])

#@roles_required('user')
#@auth_token_required
def become_creator():
  user_id =1 #current_user.id
  user=User.query.filter_by(id=user_id).first()
  if request.method=='GET':      
      user.creator=1
      db.session.commit()
  return redirect("/user_creator/2")

#----------------------------------------------------Song---------------------------------------------------------------------------------
import json
@app.route('/song/create', methods=['GET','POST'])

#@roles_required('creator')
#@auth_token_required
def Song_Creation():
    user_id =1 #current_user.id
    #uc=User.query.filter_by(id=user_id).first()
    if request.method=='POST':
        
        song = json.loads(request.form['data'])
        print(song)
        # issue from here about current_user and frontend integration
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
        artist=1 #user_id
        lyrics=song.get('lyrics','').strip()

       

        artist_name="Rabi" #uc.user_name
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
        #return redirect('/user_creator/2')
        return make_response(jsonify({'message': 'Song Created'}), 200)       
    else:       
       #return render_template('Song_Creation.html' , s=uc)
        return make_response(jsonify({'message': 'More datapoints required'}), 200)
    
#----------------------------------------------------Album--------------------------------------------------------------------------------------------------------------

@app.route('/album/create', methods=['GET','POST'])

#@roles_required('creator')
#@auth_token_required
def Album_Creation():
    user_id = 1 #current_user.id
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
        '''son1=Song.query.all()
        alb1=Album.query.all()
        k=[]
        m=[]
        l=[]
        for d in alb1:
         if d.asong_id==None:
            l.append(d)
            albm_id_counter.append(d.album_id)
        for s in son1:
           if int(s.artist)==int(user_id):
              k.append(s)
        for i in l:
           if int(i.artist)==int(user_id):
              m.append(i)       
        #return redirect("/user_creator/2")'''
        return make_response(jsonify({'message': 'Album Created'}), 200)              
    else:       
       return render_template('Album_Creation.html',s=uc) 


@app.route('/playlist/create', methods=['GET','POST'])

#@roles_required('user')
#@auth_token_required
def Playlist_Creation():
    user_id =1 #current_user.id
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
        
        #return redirect("/user_creator/1") 
        return make_response(jsonify({'message': 'Playlist Created'}), 200)       
    else:       
       return render_template('Playlist_Creation.html',s=uc) 


@app.route('/song/<string:song_id>/<int:value>/add', methods=["GET","POST"])

#@roles_required('user','creator')
#@auth_token_required
def add_song(song_id,value):
    user_id =1 #current_user.id
    uc=User.query.filter_by(id=user_id).first()
    if len(song_id) > 1:
        asong_id=int(song_id.split("::")[1])
        ku=Song.query.filter_by(song_id=asong_id).first()
    else:
        ku=Song.query.filter_by(song_id=song_id).first()
    song=ku 
    print(song)   
    #print(song_id.split("::"))
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
            #print(son1)
            for song in l:                
                    show_info = {
                        'album_id': song.album_id,
                        'album_name': song.album_name,                                                
                    }
                    albums.append(show_info)           
            return make_response(jsonify(song_info,albums), 200)          
       else:
          #addata=request.get_json()
          album_id= int(song_id.split("::")[0]) #addata['album_id']              
          count=(Album.query.filter_by(album_id=album_id).first()).sl_no                  
          ak=Album.query.filter_by(sl_no=count).first()                
          i_add=Album(album_id=album_id, album_name=ak.album_name, agenre=ak.agenre, artist=user_id,asong_id=asong_id)          
          db.session.add(i_add)
          db.session.commit()
          #return render_template("Song_View.html",a=uc,c=l,k=ku,code=2)
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
            #print(son1)
            for song in ll:                
                    show_info = {
                        'playlist_id': song.playist_id,
                        'playlist_name': song.playlist_name,                                                
                    }
                    playlists.append(show_info)           
            return make_response(jsonify(song_info,playlists), 200)        
        #return render_template("Song_View.html",a=uc,c=ll,k=ku,code=1)
       else:
          #addplay=request.get_json()
          playist_id=int(song_id.split("::")[0]) #addplay['playlist_id']     
          count=(Playlist.query.filter_by(playist_id=playist_id).first()).sl_no        
          ap=Playlist.query.filter_by(sl_no=count).first()      
          i_add=Playlist(playist_id=playist_id, playlist_name=ap.playlist_name, pgenre=ap.pgenre, puser_id=user_id,psong_id=asong_id,pdate_created=datetime.now())
          db.session.add(i_add)
          db.session.commit()
          #return render_template("Song_View.html",a=uc,c=ll,k=ku,code=1)
          return make_response(jsonify({'message': 'Song added to Playlist'}), 200)
#---------------------------------------------------Delete-----------------------------------------------------------------------------------
@app.route('/user/<string:id>/<string:code>/delete', methods=["GET","POST","DELETE"])
#@roles_required('creator')
#@auth_token_required
def delete(id,code):
   print(id)
   '''print(code[:2])
   print(code[-2:])
   print(code[2:])'''
   if request.method == "GET":
        if code[:1] =="u":
            user_id=int(id)
            db.session.delete(User.query.filter_by(id=user_id).one())
            sgd=Song.query.filter_by(artist=user_id).all()
            for i in sgd:
           #print(i)
                db.session.delete(i)
            ply=Playlist.query.filter_by(puser_id=user_id).all()
            for j in ply:
           #print(j)
                db.session.delete(j)
            db.session.commit()       
            albd=Album.query.filter_by(artist=user_id).all()
            for j in albd:
           #print(j)
                db.session.delete(j)
            db.session.commit()
            if code[-2:]=="ad":
        #return redirect('/admin_support')
                return make_response(jsonify({'message': 'Admin deleted User'}), 200)
            else:
           #return redirect("/login")
                return make_response(jsonify({'message': 'User deleted Account'}), 200)
           
        elif code[:2] == "sl":
            l=(Song.query.filter_by(song_id=int(id)).first())
            l.lyrics=""
            db.session.commit()
            #print(code[-2:])
            #print(code[2:])
            if code[-2:]=="ad":
                #return redirect('/admin_support')
                return make_response(jsonify({'message': 'Song lyrics deleted by Admin'}), 200)
            else:
                #return redirect("/user_creator/2")
                return make_response(jsonify({'message': 'Song lyrics deleted by Creator'}), 200)
        
        elif code[:2] == "sf":
            k=Song.query.filter_by(song_id=int(id)).first()       
            db.session.delete(k)
            db.session.commit()
            if code[-2:]=="ad":
                #return redirect('/admin_support')
                return make_response(jsonify({'message': 'Song deleted by Admin'}), 200)
            else:
                #return redirect("/user_creator/2")
                return make_response(jsonify({'message': 'Song deleted by Creator'}), 200)
       
        elif code[:3] == "alb":
            albd=Album.query.filter_by(album_id=id).all()
            for j in albd:           
                db.session.delete(j)
            db.session.commit()
            if code[-2:]=="ad":
                #return redirect('/admin_support')
                return make_response(jsonify({'message': 'Album deleted by Admin'}), 200)
            else:
                #return redirect("/user_creator/2")
                return make_response(jsonify({'message': 'Album deleted by Creator'}), 200)
        elif code[:3] == "als":
            #print(code)
            albs=Album.query.filter_by(album_name=id,asong_id=int(code[3:])).first()       
            db.session.delete(albs)
            db.session.commit()
            if code[-2:]=="ad":
                #return redirect('/admin_support')
                return make_response(jsonify({'message': 'Song in Album deleted by Admin'}), 200)
            else:
                #return redirect("/user_creator/2")
                return make_response(jsonify({'message': 'Song in Album deleted by Creator'}), 200)
        elif code[:3] == "pls":
            #print(code)
            plys=Playlist.query.filter_by(playlist_name=id,psong_id=int(code[3:])).first()
            db.session.delete(plys)
            db.session.commit()
            #return redirect('/user_creator/1')
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

#@roles_required('creator')
#@auth_token_required
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
       '''if code=="alb":
           albums=[]
           l=Album.query.filter_by(album_id=id).all()
           for i in l:
               if i.asong_id==None:
                   album_info = { 'album_name': i.album_name, }
           albums.append(album_info)
           return make_response(jsonify(albums))'''
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
        sgd.artist=1#user_id
        sgd.lyrics=song.get('lyrics','').strip()
        sgd.sofile_id=sofile_id     
                  
        db.session.commit()
        #return redirect('/user_creator/2')
        return make_response(jsonify({'message': 'Song has been edited'}), 200)
       #elif code=='alb':
        '''editdata=request.get_json()
           agd=Album.query.filter_by(album_id=id).all()           
           nmchng=editdata['album_name']
           for i in agd:
               i.album_name=nmchng
           db.session.commit()
           #return redirect('/user_creator/2')
           return make_response(jsonify({'message': 'Album has been edited'}), 200)
       else:
           #not req presently
           ugd=Song.query.filter_by(id=id).one()           
           ugd.username=editdata['username']
           db.session.commit()
           #return redirect('/user_creator/1')
           return make_response(jsonify({'message': 'Artist name of song has been edited'}), 200)'''



@app.route('/user/<int:id>/<string:code>/edit_album',methods=["GET","POST"])
#@roles_required('creator')
#@auth_token_required
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

#@roles_required('user','creator')
#@auth_token_required
def view(id,value):
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
                            'rating': song.rating,
                            'sofile_id': url_for('static', filename='song_store/' + song.sofile_id),                        
                        }
                        songs_export.append(song_info)            
            alb_name={ 'album_name': album_name}
            code={ 'code': 1}
            codr={ 'codr': 1 } #current_user.creator}
            return make_response(jsonify(songs_export,alb_name,code,codr))
            #return render_template("albply_view.html",songs=albsong,album_name=albname,code=1,codr=current_user.creator)
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
                            'rating': song.rating,
                            'sofile_id': url_for('static', filename='song_store/' + song.sofile_id),                        
                        }
                        songs_export.append(song_info)            
            alb_name={ 'album_name': album_name}
            code={ 'code': 0}
            codr={ 'codr': 0 } #current_user.creator}
            return make_response(jsonify(songs_export,alb_name,code,codr))
            #return render_template("albply_view.html",songs=albsong,album_name=albname,codr=current_user.creator)
#-------------------------------------------------------LogouT---------------------------------------------------------------------------------------------------------------------------
@app.route("/logout",methods=["GET","POST"])

def logout():
    if request.method=='GET':
    
        #user=User.query.filter_by(id= current_user.id).first()
        user=1 #User.query.filter_by(id= current_user.id).first()
        print(user)
        user.logout_time=datetime.now()
        db.session.commit()
        #logout_user()
        #return redirect("/login")
        return make_response(jsonify({'message': 'Logged out Successfully'}), 200)