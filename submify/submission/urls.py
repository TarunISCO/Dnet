from django.conf.urls import url

from submission.views import home


submission_patterns = [
    url(r'^$', home),
]

