from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models



class Advertisement(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    CATEGORY_CLASSES = (
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('damagers', 'ДД'),
        ('merchants', 'Торговцы'),
        ('guildmasters', 'Гилдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potionmakers', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний')
    )
    category = models.CharField(max_length=12, choices=CATEGORY_CLASSES, default='tanks')
    title = models.CharField(max_length=64)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    media = RichTextUploadingField(blank=True, null=True)
    def __str__(self):
        return f'{self.author}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/Advertisement/{self.id}'

    class Meta:
        ordering = ('-dateCreation',)
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'


class Reply(models.Model):
    replyAd = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    replyUser = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Date Creation')
    text = models.TextField(verbose_name='Text')
    status_remove = models.BooleanField(default=False, verbose_name='Отклик - отклонен')
    status_add = models.BooleanField(default=False, verbose_name='Отклик - принят')

    class Meta:
        ordering = ('-dateCreation',)
        verbose_name = 'Reply'
        verbose_name_plural = 'Replys'

