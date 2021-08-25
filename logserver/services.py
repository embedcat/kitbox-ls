import logging

from django.http import HttpResponse

from config import settings
from datetime import datetime
import os


logger = logging.getLogger(settings.LOGGER)


def create_logs_dir(id: int) -> None:
    dir = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR)
    _create_dir(dir=dir)
    dir = os.path.join(dir, str(id))
    _create_dir(dir=dir)


def append_log(id: int, file_obj, start_new_file:bool = False) -> bool:
    path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR, str(id))
    try:
        files = [f.path for f in os.scandir(path) if not f.is_dir()]
    except FileNotFoundError as e:
        logger.error(f"[SERVICES] append_log() exception: {e}")
        return False
    file = files[-1] if len(files) > 0 and start_new_file is False else os.path.join(path, f"log_{datetime.today().strftime('%Y-%m-%d-%H%M%S')}.log")
    logger.info(f"[SERVICES] append_log({id},{file_obj},{start_new_file}) into {file}")
    with open(file, 'ab') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
    return True


def get_id_dirs(id=None) -> list:
    if id is None:
        path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR)
    else:
        path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR, str(id))
    list_subfolders_with_paths = [os.path.split(f.path)[-1] for f in os.scandir(path)]
    return list_subfolders_with_paths


def download_file_response(id:int, file:str) -> HttpResponse:
    path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR, str(id), str(file))
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response


def _create_dir(dir: str) -> None:
    if not os.path.exists(dir):
        os.mkdir(dir)
        logger.info(f"[SERVICES] _create_dir({dir})")
