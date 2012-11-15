from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'submit.views.index', name='index'),
    url(r'^login/$', 'submit.views.login', name='login'),
    url(r'^logout/$', 'submit.views.logout', name='logout'),
    url(r'^dashboard/$', 'submit.views.dashboard', name='dashboard'),
    url(r'^details/(?P<subm_id>\d+)/$', 'submit.views.details', name='details'),
    url(r'^details/(?P<subm_id>\d+)/file/$', 'submit.views.filedownload', name='filedownload'),
    url(r'^assignments/(?P<ass_id>\d+)/new/$', 'submit.views.new', name='new'),
    url(r'^withdraw/(?P<subm_id>\d+)/$', 'submit.views.withdraw', name='withdraw'),
    url(r'^update/(?P<subm_id>\d+)/$', 'submit.views.update', name='update'),
    url(r'^jobs/secret=(?P<secret>\w+)$', 'submit.views.jobs', name='jobs'),
    url(r'^test_validity/(?P<ass_id>\d+)/secret=(?P<secret>\w+)$', 'submit.views.test_validity', name='test_validity'),
    url(r'^test_full/(?P<ass_id>\d+)/secret=(?P<secret>\w+)$', 'submit.views.test_full', name='test_full'),
    url(r'^settings/$', 'submit.views.settings', name='settings'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# disables itself when DEBUG==FALSE
urlpatterns += staticfiles_urlpatterns()
