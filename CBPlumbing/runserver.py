"""
This script runs the CBPlumbing application using a development server.
"""

from os import environ

import sqlalchemy as sa
import sqlalchemy.orm as so

from CBPlumbing import app, db
from CBPlumbing.models import User

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User}