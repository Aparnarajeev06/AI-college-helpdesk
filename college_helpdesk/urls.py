
from django.contrib import admin
from django.urls import path
from helpdesk.views import chat_api, home, feedback_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("api/chat/", chat_api, name="chat_api"),
    path("api/feedback/", feedback_api, name="feedback_api"),
]
