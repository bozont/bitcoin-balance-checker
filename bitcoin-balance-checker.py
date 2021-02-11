#!/usr/bin/env python3

import sys
import re
from time import sleep
from urllib.request import urlopen
from urllib.error import URLError
import argparse
from os import path


def check_balance(address):

    blockchain_tags_json = [ 
        'total_received',
        'final_balance',
        ]

    SATOSHIS_PER_BTC = 1e+8

    check_address = address

    parse_address_structure = re.match(r' *([a-zA-Z1-9]{1,34})', check_address)
    if ( parse_address_structure is not None ):
        check_address = parse_address_structure.group(1)
    else:
        print( "\nThis Bitcoin Address is invalid" + check_address )
        exit(1)

    print( "\nBitcoin Address = " + check_address )

    try:
        htmlfile = urlopen("https://blockchain.info/address/{}?format=json".format(check_address), timeout = 10)
        htmltext = htmlfile.read().decode('utf-8')
    except URLError as e:
        print("Request failed. Reason: {}".format(e.reason))
        return

    blockchain_info_array = []
    tag = ''
    try:
        for tag in blockchain_tags_json:
            blockchain_info_array.append (
                float( re.search( r'%s":(\d+),' % tag, htmltext ).group(1) ) )
    except:
        print( "Error '%s'." % tag )
        exit(1)

    for i, btc_tokens in enumerate(blockchain_info_array):

        sys.stdout.write ("%s \t= " % blockchain_tags_json[i])
        if btc_tokens > 0.0:
            print( "%.8f Bitcoin" % (btc_tokens/SATOSHIS_PER_BTC) )
        else:
            print( "0 Bitcoin" )


def main():
    argparser = argparse.ArgumentParser(description='BTC wallet balance checker')
    argparser.add_argument('wallet_address_or_file',
                       metavar='wallet_address_or_file',
                       type=str,
                       help='Wallet address or path to a text file with wallet addresses')

    args = argparser.parse_args()
    addr_or_file = args.wallet_address_or_file

    if path.exists(addr_or_file):
        with open("list-addresses.txt") as file:
            for line in file:
                address = str.strip(line)
                print("__________________________________________________\n")
                check_balance(address)

    else:
        check_balance(addr_or_file)


if __name__ == "__main__":
    main()
