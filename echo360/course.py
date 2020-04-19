import json
import sys
import selenium
import logging

from echo360.videos import EchoVideos

_LOGGER = logging.getLogger(__name__)


class EchoCourse(object):

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
            try:
                course_data_json = self._get_course_data()
                videos_json = course_data_json["section"]["presentations"]["pageContents"]
                self._videos = EchoVideos(videos_json, self._driver)
            except KeyError as e:
                self._blow_up("Unable to parse course videos from JSON (course_data)", e)
            except selenium.common.exceptions.NoSuchElementException as e:
                self._blow_up("selenium cannot find given elements", e)

        return self._videos

    @property
    def uuid(self):
        return self._uuid

    @property
    def hostname(self):
        return self._hostname

    @property
    def url(self):
        return "{}/ess/portal/section/{}".format(self._hostname, self._uuid)

    @property
    def video_url(self):
        return "{}/ess/client/api/sections/{}/section-data.json?pageSize=100".format(self._hostname, self._uuid)

    @property
    def course_id(self):
        if self._course_id == "":
            try:
                # driver = webdriver.PhantomJS() #TODO Redo this. Maybe use a singleton factory to request the lecho360 driver?s
                self.driver.get(self.url) # Initialize to establish the 'anon' cookie that Echo360 sends.
                self.driver.get(self.video_url)
                course_data_json = self._get_course_data()

                self._course_id = course_data_json["section"]["course"]["identifier"]
                self._course_name = course_data_json["section"]["course"]["name"]
            except KeyError as e:
                self._blow_up("Unable to parse course id (e.g. CS473) from JSON (course_data)", e)

        if type(self._course_id) != str:
            # it's type unicode for python2
            return self._course_id.encode('utf-8')
        return self._course_id

    @property
    def course_name(self):
        if self._course_name == "":
            # trigger getting course_id to get course name as well
            self.course_id
        if type(self._course_name) != str:
            # it's type unicode for python2
            return self._course_name.encode('utf-8')
        return self._course_name

    @property
    def driver(self):
        if self._driver is None:
            self._blow_up("webdriver not set yet!!!", "")
        return self._driver

    def _get_course_data(self):
            try:
                self.driver.get(self.video_url)
                _LOGGER.debug("Dumping course page at %s: %s",
                              self.video_url,
                              self._driver.page_source)
                # self.driver.get_screenshot_as_file('./2.png')
                # print(dir(self.driver))
                # print('ha')
                # print(self.driver.page_source)
                json_str = self.driver.find_element_by_tag_name("pre").text
                print(json_str)

                return json.loads(json_str)
            except ValueError as e:
                self._blow_up("Unable to retrieve JSON (course_data) from url", e)

    def set_driver(self, driver):
        self._driver = driver

    def _blow_up(self, msg, e):
        print(msg)
        print("Exception: {}".format(str(e)))
        sys.exit(1)
