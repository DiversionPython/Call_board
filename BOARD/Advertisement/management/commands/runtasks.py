import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
# from BOARD.models import *

from BOARD.Advertisement.models import *

logger = logging.getLogger(__name__)


def sender():

    ads = []
    week_number_last = datetime.now().isocalendar()[1] - 1
    for ad in Advertisement.objects.filter(dateCreation__week=week_number_last).values('pk',
                                                                            'title',
                                                                            'media',
                                                                            'dateCreation',
                                                                            ):
        ads.append(ad)

    if ads:
        mail_list = list(User.objects.all().values('username','email'))

        for mail in mail_list:
            html_content = render_to_string(
                'sender.html',
                {'data': ads,
                 'user': mail['username'],
                 'week_number_last': week_number_last,
                 }
            )
            msg = EmailMultiAlternatives(
                subject=f'Здравствуйте, уважаемый {mail["username"]}. Ознакомтесь с новыми объявлениями!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[mail['email']],
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Старт apscheduler"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            sender,
            # отправляем письма в понедельник в 8 утра
            trigger=CronTrigger(
                day_of_week="mon", hour="08", minute="00"
            ),
            id="sender",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена работка 'sender'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить,
            # либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Задачник запущен")
            print('Задачник запущен')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Задачник остановлен...")
            scheduler.shutdown()
            print('Задачник остановлен')
            logger.info("Задачник остановлен успешно!")