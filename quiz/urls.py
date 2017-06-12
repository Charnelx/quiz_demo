from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from simple_quiz.views import QuizListView, QuizDetailView, CategoriesListView, CategoryDetailView, HomePageView, QuestionView
from authentific.views import user_login, user_register
from .settings import STATIC_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': STATIC_ROOT}),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^login/$',
        view=user_login,
        name='login'),
    url(r'^logout/$',
        view=auth_views.logout,
        name='logout',
        kwargs={'next_page':'/login'}),
    url(r'^register/$',
        view=user_register,
        name='register'),
    url(r'^$',
        view=HomePageView,
        name='home'),
    url(regex=r'^quizzes/$',
        view=QuizListView.as_view(),
        name='quiz_index'),
    url(regex=r'^category/$',
        view=CategoriesListView.as_view(),
        name='category_index'),
    url(regex=r'^category/(?P<slug>[\w-]+)/$',
        view=CategoryDetailView.as_view(),
        name='category_detail'),
    url(r'^quiz/', include([
        url(r'^(?P<slug>[\w-]+)/$', view=QuizDetailView.as_view(), name='quiz_start_page'),
        url(r'^(?P<slug>[\w-]+)/(?P<question>[\w]+)/$', view=QuizDetailView.as_view(), name='question_at_quiz')
        ])),
    url(regex=r'^question/(?P<id>[\w]+)/$',
        view=QuestionView.as_view(),
        name='question')
]
