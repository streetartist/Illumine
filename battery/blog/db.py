from peewee import*

db = SqliteDatabase('main.db')

class Post(Model):
    time = CharField()
    content = CharField()
    author = CharField()
    tag = CharField()
    title = CharField()
    class Meta:
        database = db

db.create_tables([Post])