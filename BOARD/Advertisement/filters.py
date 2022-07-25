from django_filters import FilterSet

from .models import Advertisement, Reply


class AdvertisementFilter(FilterSet):
    class Meta:
        model = Advertisement
        fields = ('author', 'category',)


class ReplyFilter(FilterSet):
    class Meta:
        model = Reply
        fields = ('replyAd_id',)
