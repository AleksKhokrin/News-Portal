import logging

from django.conf import settings
from decouple import config
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from news.models import Category, Post

logger = logging.getLogger(__name__)



def my_job():
    
    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        week_posts = Post.objects.filter(date_creation > datetime.now() - timedelta(days=7), post_category=category)

        for subscriber in subscribers:
            for week_post in week_posts:
                url += f'{week_post.get_absolute_url}, '
            send_mail(
                'Posts in week!',
                'Посты за неделю: {url}',
                from_email=config('EMAIL_HOST_USER'),
                recipient_list=[subscriber.user.email, ],
            )



def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"),
            
            id="my_job",  
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")