Supervisor Gague Event Listeners
=================================

Version
-------
v0.0.1

Supported Backend
-----------------
* Ali CMS
* Baidu BCM(WIP)

How to Use
----------
put following snippet in your supervisor config file
.. code:block:: ini

    [eventlistener:supergauge]
    command=supergauge
    events=TICK_60 ; collect every 60s [TICK_5, TICK_3600]
    user=username ; if you have your permission screwed up, use root


How to Install
--------------
pip install supergauge --process-dependency-links
