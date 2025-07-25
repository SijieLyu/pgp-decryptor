# pgp-decryptor

A Python tool to batch decrypt `.gpg` files using GPG with multiprocessing support.

## Structure
pgp_decryptor/
├── pgp_decryptor/  <br>
│   ├── __init__.py <br>
│   ├── decryptor.py <br>
│   └── cli.py <br>
├── README.md <br>
├── pyproject.toml <br>
├── LICENSE <br>

## Features

- Parallel decryption using multiple processes
- Outputs CSV summary with decryption results
- Simple CLI support for automation and scripting

## Installation Locally
Inthe root of your project directory (where pyproject.toml is):
```bash
pip install .
```

Or for development mode (hot reload changes):
```bash
pip install -e .
```

## Usage

### Requirements
- GPG must be installed and accessible in your system PATH
- You must have the corresponding private key in your keyring

### As a Library

```python
from pgp_decryptor import PGPDecryptor

decryptor = PGPDecryptor(
    input_base_dir="path/to/encrypted",
    output_base_dir="path/to/decrypted",
    summary_dir="path/to/summary",
    num_workers=4
)
decryptor.batch_decrypt(["dataset1", "dataset2"])
```

### As Command Line
```bash
pgp-decryptor \
  --input ./encrypt \
  --output ./decrypt \
  --summary ./summary \
  --datasets dataset1 dataset2 \
  --workers 4
```





