from flask import Markup, url_for
from flask_appbuilder.models.mixins import AuditMixin, FileColumn
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from flask_appbuilder.filemanager import get_file_original_name


class tenders(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
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

class Tasks(Model):
    id = Column(Integer, primary_key=True)
    tender_id = Column(Integer, ForeignKey('tenders.id'))
    tenders = relationship('tenders')
    start = Column(Date)
    end = Column(Date)
    description = Column(String)
    parent = Column(Integer)
    relatedOn = Column(Integer)

    def __repr__(self):
        return self.description

    def len(self):
        return (self.end - self.start).days if self.start is not None and self.end is not None else None

    
class Users(Model):
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    tasks = relationship('Tasks')
    name = Column(String)
    surname = Column(String)

    def __repr__(self):
        return self.name


class taskFile(Model):
    pid = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey("tasks.id"))
    tasks = relationship("Tasks")
    file = Column(FileColumn, nullable=False)
    description = Column(String(150))

    def download(self):
        return Markup(
            '<a href="'
            + url_for("taskFileView.download", filename=str(self.file))
            + '">Download</a>'
        )

    def file_name(self):
        return get_file_original_name(str(self.file))

class taskComm(Model):
    pid = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey('tasks.id'))
    tasks = relationship('Tasks')
    comm = Column(Text)

    def __repr__(self):
        return self.comm


