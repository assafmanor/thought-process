CLI
===

The CLI consumes the API and reflects it.

.. code-block:: bash

    $ python -m thoughtprocess.cli get-users
    …


.. code-block:: bash

    $ python -m thoughtprocess.cli get-user 1
    …


.. code-block:: bash

    $ python -m thoughtprocess.cli get-snapshots 1
    …

.. code-block:: bash

    $ python -m thoughtprocess.cli get-snapshot 1 2
    …


.. code-block:: bash

    $ python -m thoughtprocess.cli get-result 1 2 'pose'
    …


| All commands accept the -h/--host and -p/--port flags to configure the host and port, but default to the API's address.
| 
| The get-result command also accepts the -s/--save flag that, if specified, receives a path, and saves the result's data to that path.

