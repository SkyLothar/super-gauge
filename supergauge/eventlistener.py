import os
import time
import logging


import click
import supervisor.childutils
import yaml

from .gauge import Gauge
from . import consts
from . import plugins


class SuperGauge(object):
    def __init__(self, config):
        self._supervisor = None
        self._plugins = []

        self.plugins = config["plugins"]
        self.supervisor = config["supervisor"]
        self._gauge = Gauge(self.supervisor, config)

    @property
    def supervisor(self):
        return self._supervisor

    @supervisor.setter
    def supervisor(self, config):
        config.update({
            key: val
            for key, val in os.environ.items()
            if key.startswith("SUPERVISOR_")
        })
        rpc = supervisor.childutils.getRPCInterface(config)
        rpc.supervisor.getState()
        state = rpc.supervisor.getState().get("statename")
        if state != consts.RUNNING:
            raise ValueError("can not talk to supervisor server")
        self._supervisor = rpc.supervisor
        return self._supervisor

    @property
    def gauge(self):
        return self._gauge

    @property
    def plugins(self):
        return self._plugins[:]

    @plugins.setter
    def plugins(self, config):
        for plugin_name, plugin_params in config.items():
            self._plugins.append(plugins.get(plugin_name, plugin_params))
        return self._plugins[:]

    @property
    def procs(self):
        return [
            proc["name"]
            for proc in self.supervisor.getAllProcessInfo()
            if proc["statename"] == consts.RUNNING
        ]

    def is_subscribed(self, event):
        return event.startswith("TICK_")

    def run(self):
        localtime = time.time()
        collected = [
            (
                self.gauge.get_metrics(proc_name),
                self.gauge.get_dimensions(proc_name)
            )
            for proc_name in self.procs
        ]

        failed = [
            plugin
            for plugin in self.plugins
            for data in collected
            if plugin.send(localtime, *data) is not True
        ]
        return failed


@click.command()
@click.argument("config_yml", type=click.File("rb"))
def runforever(config_yml):
    config = yaml.load(config_yml)
    logger = logging.getLogger(__name__)
    # TODO: set logging level and outputs

    sg = SuperGauge(config)

    while True:
        headers, payload = supervisor.childutils.listener.wait()

        if not sg.is_subscribed(headers["eventname"]):
            supervisor.childutils.listener.ok()
            return False

        failed = sg.run()
        if failed:
            logger.error(
                "failed to send metric to following plugins: {0}".format(
                    failed
                )
            )
