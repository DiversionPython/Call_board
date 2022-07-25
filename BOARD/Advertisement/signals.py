from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Reply)
def send_msg(instance, created, **kwargs):

    user = User.objects.get(pk=instance.replyUser_id)
    pk_response = instance.id
    if created:
        pk_ad = instance.replyAd_id
        user = f'{user.username}'
        user_id = Advertisement.objects.get(pk=pk_ad).author_id
        ad_title = Advertisement.objects.get(pk=pk_ad).title
        response_text = Reply.objects.get(pk=pk_response).text
        response_time = Reply.objects.get(pk=pk_response).dateCreation

        title = f'Вам пришел новый отклик от {str(user)[:15]}'
        msg = f'На ваше объявление "{ad_title}" пришел {str(response_time)[:19]} новый отклик\n' \
              f'от {user} следующего содержания: ' \
              f'{response_text}. Перейти в отклики http://127.0.0.1:8000/Advertisement/reply/'
        email = settings.DEFAULT_FROM_EMAIL
        ad_email = User.objects.get(pk=user_id).email

        send_mail(subject=title, message=msg, from_email=email, recipient_list=[ad_email, ])

    elif instance.status_add:
        ad_title = Advertisement.objects.get(pk=Reply.objects.get(pk=pk_response).replyAd_id).title
        ad_id = Advertisement.objects.get(pk=Reply.objects.get(pk=pk_response).replyAd_id).id
        reply_time = Reply.objects.get(pk=pk_response).dateCreation

        title = f'У вас одобренный отклик на объявление "{str(ad_title)[:15]}"'
        msg = f'На ваш отклик от {str(reply_time)[:19]} на объявление "{ad_title}" пришло положительное ' \
              f'подтверждение. Перейти на объявление http://127.0.0.1:8000/Advertisement/{ad_id}'
        email = settings.DEFAULT_FROM_EMAIL
        reply_email = User.objects.get(pk=Reply.objects.get(pk=pk_response).replyUser_id).email

        send_mail(subject=title, message=msg, from_email=email, recipient_list=[reply_email, ])