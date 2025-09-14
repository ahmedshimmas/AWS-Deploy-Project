from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from app import models
from project.settings import EMAIL_HOST_USER


@shared_task
def send_daily_summary():
    users = models.User.objects.filter(is_deleted=False)
    for user in users:
        print(f"Running summary for {user.email}")
        tasks = models.Task.objects.filter(user=user, is_deleted=False)
        print(f"Filtered tasks for {user.email}")
        
        pending_tasks = tasks.filter(status='pending')
        print(f"Calculated pending tasks for {user.email}")
        pending_tasks_count = pending_tasks.count()
        print(f"Calculated pending tasks count for {user.email}")

        completed_tasks = tasks.filter(status='done')
        print(f"Calculated completed tasks for {user.email}")
        completed_tasks_count = completed_tasks.count()
        print(f"Calculated completed tasks count for {user.email}")

        subject = 'Daily Tasks Summary'
        message = """
        Dear {user},

        Here is your daily tasks summary:

        Completed Tasks: {completed_tasks_count}
        Pending Tasks: {pending_tasks_count}


        Thank you for using our services.
        Happy to serve you!


        Regards,
        TickTracker Team
        """.format(
            user = user.first_name,
            completed_tasks_count = completed_tasks_count,
            pending_tasks_count = pending_tasks_count
        )

        print(f"Message formatted for {user.email}")

        if user.email:
            send_mail(
                subject=subject,
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False
            )
            print(f"Email sent for {user.email}")

    return f'Daily Tasks summary sent to {user.first_name} at {timezone.now()}'