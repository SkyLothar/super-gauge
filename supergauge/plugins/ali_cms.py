from collections import defaultdict
import json
import logging

import requests

from ..unit import unit

logger = logging.getLogger(__name__)


class AliCms(object):
    URL = "http://open.cms.aliyun.com/metrics/put"
    UNITS = defaultdict(lambda: "None")
    UNITS.update({
        unit.percent: "Percent",
        unit.sec: "Seconds",
        unit.ms: "Microseconds",
        unit.millsec: "Milliseconds",
        unit.byte: "Bytes",
        unit.kb: "Kilobytes",
        unit.mb: "Megabytes",
        unit.gb: "Gigabytes",
        unit.tb: "Terabytes",
        unit.count: "Count",
        unit.bps: "Bytes/Second",
        unit.cps: "Count/Second"
    })

    def __init__(self, user_id):
        self._session = requests.session()
        self.user_id = user_id

    @property
    def session(self):
        return self._session

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, new_user_id):
        assert new_user_id is not None
        self._user_id = str(new_user_id)
        return self._user_id

    @property
    def namespace(self):
        return "acs/custom/{0}".format(self.user_id),

    def get_dimensions(self, raw_dimensions):
        return raw_dimensions

    def get_metrics(self, timestamp, raw_metrics, raw_dimensions):
        dimensions = self.get_dimensions(raw_dimensions)
        metrics = [
            dict(
                metricName=key,
                value=val,
                unit=self.UNITS[unit],
                timestamp=timestamp,
                dimensions=dimensions
            )
            for key, val, unit in raw_metrics
        ]
        return json.dumps(metrics)

    def send(self, localtime, raw_metrics, raw_dimensions):
        timestamp = int(localtime * 1000)
        metrics = self.get_metrics(timestamp, raw_metrics, raw_dimensions)
        res = self.session.post(
            self.URL,
            data=dict(
                userId=self.user_id,
                namespace=self.namespace,
                metrics=metrics,
            )
        )
        if res.ok:
            return True
        else:
            logger.error("send metrics to ali error: {0}".format(
                json.loads(res.json()["msg"])["message"]
            ))
            return False
