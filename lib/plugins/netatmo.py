# -*- coding: utf-8 -*-
"""
Netatmo Weather
Fetch current weather from your netatmo device
"""
from sys import version_info
import os, time
from lib import PLUGINDIR, log, utils
from lib.decorators import never_raise, threaded_method
from lib.exceptions import ValidationError
from lib.plugin import BasePlugin, BaseConfig
from lib.filters import register_filter


NAME = 'Netatmo Devices'
_BASE_URL = "https://api.netatmo.com/"
_AUTH_REQ = _BASE_URL + "oauth2/token"
_GET_MEASURE_REQ = _BASE_URL + "api/getmeasure"
_GET_STATIONDATA_REQ = _BASE_URL + "api/getstationsdata"
_GET_HOME_DATA_REQ = _BASE_URL + "api/gethomedata"
_GET_CAMERA_PICTURE_REQ = _BASE_URL + "api/getcamerapicture"
_GET_EVENTS_UNTIL_REQ = _BASE_URL + "api/geteventsuntil"


class Plugin(BasePlugin):
    DEFAULT_INTERVAL = 600
    LAYOUTS = ['netatmo_main', 'netatmo_station1_modules', 'netatmo_station2_modules']

    @threaded_method
    def enable(self):
        client_id = self.pi_dash.config.get(self.namespace, 'client_id')
        client_secret = self.pi_dash.config.get(self.namespace, 'client_secret')
        username = self.pi_dash.config.get(self.namespace, 'username')
        password = self.pi_dash.config.get(self.namespace, 'password')
        if not client_id:
            log.warning('Netatmo API key (client_id) not specified.')
            return self.disable()
        if not client_secret:
            log.warning('Netatmo client secret not specified.')
            return self.disable()
        if not username:
            log.warning('Netatmo username not specified.')
            return self.disable()
        if not password:
            log.warning('Netatmo password not specified.')
            return self.disable()
        try:
            client_auth = ClientAuth(client_id, client_secret, username, password)
            client_auth.access_token
            self.client_auth = client_auth
        except Exception as ex:
            self.disable()
            self.enabled = False
            raise ValidationError('Netatmo daemon: cannot retrieve valid authentication token.' + str(ex) +
                                  " python version " + str(version_info.major) + "." + str(version_info.minor))
        super(Plugin, self).enable()

    @never_raise
    def update(self):
        if self.client_auth:
            client_auth = self.client_auth
        else:
            client_auth = ClientAuth(client_id=self.pi_dash.config.get(self.namespace, 'client_id'),
                                     client_secret=self.pi_dash.config.get(self.namespace, 'client_secret'),
                                     username=self.pi_dash.config.get(self.namespace, 'username', from_keyring=True),
                                     password=self.pi_dash.config.get(self.namespace, 'password', from_keyring=True))
        post_params = dict(access_token=client_auth.access_token)
        self.data = utils.post_request(_GET_STATIONDATA_REQ, post_params)
        super(Plugin, self).update()


class Config(BaseConfig):
    TEMPLATE = os.path.join(PLUGINDIR, 'netatmo_config.html')
    FIELDS = utils.Bunch(BaseConfig.FIELDS, client_id={}, client_secret={},
                         username={'save_to_keyring': True},
                         password={'save_to_keyring': True})

    def validate_password(self, field, value):
        if not value:
            return value
        client_auth = ClientAuth(client_id=self.pi_config.get(self.namespace, 'client_id'),
                                 client_secret=self.pi_config.get(self.namespace, 'client_secret'),
                                 username=self.pi_config.get(self.namespace, 'username', from_keyring=True),
                                 password=value)
        try:
            client_auth.access_token
            return value
        except Exception as ex:
            raise ValidationError('Invalid username or password.' + str(ex) +
                                  " python version " + str(version_info.major) + "." + str(version_info.minor))


class ClientAuth:
    """
    Request authentication and keep access token available through token method. Renew it automatically if necessary

    Args:
        client_id (str): Application clientId delivered by Netatmo on dev.netatmo.com
        client_secret (str): Application Secret key delivered by Netatmo on dev.netatmo.com
        username (str)
        password (str)
        scope (Optional[str]): Default value is 'read_station'
            read_station: to retrieve weather station data (Getstationsdata, Getmeasure)
            read_camera: to retrieve Welcome data (Gethomedata, Getcamerapicture)
            access_camera: to access the camera, the videos and the live stream.
            Several value can be used at the same time, ie: 'read_station read_camera'
    """

    def __init__(self, client_id: object, client_secret: object, username: object, password: object, scope: object = "read_station") -> object:
        post_params = {
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
            "password": password,
            "scope": scope
        }

        resp = utils.post_request(_AUTH_REQ, post_params)
        print(resp)
        self._clientId = client_id
        self._clientSecret = client_secret
        self._accessToken = resp['access_token']
        self.refreshToken = resp['refresh_token']
        self._scope = resp['scope']
        self.expiration = int(resp['expire_in'] + time.time())

    @property
    def access_token(self):
        if self.expiration < time.time():  # Token should be renewed
            postParams = {
                "grant_type": "refresh_token",
                "refresh_token": self.refreshToken,
                "client_id": self._clientId,
                "client_secret": self._clientSecret
            }
            resp = utils.post_request(_AUTH_REQ, postParams)
            self._accessToken = resp['access_token']
            self.refreshToken = resp['refresh_token']
            self.expiration = int(resp['expire_in'] + time.time())
        return self._accessToken


@register_filter()
def mod_12(value):
    return utils.to_int(value, 0) % 12

@register_filter()
def to_time_string(value):
    return time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(int(value)))

@register_filter()
def to_epoch(value):
    return int(time.mktime(time.strptime(value, "%Y-%m-%d_%H:%M:%S")))

@register_filter()
def today_stamps():
    today = time.strftime("%Y-%m-%d")
    today = int(time.mktime(time.strptime(today, "%Y-%m-%d")))
    return today, today + 3600 * 24

