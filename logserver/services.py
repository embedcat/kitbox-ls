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


def create_log_file(id: int) -> None:
    path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR, str(id))
    file = os.path.join(path, f"log_{datetime.today().strftime('%Y-%m-%d-%H%M%S')}.log-----")
    with open(file, 'wb'):
        pass
    logger.info(f"[SERVICES] create_log_file(id={id}). File={file}")


def get_current_log_file(id: int) -> str:
    path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR, str(id))
    try:
        files = [f.path for f in os.scandir(path) if not f.is_dir()]
        files.sort(key=os.path.getctime)
        return files[-1]
    except FileNotFoundError as e:
        logger.error(f"[SERVICES] append_log() exception: {e}")
        return ""


def append_log(id: int, file_obj) -> bool:
    file = get_current_log_file(id=id)
    if file == "":
        return False
    logger.info(f"[SERVICES] append_log({id},{file_obj}) into {file}")
    with open(file, 'ab') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
    return True


def finalize_log(id: int):
    file = get_current_log_file(id=id)
    os.rename(file, file[:-5])


def get_id_dirs(id=None) -> list:
    if id is None:
        path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR)
    else:
        path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR, str(id))
    list_subfolders_with_paths = [os.path.split(f.path)[-1] for f in os.scandir(path)]
    return list_subfolders_with_paths


def get_list_of_logs(id:int) -> list:
    path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR, str(id))
    files = [f for f in os.scandir(path) if not f.is_dir()]
    files.sort(key=os.path.getctime, reverse=True)
    return [{"name": f.name, "size": os.stat(f).st_size} for f in files]


def download_file_response(id:int, file:str) -> HttpResponse:
    path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR, str(id), str(file))
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response


def _create_dir(dir: str) -> None:
    if not os.path.exists(dir):
        os.mkdir(dir)
        logger.info(f"[SERVICES] _create_dir({dir})")
