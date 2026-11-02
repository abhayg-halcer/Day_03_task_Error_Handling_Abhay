# Python Data Toolkit

A Python CLI application for loading, validating, and analyzing sales CSV files.

## Setup
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

## Usage
python -m data_toolkit.cli tests/fixtures/sample_sales.csv

## Tests
python -m pytest -v
python -m pytest --cov=data_toolkit --cov-report=term-missing

## Validation Rules
- Required columns: product, quantity, price
- Product name must not be empty.
- Quantity must be a positive integer.
- Price must be non-negative and finite.

## Logging
Application logs are written to logs/app.log.

## Test Results
The current test suite contains 26 passing tests and achieves 96.41% coverage.
