Parsers
=======

API and CLI
^^^^^^^^^^^

| The parsers are classes, built on top of a platform using decorators, and easily deployable as microservices consuming raw data from the queue, and producing parsed results to it.

| They are located in thoughtprocess.parsers, and expose the following API:

    >>> from thoughtprocess.parsers import run_parser
    >>> data = … 
    >>> result = run_parser('pose', data)

| Which accepts a parser name and some raw data, as consumed from the message queue, and returns the result, as published to the message queue.


| It should also provide the following CLI:

.. code-block:: bash

    $ python -m thoughtprocess.parsers parse 'pose' 'snapshot.raw' > 'pose.result'


| Which accepts a parser name and a path to some raw data, as consumed from the message queue, and prints the result, as published to the message queue (optionally redirecting it to a file). This way of invocation runs the parser exactly once.


| the CLI also supports running the parser as a service, which works with a message queue indefinitely.

.. code-block:: bash

    $ python -m thoughtprocess.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'


Implemented Parsers
^^^^^^^^^^^^^^^^^^^

**Pose**
  Collects the translation and the rotation of the user's head at a given timestamp, and publishes the result to a dedicated topic.

**Color Image**
  | Collects the color image of what the user was seeing at a given timestamp, and publishes the result to a dedicated topic.
  | *Note*: the data itself is saved to disk, and only the metadata is published.

**Depth Image**
  | Collects the depth image of what the user was seeing at a given timestamp, and publishes the result to a dedicated topic.
  | A depth image is a width × height array of floats, where each float represents how far the nearest surface from the user was, in meters. So, if the user was looking at a chair, the depth of its outline would be its proximity to her (for example, 0.5 for half a meter), and the wall behind it would be farther (for example, 1.0 for one meter).
  | *Note*: the data itself is saved to disk, and only the metadata is published.

**Feelings**
  Collects the feelings the user was experiencing at any timestamp, and publishes the result to a dedicated topic.


Adding New Parsers
^^^^^^^^^^^^^^^^^^

These are the steps needed in order to add a new parser:

#. Create a new python module in thoughtprocess.parsers and name it '*parser_<parser_name>.py*'.

#. Add the following imports to your module:

   .. code-block:: python

       from .abstractparser import AbstractParser
       from .parser_registrator import ParserRegistrator

#. Create a class and have it extend AbstractParser.

   .. code-block:: python

          class ParserNameParser(AbstractParser):
              # TODO

#. Add the following decorator above the class declaration:

   .. code-block:: python
       :emphasize-lines: 1

       @ParserRegistrator.register('parser_name')
       class ParserNameParser(AbstractParser):
           # TODO

   | *Note*: the registered parser_name and the parser name in the file's name aren't required to be identical.

#. Implement the parse class method as such:

   .. code-block:: python
       :emphasize-lines: 6,7,8,9

       @ParserRegistrator.register('parser_name')
       class ParserNameParser(AbstractParser):
           @classmethod
           def parse(cls, data):
               metadata = cls.get_metadata(data)
               #
               # This is where the actual parsing 
               # should take place
               #
               return {**metadata, **parsed_results}

   | *Note*: the *data* parameter is a python dictionary that has the following keys:
   | user_id, username, birthdate, gender, timestamp, translation, rotation, color_image, depth_image, feelings.

#. You're good to go!