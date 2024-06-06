# Buttercup to Proton Pass Converter

This repository contains a Python script to convert CSV exports from the Buttercup password manager into a format compatible with Proton Pass. The script handles multiline entries, special characters, and combines relevant fields into the notes section for a seamless import experience.

## Features

- Converts Buttercup CSV exports to Proton Pass compatible CSV format.
- Handles multiline entries and special characters.
- Combines additional fields (, `Pseudo`, `Code` `extra-note`) into the notes section.

## Usage

### Prerequisites

- Python 3.x
- pandas library

You can install pandas using pip:

```sh
pip install pandas
