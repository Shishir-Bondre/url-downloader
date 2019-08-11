import json
import logging

import validators
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UrlSerializer
from .tasks import DownloadUrlTask

logger = logging.getLogger(__name__)


class UrlDownloadView(APIView):
    """
    Takes list of urls and an email id as input. Sends list of urls to an async task
    which downloads each of the url in background. This also validates given data
    and sends the response according
    """

    def post(self, request):
        request_data = json.loads(request.body)
        serializer = UrlSerializer(data=request_data)
        try:
            assert serializer.is_valid(), serializer.errors
            _validate_request_data(urls=serializer.data['urls'], email=serializer.data['email'])
            DownloadUrlTask.delay(urls=serializer.data['urls'], email=serializer.data['email'])
        except Exception as error:
            logger.error(f'[ERROR] {error}')
            return Response(status=400, data={
                'msg': 'Failure',
                'reason': str(error)
            })
        else:
            return Response(status=200, data={
                'msg': 'Success'
            })


def _validate_request_data(urls: list, email: str):
    """
    Uses validator package for validation on url and email
    example: url ['https://www.xyz.com'] and email someone@email.com
    :param urls: list of urls
    :param email: email id
    :return:
    """
    if not validators.email(email):
        raise Exception('INVALID EMAIL ID')

    for url in urls:
        if not validators.url(url):
            raise Exception(f'INVALID URL {url}')
