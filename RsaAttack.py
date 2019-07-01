from Crypto.PublicKey import RSA
from attacks import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This tool is for attacks on RSA multiple keys')

    parser.add_argument('--key-files', nargs='*', help='Specify RSA public keys in standart form')
    parser.add_argument('--enc-files', nargs='*', help='Specify encrypted files')
    parser.add_argument('--chosen-plaintext', action='store_true', help='Specify to start chosen plaintext attack')
    parser.add_argument('--exponents', nargs='*', help='Specify exponents of keys')
    parser.add_argument('--modules', nargs='*', help='Specify modules of keys')
    parser.add_argument('--ciphertexts', nargs='*', help='Specify ciphertexts')
    parser.add_argument('--exponents-list', nargs=1, help='Specify file with exponents (line by line)')
    parser.add_argument('--modules-list', nargs=1, help='Specify file with modules (line by line)')
    parser.add_argument('--ciphertexts-list', nargs=1, help='Specify file with ciphertexts (line by line)')

    args = parser.parse_args()

    exponents, modules, ciphertexts = list(), list(), list()

    if args.exponents_list is not None:
        for file_name in args.exponents_list:
            lines = open(file_name, 'r').readlines()
            exponents = [transform_to_int(l) for l in lines]

    if args.modules_list is not None:
        for file_name in args.modules_list:
            lines = open(file_name, 'r').readlines()
            modules = [transform_to_int(l) for l in lines]

    if args.ciphertexts_list is not None:
        for file_name in args.ciphertexts_list:
            lines = open(file_name, 'r').readlines()
            ciphertexts = [transform_to_int(l) for l in lines]

    if args.exponents is not None:
        for e in args.exponents:
            exponents.append(transform_to_int(e))

    if args.modules is not None:
        for n in args.modules:
            modules.append(transform_to_int(n))

    if args.ciphertexts is not None:
        for c in args.ciphertexts:
            ciphertexts.append(transform_to_int(c))

    if args.key_files is not None:
        for file_name in args.key_files:
            key = open(file_name, 'r').read()
            key_handle = RSA.importKey(key)

            exponents.append(key_handle.e)
            modules.append(key_handle.n)

    if args.enc_files is not None:
        for file_name in args.enc_files:
            buffer = open(file_name, 'rb').read()

            try:
                if match(r'^[\w+/=\r\n]+$', buffer.decode()):
                    ciphertexts.append(transform_to_int(buffer.decode()))
                else:
                    ciphertexts.append(bytes_as_int(buffer))
            except:
                ciphertexts.append(bytes_as_int(buffer))

    if len(exponents) != len(modules) or len(modules) != len(ciphertexts):
        print('[-] You should provide the same number of ciphertexts and keys')
        exit(0)

    if args.chosen_plaintext:
        chosen_plaintext(modules[0], exponents[0], ciphertexts[0])
        exit(0)

    # First of all, trying to find e keys with exponent e
    common_e_dict = dict()

    for index, e in enumerate(exponents):
        temp = common_e_dict.get(e, (list(), list()))

        common_e_dict[e] = (
            temp[0] + [modules[index]], 
            temp[1] + [ciphertexts[index]]
        )

        if len(temp[0]) == e - 1:
            print(common_exponent(e, *common_e_dict[e]))
            exit(0)

    # Trying to find keys with common modulus
    for i in range(len(modules)):
        for j in range(i + 1, len(modules)):
            if modules[i] == modules[j] and gcd(exponents[i], exponents[j]) == 1:
                print(common_modulus(
                    modules[i],
                    exponents[i], exponents[j],
                    ciphertexts[i], ciphertexts[j]
                ))
                exit(0)

            if gcd(modules[i], modules[j]) > 1:
                print(common_divisor(
                    modules[i], modules[j],
                    exponents[i], ciphertexts[i]
                ))
                exit(0)