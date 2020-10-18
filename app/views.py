from flask import redirect
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.actions import action
from flask_appbuilder.models.sqla.filters import *
import datetime

from flask_appbuilder.charts.views import DirectByChartView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count, aggregate_sum, aggregate_avg

from app import appbuilder, db
from .models import *

class DistChartView(GroupByChartView):
    datamodel = SQLAInterface(tenders)
    chart_title = 'Status Disctribution'
    chart_type = 'PieChart'
    #chart_3d = True

    definitions = [
    {
        #'label': 'status',
        'group': 'status',
        'series': [(aggregate_count,'status')]
    }
]


class linkedView(ModelView):
    datamodel = SQLAInterface(linked)
    list_columns = ['href']


class descView(ModelView):
    datamodel = SQLAInterface(Desc)
    list_columns = ['desc']


class commView(ModelView):
    datamodel = SQLAInterface(Comm)
    list_columns = ['comm']

class FilesModelView(ModelView):
    datamodel = SQLAInterface(files)
    #label_columns = {"file_name": "File Name", "download": "Download"}
    #add_columns = ["file", "description",'id']
    #edit_columns = ["file", "description",'id']
    list_columns = ["file_name", "download"]
    #show_columns = ["file_name", "download"]    


class tendersView(ModelView):
    datamodel = SQLAInterface(tenders)
    related_views = [linkedView, descView, commView, FilesModelView]

    #show_template = "appbuilder/general/model/show_cascade.html"
    #edit_template = "appbuilder/general/model/edit_cascade.html"
    
    #add_columns = ["name",'Sdate','status']
    #edit_columns = ["name",'Sdate','status']
    list_columns = ["name", "Sdate", "status"]
    #show_fieldsets = [("Info", {"fields": ["name"]})]
    
    
    d = datetime.datetime.strftime(datetime.date.today() + 
datetime.timedelta(days=3),'%Y-%m-%d')
    base_filters = [['status', FilterNotEqual, 'declined'],
	['status', FilterNotEqual,'dub'],
	['status', FilterNotEqual,'PIN'],
       # ['status', FilterNotEqual,'cancelled'],
	['status', FilterNotEqual,'outdated'],
       # ['status', FilterEqual, 'sent'],
       # ['status', FilterEqual, 'active'],
       # ['Sdate', FilterGreater, d]
        ]
    base_order = ('Sdate','asc')

    @action(
        "decline", "Decline", "Do you really want to?", "fa-rocket"
    )
    def decline(self, item):
        if isinstance(item, list):
            for i in item:
                i.status = 'declined'
                self.datamodel.edit(i)
                self.update_redirect()
        else:
            item.status = 'declined'
            self.datamodel.edit(item)
        return redirect(self.get_redirect())


    @action(
        "web", "Web", "Do you really want to?", "fa-rocket"
    )
    def web(self, item):
        item.status = 'web'
        self.datamodel.edit(item)
        return redirect(self.get_redirect())


    @action(
        "review", "Review", "Do you really want to?", "fa-rocket"
    )
    def review(self, item):
        item.status = 'review'
        self.datamodel.edit(item)
        return redirect(self.get_redirect())

    @action(
        "hard", "Hardware", "Do you really want to?", "fa-rocket"
    )
    def hard(self, item):
        item.status = 'hardware'
        self.datamodel.edit(item)
        return redirect(self.get_redirect())

    @action(
        "dub", "Dublicated", "Do you really want to?", "fa-rocket"
    )
    def dub(self, item):
        item.status = 'dub'
        self.datamodel.edit(item)
        return redirect(self.get_redirect())


'''
    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())
'''
db.create_all()

appbuilder.add_view(
    tendersView,
    "Tenders",
    icon="fa-folder-open-o",
    category="Contacts",
    category_icon="fa-envelope",
)

appbuilder.add_view(
    linkedView,
    "Links",
    icon="fa-folder-open-o",
    category="Contacts",
    category_icon="fa-envelope",
)

appbuilder.add_view(
    descView,
    "Description",
    icon="fa-folder-open-o",
    category="Contacts",
    category_icon="fa-envelope",
)

appbuilder.add_view(
    commView,
    "Comments",
    icon="fa-folder-open-o",
    category="Contacts",
    category_icon="fa-envelope",
)

appbuilder.add_view(
    FilesModelView,
    "Files",
    icon="fa-folder-open-o",
    category="Contacts",
    category_icon="fa-envelope",
)

appbuilder.add_view(
    DistChartView,
    "Category Distribution",
    icon="fa-folder-open-o",
    category="Contacts",
    category_icon="fa-envelope",
)
