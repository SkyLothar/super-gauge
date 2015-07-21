import logging
import time

import requests
import bceauth

logger = logging.getLogger(__name__)


class BaiduBcm(object):
    URL_FMT = "http://bcm.bj.baidubce.com/json-api/v1/metricdata/{0}/{1}"
    TIME_FMT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, access_key, secret_key, user_id, scope):
        self._user_id = user_id
        self._url = self.URL_FMT.format(user_id, scope)
        self._session = requests.session()
        self._session.auth = bceauth.AuthV1(access_key, secret_key)

    @property
    def session(self):
        return self._session

    @property
    def url(self):
        return self._url

    def get_dimensions(self, raw_dimensions):
        return [
            dict(name=key, value=val)
            for key, val in raw_dimensions.items()
        ]

    def get_metrics(self, timestamp, raw_metrics, raw_dimensions):
        dimensions = self.get_dimensions(raw_dimensions)
        metrics = [
            dict(
                metricName=key,
                value=val,
                timestamp=timestamp,
                dimensions=dimensions
            )
            for key, val, __ in raw_metrics
        ]
        return dict(metricData=metrics)

    def send(self, localtime, raw_metrics, raw_dimensions):
        gmt = time.gmtime(localtime)
        timestamp = time.strftime(self.TIME_FMT, gmt)

        metrics = self.get_metrics(timestamp, raw_metrics, raw_dimensions)
        res = self.session.post(
            self.url,
            json=metrics
        )
        if res.ok:
            return True
        else:
            logger.error("send metrics to baidu error: {0}".format(
                res.text
            ))
            return False
