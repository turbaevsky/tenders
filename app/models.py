from flask import Markup, url_for
from flask_appbuilder.models.mixins import AuditMixin, FileColumn
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from flask_appbuilder.filemanager import get_file_original_name


class tenders(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Integer)
    length = Column(Integer)
    len_unit = Column(String(5))
    Qdate = Column(Date)
    Sdate = Column(Date)
    Adate = Column(Date)
    status = Column(String(10))
    added = Column(Date)
    #comm = Column(String)

    def __repr__(self):
        return self.name

class files(Model):
    pid = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey("tenders.id"))
    tend = relationship("tenders")
    file = Column(FileColumn, nullable=False)
    description = Column(String(150))

    def download(self):
        return Markup(
            '<a href="'
            + url_for("FilesModelView.download", filename=str(self.file))
            + '">Download</a>'
        )

    def file_name(self):
        return get_file_original_name(str(self.file))

class linked(Model):
    pid = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey('tenders.id'))
    ltenders = relationship('tenders')
    link = Column(String)

    def __repr__(self):
        self.link

    def href(self):
        return Markup('<a href="' + self.link + '">link</a>')

class Desc(Model):
    pid = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey('tenders.id'))
    dtenders = relationship('tenders')
    desc = Column(Text)

    def __repr__(self):
        return self.desc

class Comm(Model):
    pid = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey('tenders.id'))
    dcomm = relationship('tenders')
    comm = Column(Text)

    def __repr__(self):
        return self.comm

   
