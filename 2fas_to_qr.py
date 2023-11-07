#!/usr/bin/env python3

import json
import os
import qrcode
import sys

from pathvalidate import sanitize_filename

def _eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)
    
class AuthCode:
     def __init__(self, service):
        self.name = service['name']
        self.secret = service['secret']
        self.token_type = service['otp']['tokenType']
        if self.token_type != 'TOTP':
            raise Exception(f'Unsupported token type {self.token_type} for account {self.name}')
        self.account = service['otp'].get('account', self.name)
        self.otpauth = f'otpauth://totp/{self.account}?secret={self.secret}&issuer={self.name}'
        self.qr = qrcode.make(self.otpauth)

def twofas_to_qr(service):
    return AuthCode(service)
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        _eprint(f'Usage: {sys.argv[0]} <2fas_input_file> <output_directory>')
        
    input = sys.argv[1]
    output = sys.argv[2]
        
    if not os.path.isfile(input):
        _eprint(f'Input file does not exist: {input}')
        
    if not os.path.isdir(output):
        _eprint(f'Output directory does not exist: {output}')

    f = open(input)
    data = json.load(f)
    services = data['services'];

    for idx, service in enumerate(services):
        auth_code = twofas_to_qr(service)
        auth_code.qr.save(f'{output}/qr_{idx}_{sanitize_filename(auth_code.name)}.png')
        
    print(f'Exported {len(services)} QR codes')
    
