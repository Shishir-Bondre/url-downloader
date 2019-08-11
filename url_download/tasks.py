from __future__ import absolute_import, unicode_literals

import asyncio
import logging
import os
from contextlib import closing

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

from .client import get_zip_files
from .email import email_body, email_subject

logger = logging.getLogger(__name__)


@shared_task
def DownloadUrlTask(urls: list, email: str):
    """
    An asynchronous task using celery. This will take list of urls and
    then fire parallel task (using threading via asyncio package). After downloading
    it call SendEmailTask
    :param urls: ['https://xyz.com']
    :param email: someone@email.com
    :return:
    """
    with closing(asyncio.new_event_loop()) as loop:
        # Processing the urls concurrently
        zip_files = loop.run_until_complete(get_zip_files(loop=loop, urls=urls))
    logger.info(f'[INFO] Downloaded urls successfully and zip files are as  {zip_files}')
    SendEmailTask.delay(email=[email], files=zip_files)


@shared_task
def SendEmailTask(to_email: list, files: list):
    """
    Celery task for sending email. uses default django mailer
    Please do configure email settings in settings.py file
    :param to_email: to email
    :param files: path of files to be send as an attachment
    :return:
    """
    email = EmailMessage(subject=email_subject(),
                         body=email_body(),
                         from_email=settings.EMAIL_HOST_USER,
                         to=to_email)
    for file in files:
        if file:
            email.attach_file(path=file)
            os.remove(file)
    logger.info(f'[INFO] Sending email to {to_email}')
    email.send()
    logger.info(f'[INFO] Email has been successfully send')
