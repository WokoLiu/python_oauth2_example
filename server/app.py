from website.app import create_app

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
