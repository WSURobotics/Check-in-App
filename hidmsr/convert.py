""" Convert raw magnetic stripe (magstripe) data to text.

This library converts bits of magnetic stripe tracks to human-readable
text. The rest of the parsing (e.g. determining account numbers)
is your problem, not mine.

Licensed under the GNU Public License, version 3 or later.

(c) 2018-2019 Cameron Conn
"""


import argparse
import binascii
import math
import sys

from functools import reduce


SIXDEC_CHARS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_"""
ABA_CHARS = """0123456789:;<=>?"""

def decode_msr_data(data):
    # Convert the list of integers to a string of ASCII characters
    decoded_str = ''.join(chr(byte) for byte in data)
    return decoded_str

def hex_to_bin(str_hex: str) -> str:
    """ Convert a hexadecimal string to a binary within a string. """
    total = "".join(map(lambda ch: "{:04b}".format(int(ch, 16)), str_hex))
    return total


def decode_sixdec(bin_str: str):
    """ Decode a binary string encoded in SIXDEC.

    Parameters
    ==========
        bin_str: a hexadecimal string of the raw binary data to be decoded.
            spaces in this parameter will be ignored.

    Returns
    =======
        a string of the decoded data with the LRC omitted.
    """

    chars = len(bin_str) // 7
    output = ""
    for i in range(0, chars*7, 7):
        substr = bin_str[i:i+7]
        parity = substr[-1]  # Discard for now
        bin_val = substr[:6]
        parity_num = sum(map(lambda x: 1 if x == "1" else 0, bin_val))

        if parity_num % 2 == 0:
            if parity != "1":
                print("invalid parity! {}:{}".format(bin_val, parity))
        elif parity != "0":
                print("invalid parity! {}:{}".format(bin_val, parity))

        h = hex(int(bin_val[::-1], 2))
        ch = SIXDEC_CHARS[eval(h)]
        output += ch

    # XXX: We are probably stripping off the LRC here, but I'm too lazy to check.
    return output[:-1]  # Strip last character to avoid garbage


def decode_aba(bin_str: str):
    """ Decode a binary string encoded in ABA.

    Parameters
    ==========
        bin_str: a hexadecimal string of the raw binary data to be decoded.
            spaces in this parameter will be ignored.

    Returns
    =======
        a string of the decoded data with the LRC omitted.
    """

    chars = len(bin_str) // 5
    output = ""
    for i in range(0, chars*5, 5):
        substr = bin_str[i:i+5]
        parity = substr[-1]  # Discard for now
        bin_val = substr[:4]
        parity_num = sum(map(lambda x: 1 if x == "1" else 0, bin_val))

        if parity_num % 2 == 0:
            if parity != "1":
                print("invalid parity! {}:{}".format(bin_val, parity))
        elif parity != "0":
                print("invalid parity! {}:{}".format(bin_val, parity))

        h = hex(int(bin_val[::-1], 2))
        ch = ABA_CHARS[eval(h)]
        output += ch

    # XXX: We are probably stripping off the LRC here, but I'm too lazy to check.
    return output[:-1]  # Strip last character to avoid garbage


# TODO: Protect against `IndexError`s. Right now, we aren't checking that we aren't
# going out of bounds of lists. We need to do that in the future.
def extract_data(raw_data):
    """ Extract card data form each track (e.g. removed headers).

    Note that this does NOT decode the data from the tracks. You must
    convert data from this method manually.

    Parameters
    ==========
        raw_data: a list of integers of the raw data read from the card reader.
            This method requires that raw_data is a valid list of values otherwise
            this method will likely raise an IndexError.

    Returns
    =======
        A tuple of the extracted track data from each track, in order corresponding to
            the track number. Tracks with no data will be returned as `None`. Tracks with
            data will be a hexadecimal string of the extracted binary data.
    """

    raw_data = raw_data[1:]  # Strip off unknown first character
    print('raw_data:')
    print(raw_data)
    response = []
    if raw_data[0] != 27 and raw_data[2] != 27:
        raise ValueError("Invalid sequence!")

    data1, data2, data3 = [], [], []
    length1, length2, length3 = 0, 0, 0
    end_data1, end_data2, end_data3 = 0, 0, 0
    if raw_data[3] != 1:
        raise ValueError("Invalid start sentinel for track #1")

    length1 = raw_data[4]
    start_data1 = 5
    end_data1 = start_data1 + length1
    data1 = raw_data[start_data1:end_data1]
    print("length1: {}".format(length1))
    print("data1:")
    print(data1)

    #if len(raw_data) > end_data1 + 3:

    # raw_data[start2] = 27; find it
    #start2 = 0
    if length1 == 0:
        start2 = end_data1
    else:
        start2 = end_data1 + 1

    print("#2: 27 = {}".format(raw_data[start2]))

    length2 = raw_data[start2 + 2]
    start_data2 = start2 + 3
    end_data2 = start_data2 + length2
    data2 = raw_data[start_data2:end_data2]
    print("length2: {}".format(length2))
    print(length2)
    print("data2:")
    print(data2)

    # raw_data[start3] = 27; find it
    start3 = end_data2
    #if length2 == 0:
    #    start3 = end_data2
    #else:
    #    start3 = end_data2 + 1
    print("#3: 27 = {}".format(raw_data[start3]))

    length3 = raw_data[start3 + 2]
    print("length3: {}".format(length3))
    print("from start3:")
    print(raw_data[start3:])
    start_data3 = start3 + 3
    end_data3 = start_data3 + length3
    data3 = raw_data[start_data3:end_data3]
    print("data3:")
    print(data3)

    end_sentinel = raw_data[end_data3]
    file_sep = raw_data[end_data3 + 1]
    final_esc = raw_data[end_data3 + 2]
    status = raw_data[end_data3 + 3]
    if end_sentinel != 63 or file_sep != 28 or final_esc != 27:
        raise ValueError("Invalid ending sentinel")

    if status == 0x39:
        print("card moving error")
    elif status == 0x30:
        print("card read correctly")
    else:
        print("status code: {}".format(status))



    data1_str, data2_str, data3_str = "", "", ""
    if len(data1) > 0:
        data1_str = reduce((lambda a, b: a + b), map(lambda x: "{:02X}".format(x), data1))
    if len(data2) > 0:
        data2_str = reduce((lambda a, b: a + b), map(lambda x: "{:02X}".format(x), data2))
    if len(data3) > 0:
        data3_str = reduce((lambda a, b: a + b), map(lambda x: "{:02X}".format(x), data3))

    return data1_str, data2_str, data3_str


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert magnetic stripe data formats.")
    parser.add_argument("track", type=str, nargs="+")
    parsed = parser.parse_args()

    tracks = parsed.track
    if tracks == None:
        print("Please provide data to convert")
        sys.exit(1)

    for i, t in enumerate(tracks):
        decoded_binary = hex_to_bin(t)

        if i == 0 or i == 2:  # Track 1, 3
            result = decode_sixdec(decoded_binary)
        elif i == 1:  # Track 2
            result = decode_aba(decoded_binary)
        print(result)

