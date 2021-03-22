from django.urls import path
from . import views
urlpatterns = [
    path("",views.blog,name="blog"),
    path("create/",views.create,name="create_article"),
    path("preview/",views.preview,name="preview"),
    path("draft/",views.draft,name="draft"),
    path("preview/<ids>/",views.preview_data,name="preview_data"),
    path("post/<ids>/",views.post,name="post"),
    path("edit/<ids>/",views.edit,name="edit"),
    path("posting/",views.posting,name="posting"),
    path("previewing/",views.previewing,name="previewing"),
    path("drafting/",views.drafting,name="drafting"),
    path("<user>/<title>/<ids>/",views.inside,name="inside"),
]