from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', AdvertisementList.as_view(), name='ad_list'),
    path('<int:pk>', AdvertisementDetail.as_view(), name='one_ad'),
    path('reply/', ReplyList.as_view(), name='reply'),
    path('create/', AdvertisementCreate.as_view(), name='ad_create'),
    path('update/<int:pk>', AdvertisementUpdate.as_view(), name='ad_update'),
    path('search/', AdvertisementSearch.as_view(), name='ad_search'),
    path('reply_accept/<int:pk>', ReplyAccept.as_view(), name='accept'),
    path('reply_remove/<int:pk>', ReplyRemove.as_view(), name='remove'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)