from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
                path('', Index.as_view(), name='index'),
                path('contacts/', ContactsView.as_view(), name='contacts'),
                path('blog/', Blog.as_view(), name='blog'),
                path('news/<slug:news_slug>/', ShowNews.as_view(), name='news'),
                path('conf/', Conf.as_view(), name='conf'),
                

                
              ]