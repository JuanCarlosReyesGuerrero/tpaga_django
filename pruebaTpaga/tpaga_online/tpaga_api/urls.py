from django.conf.urls import url

#from tpaga_api.views import TpagaTestClient
from tpaga_api.views import TpagaTestClient

urlpatterns = [
    # url(r'^api/$', views.serie_list),
    # url(r'^api/(?P<pk>[0-9]+)/$', views.serie_detail),

    # url(r'^tpaga/$', views.TpagaTestClient.as_view()),
    # url(r'^fecha/$',fecha_actual),
    # url(r'^acerca/',VistaSaludo.as_view(saludo="Quetal")),
    url(r'^tpaga/',  TpagaTestClient.as_view())
]
