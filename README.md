MusPlay is a full-stack music streaming and management application built with Flask (Python) for the backend and Vue.js for the frontend. It allows users to register, log in, create and manage songs/albums/playlists, track listens, and visualize performance with interactive charts.

Demo Video Link: https://drive.google.com/file/d/1_EBk9edtjpfNR7Q67bQq72FoflzFuo-m/view?usp=drive_link

Features:
Authentication & Authorization using JWT
Song Management – Upload, stream, rate, and delete songs.
Album Management – Create, edit, and manage albums.
Performance Analytics – Visualize listens & ratings with Chart.js.
Role-Based Access Control (RBAC) – User, Creator, and Admin.

Tech Stack:
Backend: (Python/Flask-JWT-Extended)
Flask-SQLAlchemy (ORM), SQLite (configurable)
Frontend (Vue.js - Vue 3 with Vuex & Vue Router

```plaintext
musplay_music_app_/
│── backend/                # Flask backend
│   ├── app.py              # Entry point
│   ├── models.py           # Database models
│   ├── config.py           # Config (DB, JWT, OAuth)
│   ├── requirements.txt    # Backend dependencies
│── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── store/          # Vuex store
│   │   ├── router/         # Vue Router
│   ├── package.json        # Frontend dependencies
│── README.md               # Project documentation

