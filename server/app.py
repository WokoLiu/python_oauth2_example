import os

from website.app import create_app

os.environ.setdefault('AUTHLIB_INSECURE_TRANSPORT', '1')  # use http

app = create_app({
    'SECRET_KEY': 'secret',
    'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:12345678@localhost:3306/test',
})


@app.cli.command()
def initdb():
    from website.models import db
    db.create_all()


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
