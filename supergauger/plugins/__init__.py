from .ali_cms import AliCms
from .baidu_bcm import BaiduBcm
from .echo import Echo

__all__ = ["get"]

PLUGINS = dict(
    ali_cms=AliCms,
    baidu_bcm=BaiduBcm,
    echo=Echo
)


def get(plugin_name, plugin_params):
    plugin_params = plugin_params or {}
    return PLUGINS[plugin_name](**plugin_params)
