from .ali_cms import AliCms
from .baidu_bcm import BaiduBcm

__all__ = ["get"]

PLUGINS = dict(
    ali_cms=AliCms,
    baidu_bcm=BaiduBcm
)


def get(plugin_name, plugin_params):
    return PLUGINS[plugin_name](**plugin_params)
