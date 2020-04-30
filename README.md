[![Build Status](https://travis-ci.org/assafmanor/thoughtprocess.svg?branch=master)](https://travis-ci.org/assafmanor/thoughtprocess)
[![codecov](https://codecov.io/gh/assafmanor/thoughtprocess/branch/master/graph/badge.svg)](https://codecov.io/gh/assafmanor/thoughtprocess)
[![Documentation Status](https://readthedocs.org/projects/thought-process/badge/?version=latest)](https://thought-process.readthedocs.io/en/latest/?badge=latest)

# Thought Process

A hardware that can read minds, and upload snapshots of cognitions!\
Submitted for the 'Advanced System Design' course in TAU.

## Getting Started

### Prerequisites
    
    Python 3.8
    Git
    Virtualenv
    Docker (worked with version 19.03.8)
    docker-compose (worked with version 1.25.4)

### Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone https://github.com/assafmanor/thoughtprocess.git
    ...
    $ cd thoughtprocess
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [Thought Process] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

### Deployement

In order to run all the services together, enter the following line from the thoughtprocess directory:

```sh
[Thought Process] $ ./scripts/run-pipeline.sh
```

### Basic Usage

After all services are up and running, you will be able to invoke the client to upload a sample, use the CLI to see the results, and a browser to visualize them in the GUI via `http://localhost:8080`. \
For further exaplanation see documentation.

## Documentation

The full documenation is available [here](https://thought-process.readthedocs.io/).
