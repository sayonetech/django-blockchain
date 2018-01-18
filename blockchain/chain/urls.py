from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/v0/', include('chain.api.v0.urls'), name='api'),
]
