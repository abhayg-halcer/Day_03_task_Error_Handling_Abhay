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

## Assumptions

- Input data is provided as a CSV file.
- The CSV file contains the required columns: `product`, `quantity`, and `price`.
- Product names must not be empty.
- Quantity must be a positive integer.
- Price must be a non-negative finite number.
- CSV input is expected to use UTF-8 encoding.

## Limitations

- The application currently processes CSV files only.
- It does not connect to a database or external sales API.
- The application validates the supplied records but does not automatically correct invalid data.
- Sales totals are calculated from the supplied prices; no currency conversion is performed.
- The application is designed as a command-line tool rather than a graphical application.
