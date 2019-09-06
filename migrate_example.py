import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
db = SQLAlchemy(app)

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
DB_CONFIG_PATH = os.path.join(THIS_DIR, 'db_config.ini')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

def parse_config(config_path=DB_CONFIG_PATH, section='postgresql'):
    """Read DB_CONFIG_PATH & parse the section postgresql in that file then return db credentials.

    Keyword Arguments:
        config_path {[type]} -- [description] (default: {DB_CONFIG_PATH})
        section {str} -- [description] (default: {'postgresql'})

    Raises:
        Exception: [If there's no section 'postgresql' in DB_CONFIG_PATH, then raise error]

    Returns:
        [list] -- [credentials for the db]
    """
    # create a parser
    parser = ConfigParser()

    # read the configuration
    parser.read(config_path)

    # get the section
    obj = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            obj[param[0]] = param[1]

    else:
        raise ValueError('Section {0} not found in the {1} file'.format(section, config_path))
    return obj

def get_postgres_url(config_path=DB_CONFIG_PATH, **config_overrides):
    url_base = 'postgresql+psycopg2://{user}:{password}@{host}/{database}'
    try:
        postgres_config = parse_config(config_path=config_path, section='postgresql')
    except Exception as exc:
        logging.debug('Exception while parsing Postgres config. {}: {}'.format(type(exc).__name__, str(exc)))
        postgres_config = {
            'user': os.environ.get('POSTGRES_USER', 'postgres'),
            'password': os.environ.get('POSTGRES_PASSWORD', ''),
            'host': os.environ.get('POSTGRES_HOST', 'localhost'),
            'database': os.environ.get('POSTGRES_DATABASE', 'mypostgresdb'),
        }
        postgres_config.update(config_overrides)
    postgres_url = url_base.format(**postgres_config)
    print("this is postgres_url", postgres_url)
    return postgres_url

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    pets = db.relationship('Pet', backref='owner', lazy='dynamic')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    new = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    
if __name__ == '__main__':
    manager.run()
    