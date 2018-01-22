from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, health
import welcome.views
urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index),
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^player/', welcome.views.playerpage, name='playerpage'),
    url(r'^online/', welcome.views.onlinepage, name='onlinepage'),
    url(r'^time/', welcome.views.timepage, name='timepage'),
    url(r'^attacks/', welcome.views.attackpage, name='attackpage'),
    url(r'^playerdata/', welcome.views.playerdata, name='playerdata'),
    url(r'^timeintervaldata/', welcome.views.timeintervaldata, name='timeintervaldata'),
    url(r'^onlinedata/', welcome.views.onlinedata, name='onlinedata'),
    url(r'^attack_analyzer/', welcome.views.attack_analyzer, name='attack'),
    url(r'^session/', welcome.views.update_world, name='session'),
    url(r'^update/', welcome.views.update_log, name='logs'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
