import os

import docker
import psutil
import supervisor.childutils

from . import consts
from . import utils
from . import plugins
from .unit import unit


class Gauger(object):
    METRICS = dict(
        mem_rss=(lambda proc: utils.to_mb(proc.memory_info().rss), unit.mb),
        mem_vms=(lambda proc: utils.to_mb(proc.memory_info().vms), unit.mb),
        threads=(lambda proc: len(proc.threads()), unit.count),
        open_fds=(lambda proc: proc.num_fds(), unit.count),
        connections=(lambda proc: len(proc.connections()), unit.count)
    )

    def __init__(self, config):
        self._docker = None
        self._supervisor = None
        self._plugins = []

        self.docker = config["docker"]
        self.supervisor = config["supervisor"]
        self.plugins = config["plugins"]

    @property
    def plugins(self):
        return self._plugins[:]

    @plugins.setter
    def plugins(self, config):
        for plugin_name, plugin_params in config.items():
            self._plugins.append(plugins.get(plugin_name, plugin_params))
        return self._plugins[:]

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
        if state != "RUNNING":
            raise ValueError("can not talk to supervisor server")
        self._supervisor = rpc.supervisor

    @property
    def docker(self):
        return self._docker_client

    @docker.setter
    def docker(self, config):
        client = docker.Client(**config)
        if client.ping():
            self._docker_client = client
        else:
            raise ValueError("can not talk to docker server")

    def get_proc(self, proc_name):
        proc_info = self.supervisor.getProcessInfo(proc_name)
        if proc_info["state"] not in consts.SUPERVISOR_RUNNING:
            return None

        proc = psutil.Process(proc_info["pid"])
        if proc.name() == "docker":
            pid = self._get_container_pid(proc_name)
            if pid is None:
                return None
            else:
                proc = psutil.Process(pid)
        return proc

    def get_metric(self, proc_name):
        proc = self.get_proc(proc_name)
        if proc is None:
            return None
        all_procs = self._get_all_procs(proc)
        metrics = self._merge_metrics(all_procs)
        return metrics

    def get_dimensions(self, proc_name):
        return dict(
            hostname=consts.HOSTNAME,
            app=proc_name
        )

    def _get_all_procs(self, children, all_procs=None):
        if not isinstance(children, (list, tuple)):
            children = [children]

        if not children:
            return all_procs

        all_procs = all_procs or []
        new_children = []

        for proc in children:
            all_procs.append(proc)
            new_children += proc.children()

        return self._get_all_procs(new_children, all_procs)

    def _get_container_pid(self, label):
        containers = self.docker.containers(
            all=True,
            filters=dict(label=label)
        )
        if len(containers) != 1:
            raise ValueError

        cid = containers.pop()["Id"]
        info = self.docker.inspect_container(cid)

        if info["State"]["Running"]:
            pid = info["State"]["Pid"]
        else:
            pid = None

        return pid

    def _merge_metrics(self, procs):
        merged_metrics = {
            key: 0
            for key in self.METRICS.keys()
        }

        for proc in procs:
            for key, (func, __) in self.METRICS.items():
                merged_metrics[key] += func(proc)

        metrics = [
            (name, val, self.METRICS[name][1])  # 0=func, 1=unit
            for name, val in merged_metrics.items()
        ]
        metrics.append(("children", len(procs), unit.count))
        return metrics
