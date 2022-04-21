# snake_snake
Online multiplayer snake game!

## How to start server

    gunicorn --worker-class eventlet -w 7 app:app
