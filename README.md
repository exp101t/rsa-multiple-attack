# Installation
1. Download the project: `git clone https://github.com/exp101t/rsa-multiple-attack.git`
2. Install Python requirements: `pip3 install -r requirements.txt`
# Arguments list
| Argument | Argument purpose |
|:--------:|------------------|
| `-h` / `--help` | Shows argument list |
| `--key-files` | List of files (separated by space) with RSA public keys (in PEM format) |
| `--enc-files` | List of files (separated by space) with encrypted data (raw binary or Base64) |
| `--exponents`<br>`--modules`<br>`--ciphertexts` | List of exponents / modules / ciphertexts separated by space<br>They must be presented as decimal / hexidecimal integer or in Base64 |
| `--exponents-list`<br>`--modules-list`<br>`--ciphertexts-list` | File with exponents / modules / ciphertexts<br>They must be presented as decimal / hexidecimal integer or in Base64 (line by line) | 
| `--chosen-plaintext` | Starts chosen plaintext attack in interactive mode<br>At least one key and ciphertext must be provided |
