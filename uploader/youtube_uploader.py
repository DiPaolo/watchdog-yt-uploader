import os
import pprint
import queue
import random
import shutil
import threading
import time
from dataclasses import dataclass

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from PySide6 import QtCore
from PySide6.QtCore import Signal
from googleapiclient.http import MediaFileUpload
import google.oauth2.credentials

import config
import logger

scopes = ["https://www.googleapis.com/auth/youtube.upload"]
user_cred_json = 'qqqwtf.json'


@dataclass
class MediaFile:
    uuid: str
    filename: str
    title: str
    description: str

@dataclass
class UploadedFileInfo:
    uuid: str
    err_msg: str
    uploaded_url: str


class YouTubeUploader(QtCore.QObject):
    fileUploaded = Signal(UploadedFileInfo)

    def __init__(self):
        super().__init__()
        self.q = queue.Queue()
        self.worker = None

    def __del__(self):
        if self.worker:
            self.worker.stop()

    def start(self):
        if self.worker:
            self.stop()

        self.worker = Worker(self.q)
        self.worker.fileUploaded.connect(self.fileUploaded)
        self.worker.start()

    def stop(self):
        if self.worker:
            self.worker.stop()
            self.worker = None

    def queue_media_file(self, media: MediaFile):
        logger.debug(f'queued new media file. Queue has approx. {self.q.qsize()} items now')
        self.q.put(media)


class Worker(QtCore.QThread):
    fileUploaded = Signal(UploadedFileInfo)

    def __init__(self, q, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_stopped = True
        self.q = q

    def run(self):
        logger.debug('start worker')
        self.is_stopped = False
        while not self.is_stopped:
            item = None
            try:
                item = self.q.get(timeout=1)
            except queue.Empty:
                pass

            if item:
                logger.debug(f'process item (UUID={item.uuid}) from queue. Queue has approx. {self.q.qsize()} items left')
                if config.DEBUG:
                    err_msg = _upload_media_file_mock(item.filename, item.title, item.description)
                else:
                    err_msg = _upload_media_file(item.filename, item.title, item.description)

                if err_msg == '':
                    self.fileUploaded.emit(UploadedFileInfo(
                        item.uuid,
                        err_msg,
                        ''))

                self.q.task_done()
            else:
                time.sleep(1)

        logger.debug('exiting working thread')

    def stop(self):
        logger.debug('stop worker. waiting...')
        self.is_stopped = True
        self.wait(10 * 1000)
        logger.debug('stopped')


def _upload_media_file(filename: str, title: str, description: str) -> str:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "/Users/dipaolo/Downloads/client_secret_448446771119-fljo991dmq35ge7qk0ohchpqdl8acqeu.apps.googleusercontent.com.json"
    # "/Users/dipaolo/repos/watchdog-yt-uploader/client_secret_148455518759-u47f4culv97siandr4da4mg1vupghiuq.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    if not os.path.exists(user_cred_json):
        credentials = flow.run_local_server()
        logger.info('Got new credentials')
        pprint.pprint(credentials)

        with open(user_cred_json, 'wt+') as f:
            f.write(credentials.to_json())
    else:
        logger.info('Use previously saved credentials')
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(user_cred_json)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        body=dict(
            snippet=dict(
                title=title,
                description=description,
                # "tags": ["surfing", "Santa Cruz"],
                # categoryId="22",
            ),
            status=dict(
                privacyStatus="private"
            )
        ),

        # statistics,contentDetails,fileDetails,processingDetails,suggestions
        part="snippet,status",
        media_body=MediaFileUpload(filename)
    )

    logger.debug('Sending request...')
    try:
        response = request.execute()
        logger.debug('Got the response:')
        logger.debug(response)
    except googleapiclient.errors.HttpError as e:
        err_msg = f'failed to upload video. Reason: {e.reason}'
        logger.error(err_msg)
        return err_msg

    return ''


def _upload_media_file_mock(filename: str, title: str, description: str) -> str:
    duration_sec = random.randrange(3, 10)
    logger.info(f' === Upload {filename} to {config.UPLOADER_MOCK_DIR} in {duration_sec} seconds ===')

    if not os.path.exists(config.UPLOADER_MOCK_DIR):
        os.mkdir(config.UPLOADER_MOCK_DIR)
    shutil.copyfile(filename, os.path.join(config.UPLOADER_MOCK_DIR, os.path.basename(filename)))

    time.sleep(duration_sec)

    return ''
