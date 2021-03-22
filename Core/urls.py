from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("like/",views.like,name="like"),
     path("dislike/",views.dislike,name="dislike"),
     path("follow/",views.follow,name="follow"),
     path("mark/",views.mark,name="mark"),
     path("profile/<user>/",views.profile,name="profile"),
     path("photo/upload/list/",views.photo_upload,name="photo_upload"),
     path("video/upload/list/",views.video_upload,name="video_upload"),
     path("post/upload/list/",views.post_upload,name="post_upload"),
     path("settings/",views.settings,name="settings"),
     path("notifications/",views.notifications,name="notifications"),
     path("bookmarks/",views.bookmarks,name="bookmarks"),
     path("activities/<method>/<value>/",views.activities,name="activities"),
     path("analytics/",views.analytics,name="analytics"),
     path("news/<topic>/",views.news,name="news"),
     path("news/ajax/fetch",views.ajax_news,name="ajax_news"),
]