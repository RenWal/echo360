import json
import sys
import selenium
import logging
import datetime

from echo360.videos import EchoVideos

_LOGGER = logging.getLogger(__name__)


class SingleVidEchoCourse(object):

    def __init__(self, uuid, hostname=None):
        self._course_id = ""
        self._course_name = ""
        self._uuid = uuid
        self._videos = None
        self._driver = None
        if hostname is None:
            self._hostname = "https://view.streaming.sydney.edu.au:8443"
        else:
            self._hostname = hostname

    def get_videos(self):
        if self._driver is None:
            self._blow_up("webdriver not set yet!!!", "")
        if not self._videos:
            videos_json = self._fabricate_json()
            self._videos = EchoVideos(videos_json, self._driver)

        return self._videos

    @property
    def uuid(self):
        return self._uuid

    @property
    def hostname(self):
        return self._hostname

    @property
    def driver(self):
        if self._driver is None:
            self._blow_up("webdriver not set yet!!!", "")
        return self._driver

    @property
    def course_id(self):
        return "SINGLE"

    @property
    def course_name(self):
        return "single video"

    @property
    def url(self):
        return self._hostname + "/ess/echo/presentation/" + self._uuid

    # evil hack to make the video parser think we had the course data
    def _fabricate_json(self):
        title = "No title available"
        start_time = str(datetime.datetime.now())
        return [{"title":title, "startTime":start_time, "richMedia":self.url}]

    def set_driver(self, driver):
        self._driver = driver

    def _blow_up(self, msg, e):
        print(msg)
        print("Exception: {}".format(str(e)))
        sys.exit(1)
