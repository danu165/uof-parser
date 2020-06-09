# Use of Force Collector and Parser

This project will house code to collect and parse use of force policies.

Collector (not developed yet) `uof_collector`
* This will automatically search the web for a police department's use of force policy and download it.
* The current code in `uof_collector` is in its infant stages

Parser (currently in proof-of-concept) `uof_parser`
* This is driven by a `config.yaml` file.
* The config file lists initial search terms for each policy.
    * Once the search term is found, the sentence is returned.
    * It then checks if the sentence contains certain phrases. If so, it receives a positive indicator.
    * Additional conditions can be provided within double parentheses.

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

```
make test
```