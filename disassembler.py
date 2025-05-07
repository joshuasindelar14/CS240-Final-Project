import sys

op_codes = {
    "000000": "R-type",
    "100011": "lw",
    "101011": "sw",
    "000100": "beq",
    "000101": "bne",
    "100111": "pow",
    "100101": "addii",
    "101010": "sqrt",
    "110100": "max",
    "110101": "min",
    "110111": "avg",
    "110001": "abs",
    "111001": "mod",
    "011101": "fac",
    "010101": "srt",
    "001000": "li",
    "000010": "j",
    "001111": "lui",
}

func_codes = {
    "100000": "add",
    "100010": "sub",
    "100100": "and",
    "100101": "or",
    "101010": "slt",
    "100001": "add",
    "001100": "and",
    "011010": "div",
    "001010": "slt",
}

registers = {
    "00000": "$zero",
    "01000": "$t0",
    "01001": "$t1",
    "01010": "$t2",
    "01011": "$t3",
    "01100": "$t4",
    "01101": "$t5",
    "01110": "$t6",
    "01111": "$t7",
    "10000": "$s0",
    "10001": "$s1",
    "10010": "$s2",
    "10011": "$s3",
    "10100": "$s4",
    "10101": "$s5",
    "10110": "$s6",
    "10111": "$s7",
    "00100": "$a0",
    "00101": "$a1",
    "00110": "$a2",
    "00111": "$a3",
    "00010": "$v0",
    "00001": "$at",
}

def bin_to_signed_int(bin_str):
    return int(bin_str, 2) if bin_str[0] == '0' else int(bin_str, 2) - (1 << len(bin_str))

def handle_lines(bin_file: str):
    with open(bin_file, "r") as input_file:
        content = input_file.read().strip()
        lines = content.splitlines()

    mips_instructions = []
    for line in lines:
        mips_instructions.extend(bin_to_mips(line.strip()))

    with open("output.txt", "w") as output_file:
        output_file.write('\n'.join(mips_instructions) + '\n')


def bin_to_mips(line):
    mips = []
    for i in range(0, len(line), 32):
        bit_string = line[i:i+32]
        if len(bit_string) < 32:
            continue  # Skip incomplete instructions

        # NOP check
        if bit_string == "00000000000000000000000000000000":
            mips.append("nop")
            continue

        op_code = bit_string[0:6]

        if op_code == "000000":
            # syscall check
            if bit_string == "00000000000000000000000000001100":
                mips.append("syscall")
                continue

            # R-type
            rs = bit_string[6:11]
            rt = bit_string[11:16]
            rd = bit_string[16:21]
            shamt = bit_string[21:26]
            func_code = bit_string[26:32]
            mnemonic = func_codes.get(func_code, "unknown")
            mips.append(f"{mnemonic} {registers.get(rd, '?')}, {registers.get(rs, '?')}, {registers.get(rt, '?')}")
        elif op_code in ["100011", "101011"]:  # lw/sw
            rs = bit_string[6:11]
            rt = bit_string[11:16]
            offset = bin_to_signed_int(bit_string[16:32])
            mips.append(f"{op_codes[op_code]} {registers.get(rt, '?')}, {offset}({registers.get(rs, '?')})")
        elif op_code in ["000100", "000101"]:  # beq/bne
            rs = bit_string[6:11]
            rt = bit_string[11:16]
            offset = bin_to_signed_int(bit_string[16:32]) * 4  # relative offset (can add PC if needed)
            mips.append(f"{op_codes[op_code]} {registers.get(rs, '?')}, {registers.get(rt, '?')}, {offset}")
        elif op_code == "100111":  # pow
            rt = bit_string[6:11]
            rd = bit_string[11:16]
            imm = bin_to_signed_int(bit_string[16:32])
            mips.append(f"pow {registers.get(rd, '?')}, {registers.get(rt, '?')}, {imm}")
        elif op_code == "100101":  # addii
            rd = bit_string[6:11]
            imm1 = bin_to_signed_int(bit_string[11:21])
            imm2 = bin_to_signed_int(bit_string[21:32])
            mips.append(f"addii {registers.get(rd, '?')}, {imm1}, {imm2}")
        elif op_code in ["110100", "110101", "110111"]:  # max/min/avg
            rs = bit_string[6:11]
            rt = bit_string[11:16]
            rd = bit_string[16:21]
            mips.append(f"{op_codes[op_code]} {registers.get(rd, '?')}, {registers.get(rs, '?')}, {registers.get(rt, '?')}")
        elif op_code == "110001":  # abs
            rt = bit_string[6:11]
            rd = bit_string[11:16]
            mips.append(f"abs {registers.get(rd, '?')}, {registers.get(rt, '?')}")
        elif op_code == "101010":  # sqrt
            rs = bit_string[6:11]
            rt = bit_string[11:16]
            rd = bit_string[16:21]
            mips.append(f"sqrt {registers.get(rd, '?')}, {registers.get(rs, '?')}")
        elif op_code == "111001":  # mod
            rt = bit_string[6:11]
            rd = bit_string[11:16]
            imm = bin_to_signed_int(bit_string[16:32])
            mips.append(f"mod {registers.get(rd, '?')}, {registers.get(rt, '?')}, {imm}")
        elif op_code == "011101":  # fac
            rt = bit_string[6:11]
            rd = bit_string[11:16]
            mips.append(f"fac {registers.get(rd, '?')}, {registers.get(rt, '?')}")
        elif op_code == "010101":  # srt
            rt = bit_string[6:11]
            rd = bit_string[11:16]
            mips.append(f"srt {registers.get(rd, '?')}, {registers.get(rt, '?')}")
        elif op_code == "001000":  # li
            rt = bit_string[11:16]
            imm = bin_to_signed_int(bit_string[16:32])
            mips.append(f"li {registers.get(rt, '?')}, {imm}")
        elif op_code == "001111":  # lui
            rt = bit_string[11:16]
            imm = bin_to_signed_int(bit_string[16:32])
            mips.append(f"lui {registers.get(rt, '?')}, {imm}")
        elif op_code == "000010":  # j
            target = bit_string[6:32]
            target_address = int(target, 2) << 2
            mips.append(f"j {target_address}")
        else:
            # Unknown or generic I-type
            rs = bit_string[6:11]
            rt = bit_string[11:16]
            imm = bin_to_signed_int(bit_string[16:32])
            mips.append(f"{op_codes.get(op_code, 'unknown')} {registers.get(rs, '?')}, {registers.get(rt, '?')}, {imm}")

    return mips

if __name__ == "__main__":
    input_file = "disassembler_input.txt"
    handle_lines(input_file)
