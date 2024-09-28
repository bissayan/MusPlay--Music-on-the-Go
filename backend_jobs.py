# tasks.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import csv
from io import StringIO
from datetime import datetime, timedelta
from celery_config import celery
from app import db, User, Song ,Album
from celery.schedules import crontab



@celery.task
def generate_monthly_report():
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    users = User.query.filter_by(creator=1).all()
    
    song_filtered=[]
        
    for user in users:
        rate=Song.query.filter_by(artist=user.id).all()
        rating=0
        for r in rate:
            song_filtered.append(r)        
            if r.rating==None:
                rating=rating + 0 
            else:
                rating=rating + int(r.rating)
        
        if len(song_filtered)==0:
            g=1
        else:
            g=len(song_filtered)
        total_rating = int((rating)/g)
        count=0
        for i in Album.query.all():
            if int(i.artist)==int(user.id):
                if i.asong_id==None:
                    count+=1              
                        
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Monthly Activity Report</title>
        </head>
        <body>
            <h1>Monthly Activity Report - {current_month} {current_year}</h1>
            <p>Hello {user.user_name},</p>
            <p>Here's your activity summary for the month of {current_month} {current_year}:</p>
            <ul>
                <li>Your Total Songs: {g}</li>
                <li>Total Rating: {total_rating}</li>
                <li>Your Total Albums: {count}</li>
            </ul>
            <p>Thank you for Creating Songs on our Platform, Our Audience are waiting to hear more from you !!!</p>
            <p>Best regards,</p>
            <p>MusPlay Team</p>
            <p> For further support reach out us at musplayadmin@gmail.com </p>
        </body>
        </html>
        """
        send_email(user.email_id, html_content,'Monthly Activity Report')


@celery.task
def daily_reminders():        
        all_users = User.query.filter_by(user=1).all()
        for user in all_users:
            reminder_time = datetime.utcnow() - timedelta(days=1)
            user_listens_today = User.query.filter_by(id=user.id).filter(user.login_time >= reminder_time).all()
            
            if not user_listens_today:
                html_content = f"""<!DOCTYPE html>
                                    <html>
                                    <head>
                                        <title>Daily Remainder</title>
                                    </head>
                                    <body>                                    
                                        <p>Hello {user.user_name},</p>                                    
                                        <p>It seems like you haven't listened to our latest songs today. Check out the Trends and Vibe with the Beats perfect to fit your mood on the Go.</p>
                                        <p>Best regards,</p>
                                        <p>MusPlay Team</p>
                                        <p> For further queries reach out us at musplayadmin@gmail.com </p>
                                    </body>
                                    </html>
                                """
                send_email(user.email_id, html_content,'Daily Reminder')


def send_email(to_email, html_content,subjected):
    from_email = 'sayaniitmadras2026@gmail.com'
    subject = subjected

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    part1 = MIMEText(html_content, 'html')
    msg.attach(part1)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'sayaniitmadras2026@gmail.com'
    smtp_password = 'rpuu xpbc qace gnib'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())


@celery.task
def export_song_details_as_csv(creator_user_id):
    songs = Song.query.filter_by(artist=creator_user_id).all()
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(["Song Name", "Genre", "Lyrics","Artist Name","Date Created", "Listen Count", "Rating"])
    for song in songs:
        csv_writer.writerow([str(song.song_name),str(song.sgenre),str(song.lyrics),str(song.artist_name),str(song.date_created),song.listen_count,song.rating])
    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, "csv/song_report.csv")
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_buffer.getvalue())
    return csv_buffer.getvalue()



            



    



        