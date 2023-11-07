# Overview

Converts 2FAS authenticator backup files to QR codes that can be imported into any other authenticator app.

See: <https://2fas.com/>

## Usage

Using the app go to Settings -> Backup -> Export -> Disable Set Password Option -> Export to File

Move the file to a system with python3 and execute script:

```bash
pip3 install -r requirements.txt
python3 ./2fas_to_qr.py '<2FAS Input File>' '<Output Directory>'
```

Then scan the generated codes using your authenticator app of preference. Remember to delete the 2FAS backup file as well as generated QR codes afterwards! They contain the plaintext secrets that anyone can see.
