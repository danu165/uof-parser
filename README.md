# Use of Force Collector and Parser

This project will house code to collect and parse use of force policies.

Collector (not developed yet)
* This will automatically search the web for a police department's use of force policy and download it.

Parser (currently in proof-of-concept)
* This is driven by a `config.yaml` file.
* The config file lists initial search terms for each policy.
    * Once the search term is found, the sentence is returned.
    * It then checks if the sentence contains certain phrases. If so, it receives a positive indicator.

## Getting Started

This project uses pipenv to manage its packages.

### Prerequisites

To install pipenv:

```
pip install pipenv
```

### Installing

Once pipenv is installed, simply run this:

```
pipenv install
```

## Running the tests

`pytest . -v -s`