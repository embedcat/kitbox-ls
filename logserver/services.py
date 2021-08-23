from django.http import HttpResponse

from config import settings
from datetime import datetime
import os


def create_logs_dir(id: int) -> None:
    dir = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR)
    _create_dir(dir=dir)
    dir = os.path.join(dir, str(id))
    _create_dir(dir=dir)


def append_log(id: int, data, start_new_file:bool = False) -> None:
    path = os.path.join(os.getcwd(), settings.KITBOX_LOGS_DIR, str(id))
    files = [f.path for f in os.scandir(path) if not f.is_dir()]
    file = files[-1] if len(files) > 0 and start_new_file is False else os.path.join(path, f"log_{datetime.today().strftime('%Y-%m-%d-%H%M%S')}.log")
    print(file)
    with open(file, 'a') as f:
        f.write(data)


def get_id_dirs(id=None) -> list[str]:
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
    print(dir)
    if not os.path.exists(dir):
        os.mkdir(dir)
