from ape import plugins

from .config import KongConfig


@plugins.register(plugins.Config)
def config_class():
    return KongConfig
