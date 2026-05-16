import peewee

from louvores.db.database import db


class Coletanea(peewee.Model):
    codigo = peewee.CharField()
    titulo = peewee.CharField()

    class Meta:
        database = db


class Hino(peewee.Model):
    coletanea = peewee.ForeignKeyField(Coletanea, backref="hinos")
    numeracao = peewee.IntegerField(null=True)
    titulo = peewee.CharField()
    letra = peewee.TextField(null=True)
    creditos = peewee.CharField(null=True)
    revisado = peewee.BooleanField(default=False)

    class Meta:
        database = db
