# How to test

## Prerequisites
```bash
# go to zappy root
cd path/to/zappy_root/
# activate virtual environment
source ./venv/bin/activate
# install pytest with pip
pip3 install pytest
# install anyio to run async tests and web3 test pack 
pip3 install anyio web3[tester]
```
## Usage
```bash
pytest -v
```
The `-v` option will give you a detailed output of tests.

For extended usage documentation, take a look at the [pytest docs](https://docs.pytest.org/en/stable/usage.html).

## Asynchronous I/O Tests

Async I/O testing is done with the [Anyio library](https://anyio.readthedocs.io/en/latest/index.html).

Anyio provides a flexible and scalable library that adds support for pytest async tests.

The Python builtin `asyncio` library is supported on install. [Anyio also supports curio and trio as backends](https://anyio.readthedocs.io/en/latest/testing.html?highlight=pytest#specifying-the-backends-to-run-on).
