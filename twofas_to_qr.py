"""Module that converts 2fas backup files to QR codes"""
#!/usr/bin/env python3

import json
import os
import sys

import qrcode
from pathvalidate import sanitize_filename


class AuthCode:
    """Holds auth data and QR code for a single service"""

    def __init__(self, twofas_service):
        self.name = twofas_service["name"]
        self.secret = twofas_service["secret"]
        self.token_type = twofas_service["otp"]["tokenType"]
        if self.token_type != "TOTP":
            raise ValueError(
                f"Unsupported token type {self.token_type} for account {self.name}")
        self.account = twofas_service["otp"].get("account", self.name)
        self.otpauth = f"otpauth://totp/{self.account}?secret={self.secret}&issuer={self.name}"
        self.qr = qrcode.make(self.otpauth)

    def save_image(self, path):
        """Saves QR image to selected path"""
        self.qr.save(path)


def _eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        _eprint(f"Usage: {sys.argv[0]} <2fas_input_file> <output_directory>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.isfile(input_path):
        _eprint(f"Input file does not exist: {input_path}")
        sys.exit(1)

    if not os.path.isdir(output_path):
        _eprint(f"Output directory does not exist: {output_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        json_data = json.load(f)

    services = json_data["services"]

    for idx, service in enumerate(services):
        try:
            auth_code = AuthCode(service)
        except ValueError as error:
            _eprint(error)
            sys.exit(1)

        out_file = f"{output_path}/qr_{idx}_{sanitize_filename(auth_code.name)}.png"
        auth_code.save_image(out_file)

    print(f"Exported {len(services)} QR codes")
