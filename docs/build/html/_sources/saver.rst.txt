Saver
=====

The saver is available as thoughtprocess.saver and exposes the following API:

    >>> from thoughtprocess.saver import Saver
    >>> saver = Saver(database_url)
    >>> data = …
    >>> saver.save('pose', data)

| Which connects to a database, accepts a topic name and some data, as consumed from the message queue, and saves it to the database.


| It also provides the following CLI:

.. code-block:: bash

    $ python -m thoughtprocess.saver save             \
        -d/--database 'postgresql://127.0.0.1:5432'   \
        'pose'                                        \
        'pose.result' 

| Which accepts a topic name and a path to some raw data, as consumed from the message queue, and saves it to a database.
| This way of invocation runs the saver exactly once.

| The CLI also supports running the saver as a service, which works with a message queue indefinitely; it is then the saver's responsibility to subscribe to all the relevant topics it is capable of consuming and saving to the database.

.. code-block:: bash

    $ python -m thoughtprocess.saver run-saver  \
        'postgresql://127.0.0.1:5432'           \
        'rabbitmq://127.0.0.1:5672/'
