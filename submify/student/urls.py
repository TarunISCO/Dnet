from django.conf.urls import url
from  student import views
urlpatterns = [
    url(r'^$', views.student_detail, name='student_detail')
]
