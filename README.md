# snake_snake
Online multiplayer snake game!

| **Coverage Status** | [![Coverage Status](https://coveralls.io/repos/github/V1ckeyR/snake_snake/badge.svg?branch=main)](https://coveralls.io/github/V1ckeyR/snake_snake?branch=main) |


## How to start server

    gunicorn --worker-class eventlet -w 7 app:app
