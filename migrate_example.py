from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from get_db import get_postgres_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_postgres_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)



class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    pets = db.relationship('Pet', backref='owner', lazy='dynamic')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    
if __name__ == '__main__':
    manager.run()
    
# Run this command in terminal to create local postgres db: `psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'my_db'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE my_db"`
# Initialize 1st migration: `python migrate_example.py db init` which will create migrations folder
# After define or make changes to models, run `python migrate_example.py db migrate`
# Run this if cant pip install pstcopg2 `env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip --no-cache install psycopg2`
# Then run `python migrate_example.py db upgrade` to update local database