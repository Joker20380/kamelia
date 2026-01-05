from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
                path('', Index.as_view(), name='index'),
                path('contacts/', ContactsView.as_view(), name='contacts'),
                path('blog/', Blog.as_view(), name='blog'),
                path('news/<slug:news_slug>/', ShowNews.as_view(), name='news'),
                path('conf/', Conf.as_view(), name='conf'),
                path("rooms/", RoomListView.as_view(), name="rooms"),
                path("booking/success/", booking_success_view, name="booking_success"),
                path("rooms/<slug:room_slug>/", RoomDetailView.as_view(), name="room"),
                path("rooms/category/<slug:category_slug>/", RoomCategoryView.as_view(), name="room_category"),
                path("availability/", availability_view, name="availability"),
                path("booking/<slug:room_slug>/", booking_create_view, name="booking_create"),

               
               ]
