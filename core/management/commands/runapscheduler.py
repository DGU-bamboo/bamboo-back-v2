import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from post.models import Post
from report.models import Report
from django.utils import timezone


logger = logging.getLogger(__name__)


def periodic_nemo():
    queryset = Report.objects.filter(type="NEMO", is_approved=True, post=None)
    content = ""
    priority = 1
    if queryset.exists():
        for q in queryset:
            content += f"({priority})" + q.postify + "\n\n"
            priority += 1
        content += "#니모를찾아서 #동국대학교대나무숲 #동대나무숲"
        title = timezone.now().strftime("%Y-%m-%d %p %I시 %M분") + " 니모"
        post = Post.objects.create(title=title, content=content, type="NEMO")
        queryset.update(post=post)
        logger.info("Periodic_nemo function completed")


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler._logger.setLevel(logging.DEBUG)

        scheduler.add_job(
            periodic_nemo,
            trigger=CronTrigger(hour="12,22", minute="25"),
            id="periodic_nemo",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
