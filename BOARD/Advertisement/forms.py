from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import *

from .models import *


class AdvertisementUpdateForm(ModelForm):
    exclude = ['author']

    class Meta:
        model = Advertisement
        fields = ('category', 'title', 'media')


class AdvertisementCreateForm(ModelForm):

    category = 'category'
    title = CharField(label='title', widget=TextInput(attrs={'class': 'form-control'}))
    media = CharField(label='media', widget=CKEditorUploadingWidget(attrs={'class': 'form-control'}))

    class Meta:
        model = Advertisement
        fields = ('category', 'title', 'text', 'media')


class ReplyForm(ModelForm):

    class Meta:
        model = Reply
        fields = ('text', )
        widgets = {'text': TextInput(attrs={'size': 50, 'placeholder': 'Введите комментарий'})}