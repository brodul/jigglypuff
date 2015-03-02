This is alfa. :D

Demo can be found here:
`Brodul's jigglypuff <http://jigglypuff.brodul.org/>`_

Make sure you have the packets::

    ffmpeg
    python-virtualenv
    rabbitmq-server
    youtube-dl


You need this in ``/etc/rabbitmq/rabbitmq-env.conf``::

    NODE_IP_ADDRESS='127.0.0.1'
    NODENAME='guest@localhost'


Make a virtualenv in the root of the project::

    virtualenv --no-site-packages .


Activate the virtual env::

    source bin/activate


Install the deps::

    python setup.py install


Run the dev server::

    pserve production.ini


Run the MQ server::

    rabbitmq-server -detached


Run the worker::

    mkdir jigglypuff/media
    celery -A jigglypuff.tasks worker --loglevel=INFO &
