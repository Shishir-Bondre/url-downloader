import asyncio
import logging
import os
from zipfile import ZipFile

import aiohttp

logger = logging.getLogger(__name__)


async def get_zip_files(loop, urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(download_url(session=session, url=url))  # Creates a new thread for each url
        result = await asyncio.gather(*tasks)
    return result


async def download_url(session, url):
    try:
        # We want to get wait only for 60 secs
        async with session.get(url, timeout=60) as response:
            response.raise_for_status()
            file_contents = await response.text()
            host = response.host
            html_file = _create_html_file(file_name=host, file_contents=file_contents)
            zip_file = _create_zip_file(file_name=host, file_to_be_ziped=html_file)
    except Exception as error:
        logger.error(f'[ERROR] while downloading url {error}')
        pass  # Pass onto to next thread
    else:
        return zip_file


def _create_html_file(file_name, file_contents):
    html_file = file_name + '.html'
    with open(html_file, 'w') as html:
        html.write(file_contents)
    return html_file


def _create_zip_file(file_name, file_to_be_ziped):
    zip_file = file_name + '.zip'

    with ZipFile(zip_file, 'w') as zfile:
        zfile.write(file_to_be_ziped)
        os.remove(file_to_be_ziped)  # Trying to free up the space
    return zip_file
