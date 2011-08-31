from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.views.generic.date_based import archive_index



admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^site_media/(.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT}),
    (r'^$', 'subscribe.views.inscrever'),
    (r'^editar_inscrito/(?P<codigo>\d+)/$', 'subscribe.views.editar_inscrito'),
    (r'^listar_inscritos/(?P<codigo>\d+)$', 'subscribe.views.listar_inscritos'), 
    (r'^mostrar_aprovado/(?P<codigo>\d+)/$', 'subscribe.views.mostrar_aprovado'),
    (r'^principal/$', 'subscribe.views.principal'),
    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'logout.html', 'next_page': '/login'}),

)
