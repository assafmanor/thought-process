Client
======

API and CLI
^^^^^^^^^^^

The client is available as thoughtprocess.client and exposes the following API:

    >>> from thoughtprocess.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    … # upload path to host:port

And the following CLI:

.. code-block:: bash

    $ python -m thoughtprocess.client upload-sample \
        -h/--host '127.0.0.1'             \
        -p/--port 8000                    \
        'snapshot.mind.gz'
    …


The Sample
^^^^^^^^^^

| The format of the sample is a gzipped binary with a sequence of message sizes (uint32) and messages.
| 
| First, we have a single User message, and then as many Snapshot messages as necessary.\
| 
| The user and snapshot messages are defined in `this .proto file <https://storage.googleapis.com/advanced-system-design/cortex.proto>`_.
| 
| An example sample is available `here <https://storage.googleapis.com/advanced-system-design/sample.mind.gz>`_.
