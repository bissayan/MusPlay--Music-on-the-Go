from flask import request,render_template,redirect,flash,session,url_for,jsonify, make_response
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
#from app import*

from flask_security import  login_user, logout_user, current_user

from .models import db,User, Album, Song
from flask import current_app as app

#from flask_login import login_user, LoginManager, login_required, logout_user, current_user
#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login'


from app import user_datastore

@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    # for rendering admin login page
    #if request.method == "GET":        
        #return render_template("Loginnn.html",deter=3 )
    
    # get email and password and check those and then login admin
    # username for admin = musplayadmin@gmail.com
    # password for admin = 6789
    if request.method == "POST":
            #email = request.form["email_id"]
            #password = request.form["password"]
        #if (email == "musplayadmin@gmail.com" and password=="6789"):
            #session['email'] = email
            #return redirect('/admin')
            logdata=request.get_json()
            email_id = logdata["email_id"]
            user = user_datastore.find_user(email_id=email_id)
            login_user(user)             
                
            auth_token = user.get_auth_token()
            return make_response(jsonify({'message': 'Admin logged in successfully', 'auth_token': auth_token, 'id': current_user.id,'email': current_user.email_id,'roles': [role.name for role in current_user.roles]}), 200)
                        #else:
            flash('You are not allowed to acess admin page')
            #return redirect('/login')
            return make_response(jsonify({'message': 'false'}), 400)
        

#---------------------------------------------------Admin------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/api/admin", methods=["GET"])
def admin():
    sg = Song.query.all()
    us = User.query.filter_by(user=1).all()
    usc = User.query.filter_by(creator=1).all()
    alb = Album.query.filter_by(asong_id=None).all()

    matplotlib.use('Agg')

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
        plt.bar(sgnm, lisco, color='blue', width=0.4)
        plt.xlabel("Song Names")
        plt.ylabel("Listen Count")
        plt.title("Song Performance")

        filename = 'SongPeB.png'
        filepath = os.path.join(os.path.join(app.root_path, 'say2vue', 'public', 'static', 'song_store'), filename)
        plt.savefig(filepath)
        plt.close()

        monitor = {
            'Users': len(us),
            'Creators': len(usc),
            'Songs': len(sg),
            'Albums': len(alb),
            'Genres': len(g)
        }

        return make_response(jsonify(monitor), 200)

    return make_response(jsonify({}), 200)    
            #return render_template('admin_dashboard.html',sg=len(sg),us=len(us),usc=len(usc),alb=len(alb),usf=1,usong=usong,g=len(g))
        #else:
            #return ("You are not allowed to access admin page") 

#--------------------------------------------------Admin Support-------------------------------------------------------------------------------------------------------------------------------------------   
@app.route("/admin_support", methods=["GET","POST"])
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
@app.route("/policy/<int:code>", methods=["GET","POST"])
def policy(code):
    return render_template("policy.html",code=code)

#---------------------------------------------------Flag_Unflag--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
@app.route("/flag_unflag/<string:code>/<int:id>", methods=["GET","POST","PUT"])
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
    