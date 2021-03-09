from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="blog"),
    path("create/",views.create,name="create"),
    path("preview/content/<ids>/",views.preview,name="preview"),
    path("post/content/<ids>/",views.post,name="post"),
    path("edit/content/<ids>/",views.edit,name="edit"),
    path("draft/content/save/",views.draft,name="draft"),
    path("draft/content/saved/<ids>/",views.drafted,name="drafted"),
    path("delete/content/<ids>/",views.delete,name="delete"),
    path("<title>/<id>/",views.inside,name="inside"),
]