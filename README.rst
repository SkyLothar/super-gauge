Supervisor Gague Event Listeners
=================================

Version
-------
v0.0.2

Supported Backend
-----------------
* Ali CMS
* Baidu BCM

How to Use
----------
create a config file

.. code-block:: yaml

    docker:
        version: auto

    supervisor:
        SUPERVISOR_SERVER_URL: http://localhost:9000/RPC2
        # SUPERVISOR_USERNAME: chulai-usr
        # SUPERVISOR_PASSWORD: chulai-pwd

    plugins:
        # echo: {}
        # ali_cms:
        #   user_id: ALI-USER-ID
        # baidu_bcm:
        #   access_key: BCE_ACCESS-KEY
        #   secret_key: BCE-SECRET-KEY
        #   user_id: BCE-USER-ID
        #   scope: BCM-SCOPE

    logging:
      version: 1
      loggers:
          supergauge.eventlistener:
              handlers: [file]
              level: DEBUG
          __main__:
              handlers: [file]
              level: INFO
      handlers:
        file:
          class : logging.handlers.RotatingFileHandler
          level: DEBUG
          formatter: precise
          filename: log/gauge.log
          maxBytes: 1024
          backupCount: 3
      formatters:
        precise:
          class: logging.Formatter
          format: "%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s"


put following snippet in your supervisor config file

.. code-block:: ini

    [eventlistener:supergauge]
    command=supergauge /path/to/config/file
    events=TICK_60 ; collect every 60s [TICK_5, TICK_60, TICK_3600]
    user=username ; if you have your permission screwed up, use root


How to Install
--------------
pip install supergauge --process-dependency-links
