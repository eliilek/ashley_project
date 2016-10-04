from django.conf.urls import include, url

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^session', hello.views.session, name='session'),
    url(r'^subject/(?P<subid>[0-9]+)/$', hello.views.subject, name='subject'),
    url(r'^subject/(?P<subid>[0-9]+)/edit', hello.views.edit_subject, name='edit_subject'),
    url(r'^response_set/(?P<responseid>[0-9]+)', hello.views.response_set, name='response_set'),
    url(r'^trial', hello.views.trial, name='trial'),
    url(r'^myself', hello.views.myself, name='myself'),
    url(r'^report_results', hello.views.report_results, name='report_results'),
    url(r'^phase/(?P<subid>[0-9]+))/$', hello.views.phase_view, name='phase_view'),
]
