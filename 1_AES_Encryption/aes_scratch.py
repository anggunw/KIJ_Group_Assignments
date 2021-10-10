import os
import sys

sBox = [
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
]

def split_grids_in_16(s):
    all_grid = []
    for i in range(len(s)//16):
        b = s[i*16: i*16 + 16]
        grid = [[], [], [], []]
        for i in range(4):
            for j in range(4):
                grid[i].append(b[i + j*4])
        all_grid.append(grid)
    return all_grid

def add_round_key(expanded_key, round):
    return [row[round*4: round*4 + 4] for row in expanded_key]

def sbox(byte):
    x = byte >> 4
    y = byte & 15
    return sBox[x][y]

def expand_key(key, rounds):

    round_constants = [[1, 0, 0, 0]]

    for _ in range(1, rounds):
        round_constants.append([round_constants[-1][0]*2, 0, 0, 0])
        if round_constants[-1][0] > 0x80:
            round_constants[-1][0] ^= 0x11b

    key_grid = split_grids_in_16(key)[0]

    for round in range(rounds):
        last_column = [row[-1] for row in key_grid]
        last_column_rotate_step = rotate_row_left(last_column)
        last_column_sbox_step = [sbox(b) for b in last_column_rotate_step]
        last_column_round_constants_step = [last_column_sbox_step[i] ^ round_constants[round][i] for i in range(len(last_column_rotate_step))]

        for r in range(4):
            key_grid[r] += bytes([last_column_round_constants_step[r] ^ key_grid[r][round*4]])

        for i in range(len(key_grid)):
            for j in range(1, 4):
                key_grid[i] += bytes([key_grid[i][round*4+j] ^ key_grid[i][round*4+j+3]])

    return key_grid

def rotate_row_left(row, n=1):
    return row[n:] + row[:n]

def multiply_by_2(v):
    s = v << 1
    s &= 0xff
    if (v & 128) != 0:
        s = s ^ 0x1b
    return s

def multiply_by_3(v):
    return multiply_by_2(v) ^ v

def mix_columns(grid):
    new_grid = [[], [], [], []]
    for i in range(4):
        col = [grid[j][i] for j in range(4)]
        col = mix_column(col)
        for i in range(4):
            new_grid[i].append(col[i])
    return new_grid

def mix_column(column):
    r = [
        multiply_by_2(column[0]) ^ multiply_by_3(column[1]) ^ column[2] ^ column[3],
        multiply_by_2(column[1]) ^ multiply_by_3(column[2]) ^ column[3] ^ column[0],
        multiply_by_2(column[2]) ^ multiply_by_3(column[3]) ^ column[0] ^ column[1],
        multiply_by_2(column[3]) ^ multiply_by_3(column[0]) ^ column[1] ^ column[2],
    ]
    return r

def add_sub_key(block_grid, key_grid):
    r = []
    for i in range(4):
        r.append([])
        for j in range(4):
            r[-1].append(block_grid[i][j] ^ key_grid[i][j])
    return r

def enc(key, data):
    grids = split_grids_in_16(data)

    expanded_key = expand_key(key, 11)

    temp_grids = []
    round_key = add_round_key(expanded_key, 0)

    for grid in grids:
        temp_grids.append(add_sub_key(grid, round_key))

    grids = temp_grids

    for round in range(1, 10):
        temp_grids = []

        for grid in grids:
            sub_bytes_step = [[sbox(val) for val in row] for row in grid]
            shift_rows_step = [rotate_row_left(
                sub_bytes_step[i], i) for i in range(4)]
            mix_column_step = mix_columns(shift_rows_step)
            round_key = add_round_key(expanded_key, round)
            add_sub_key_step = add_sub_key(mix_column_step, round_key)
            temp_grids.append(add_sub_key_step)

        grids = temp_grids

    temp_grids = []
    round_key = add_round_key(expanded_key, 10)

    for grid in grids:
        sub_bytes_step = [[sbox(val) for val in row] for row in grid]
        shift_rows_step = [rotate_row_left(
            sub_bytes_step[i], i) for i in range(4)]
        add_sub_key_step = add_sub_key(shift_rows_step, round_key)
        temp_grids.append(add_sub_key_step)

    grids = temp_grids

    int_stream = []

    for grid in grids:
        for column in range(4):
            for row in range(4):
                int_stream.append(grid[row][column])

    return bytes(int_stream)
    
class AESScratch:
    def __init__(self, key, nonce):
        self.key = key
        self.nonce = nonce

    def createcounter(self, filelength):
        blocknum = filelength // 16
        if filelength % 16 != 0:
            blocknum += 1

        counter = ""

        for x in range(blocknum):
            counter += self.nonce.decode()
            counter += '%08d' % x

        return counter

    def ctr(self, filename):
        try:
            filelength = os.stat(filename).st_size
        except Exception as e:
            return str(e)

        # combine nonce with counter
        counter = self.createcounter(filelength).encode()

        result = enc(self.key, counter)

        # aes encryption
        return result

    def encrypt(self, filename):
        counter = self.ctr(filename)

        # read plain text
        try:
            fp = open(f"{filename}", 'rb')
            plaintext = fp.read()
            fp.close()
        except Exception as e:
            return str(e)

        # unpad counter
        filelength = os.stat(filename).st_size
        counter = counter[:filelength]

        # xor plain text with encrypted counter
        int_counter = int.from_bytes(counter, sys.byteorder)
        int_plaintext = int.from_bytes(plaintext, sys.byteorder)
        int_ciphertext = int_counter ^ int_plaintext
        ciphertext = int_ciphertext.to_bytes(len(counter), sys.byteorder)

        encryptedfilename = filename + ".enc"
        self.convertfile(ciphertext, filename, encryptedfilename)

        return(f"file {filename} has been encrypted to {encryptedfilename}")

    def decrypt(self, filename):
        counter = self.ctr(filename)

        # read ciphertext
        try:
            fp = open(f"{filename}", 'rb')
            ciphertext = fp.read()
            fp.close()
        except Exception as e:
            return str(e)

        # unpad counter
        filelength = os.stat(filename).st_size
        counter = counter[:filelength]

        # xor ciphertext with encrypted counter
        int_counter = int.from_bytes(counter, sys.byteorder)
        int_ciphertext = int.from_bytes(ciphertext, sys.byteorder)
        int_plaintext = int_counter ^ int_ciphertext
        plaintext = int_plaintext.to_bytes(len(counter), sys.byteorder)

        decryptedfilename = filename[:-4]
        self.convertfile(plaintext, filename, decryptedfilename)

        return (f"file {filename} has been decrypted to {decryptedfilename}")

    def convertfile(self, text, fromfile, tofile):
        fp = open(f"{tofile}", 'wb+')
        fp.write(text)
        fp.close()
        os.remove(fromfile)
        return

        