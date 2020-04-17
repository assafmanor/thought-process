GUI
===

The GUI consumes the API and reflects it.

API and CLI
^^^^^^^^^^^

The GUI is available as thoughtprocess.gui and exposes the following API:

    >>> from thoughtprocess.gui import run_server
    >>> run_server(
    ...     host = '127.0.0.1',
    ...     port = 8080,
    ...     api_host = '127.0.0.1',
    ...     api_port = 5000,
    ... )

and the following CLI command:

.. code-block:: bash

    $ python -m thoughtprocess.gui run-server  \
        -h/--host '127.0.0.1'                  \
        -p/--port 8080                         \
        -H/--api-host '127.0.0.1'              \
        -P/--api-port 5000

