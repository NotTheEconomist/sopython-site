from flask import Flask, session
from flask_alembic import Alembic
from flask_alembic.cli.click import cli as alembic_cli
from flask_babel import Babel
from flask_oauthlib.client import OAuth
from sopy.ext.sqlalchemy import SQLAlchemy
from sopy.ext.views import template

alembic = Alembic()
babel = Babel()
db = SQLAlchemy()
oauth = OAuth()

oauth_so = oauth.remote_app(
    'Stack Exchange',
    authorize_url='https://stackexchange.com/oauth',
    access_token_url='https://stackexchange.com/oauth/access_token',
    access_token_method='POST',
    base_url='https://api.stackexchange.com/2.2/',
    app_key='OAUTH_SO'
)


def create_app(info=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('sopy.config.defaults')
    app.config.from_pyfile('config.py', True)

    app.cli.add_command(alembic_cli, 'db')

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    alembic.init_app(app)
    babel.init_app(app)
    db.init_app(app)

    from sopy.ext import views

    views.init_app(app)

    from sopy import auth, tags, sodata, canon, salad, wiki, pages

    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(tags.bp, url_prefix='/tags')
    app.register_blueprint(sodata.bp, url_prefix='/sodata')
    app.register_blueprint(canon.bp, url_prefix='/canon')
    app.register_blueprint(salad.bp, url_prefix='/salad')
    app.register_blueprint(wiki.bp, url_prefix='/wiki')
    app.register_blueprint(pages.bp, url_prefix='/pages')

    from sopy.salad.models import Salad

    @app.route('/')
    @template('index.html')
    def index():
        print(session)
        return {'wod': Salad.word_of_the_day()}

    return app
