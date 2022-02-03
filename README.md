## Zappy
### ZAP-PYTHON

ZAP Oracles (introduction here)

This repository provides Interface to Zap contracts and tools to use Zap platform with Python projects
Each package is a public npm module that serve developer's needs to intergrate Zap platform

# Development

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes

### Prerequisites

```
python3 -m venv venv
source ./venv/bin/activate
```

### Installing

```
pip3 install -r requirements.txt
```

### Setup
Create a `config.json` file in the root of the project./
Add your private key to the property `privateKey`/
For example:
```
{
    "privateKey": "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
}
```

## Running build and tests
* Run all tests: `pytest`
* Run a specific test file: `pytest tests/nft/<folder>/<file-name>.py`
* Run a specific test in a file: `pytest tests/nft/<folder>/<file-name>.py::<nameof_test>`
    * Example: `pytest tests/nft/zap_media/test_zapMedia.py::test_total_supply` will only run `test_total_supply` in `test_zapMedia.py`  


    ### Notes:
    Add `-v` flag `pytest -v` for verbose messages.  
    Will only run tests in `./tests/nft/*`  
## Packages

## Usage

##### Creating a Zap Provider oracle
```

```
**With Custom configuration**
```

```
**Some example for provider usage**



## Built With


## Contributing

Please read [CONTRIBUTING.md]() for details on our code of conduct, and the process for submitting pull requests to us.


See also the list of [contributors]()

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
