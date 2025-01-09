import logging
from urllib.parse import urlparse

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from instagrapicustom.mixins.account import AccountMixin
from instagrapicustom.mixins.album import DownloadAlbumMixin, UploadAlbumMixin
from instagrapicustom.mixins.auth import LoginMixin
from instagrapicustom.mixins.bloks import BloksMixin
from instagrapicustom.mixins.challenge import ChallengeResolveMixin
from instagrapicustom.mixins.clip import DownloadClipMixin, UploadClipMixin
from instagrapicustom.mixins.collection import CollectionMixin
from instagrapicustom.mixins.comment import CommentMixin
from instagrapicustom.mixins.direct import DirectMixin
from instagrapicustom.mixins.explore import ExploreMixin
from instagrapicustom.mixins.fbsearch import FbSearchMixin
from instagrapicustom.mixins.fundraiser import FundraiserMixin
from instagrapicustom.mixins.hashtag import HashtagMixin
from instagrapicustom.mixins.highlight import HighlightMixin
from instagrapicustom.mixins.igtv import DownloadIGTVMixin, UploadIGTVMixin
from instagrapicustom.mixins.insights import InsightsMixin
from instagrapicustom.mixins.location import LocationMixin
from instagrapicustom.mixins.media import MediaMixin
from instagrapicustom.mixins.multiple_accounts import MultipleAccountsMixin
from instagrapicustom.mixins.note import NoteMixin
from instagrapicustom.mixins.notification import NotificationMixin
from instagrapicustom.mixins.password import PasswordMixin
from instagrapicustom.mixins.photo import DownloadPhotoMixin, UploadPhotoMixin
from instagrapicustom.mixins.private import PrivateRequestMixin
from instagrapicustom.mixins.public import (
    ProfilePublicMixin,
    PublicRequestMixin,
    TopSearchesPublicMixin,
)
from instagrapicustom.mixins.share import ShareMixin
from instagrapicustom.mixins.signup import SignUpMixin
from instagrapicustom.mixins.story import StoryMixin
from instagrapicustom.mixins.timeline import ReelsMixin
from instagrapicustom.mixins.totp import TOTPMixin
from instagrapicustom.mixins.track import TrackMixin
from instagrapicustom.mixins.user import UserMixin
from instagrapicustom.mixins.video import DownloadVideoMixin, UploadVideoMixin

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Used as fallback logger if another is not provided.
DEFAULT_LOGGER = logging.getLogger("instagrapi")


class Client(
    PublicRequestMixin,
    ChallengeResolveMixin,
    PrivateRequestMixin,
    TopSearchesPublicMixin,
    ProfilePublicMixin,
    LoginMixin,
    ShareMixin,
    TrackMixin,
    FbSearchMixin,
    HighlightMixin,
    DownloadPhotoMixin,
    UploadPhotoMixin,
    DownloadVideoMixin,
    UploadVideoMixin,
    DownloadAlbumMixin,
    NotificationMixin,
    UploadAlbumMixin,
    DownloadIGTVMixin,
    UploadIGTVMixin,
    MediaMixin,
    UserMixin,
    InsightsMixin,
    CollectionMixin,
    AccountMixin,
    DirectMixin,
    LocationMixin,
    HashtagMixin,
    CommentMixin,
    StoryMixin,
    PasswordMixin,
    SignUpMixin,
    DownloadClipMixin,
    UploadClipMixin,
    ReelsMixin,
    ExploreMixin,
    BloksMixin,
    TOTPMixin,
    MultipleAccountsMixin,
    NoteMixin,
    FundraiserMixin,
):
    proxy = None

    def __init__(
        self,
        settings: dict = {},
        proxy: str = None,
        delay_range: list = None,
        logger=DEFAULT_LOGGER,
        **kwargs,
    ):

        super().__init__(**kwargs)

        self.settings = settings
        self.logger = logger
        self.delay_range = delay_range

        self.set_proxy(proxy)

        self.init()

    def set_proxy(self, dsn: str):
        if dsn:
            assert isinstance(
                dsn, str
            ), f'Proxy must been string (URL), but now "{dsn}" ({type(dsn)})'
            self.proxy = dsn
            proxy_href = "{scheme}{href}".format(
                scheme="http://" if not urlparse(self.proxy).scheme else "",
                href=self.proxy,
            )
            self.public.proxies = self.private.proxies = {
                "http": proxy_href,
                "https": proxy_href,
            }
            return True
        self.public.proxies = self.private.proxies = {}
        return False
