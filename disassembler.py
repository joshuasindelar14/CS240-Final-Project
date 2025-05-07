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
}
func_codes = {
    "100000": "add",
    "100010": "sub",
    "100100": "and",
    "100101": "or",
    "101010": "slt",
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
}


def handle_lines(bin_file: str):
    with open(bin_file, "r") as input_file:
        lines = input_file.readlines()

    mips_instructions = []
    for line in lines:
        mips_instructions.extend(bin_to_mips(line.strip()))

    with open("output.txt", "w") as output_file:
        for instruction in mips_instructions:
            output_file.write(instruction + "\n")


def bin_to_mips(line):
    mips = []
    bit_string = ""
    for i in range(0, len(line)):
        bit_string += line[i]
        if len(bit_string) == 32:
            op_code = bit_string[0:6]
            print(op_code)
            if op_code == "000000":
                rs, rt, rd, shift, func_code = (
                    bit_string[6:11],
                    bit_string[11:16],
                    bit_string[16:21],
                    bit_string[21:26],
                    bit_string[26:32],
                )
                mips.append(
                    f"{func_codes[func_code]} {registers[rd]}, {registers[rs]}, {registers[rt]}"
                )
            elif op_code in ["100011", "101011"]:
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                mips.append(
                    f"{op_codes[op_code]} {registers[rt]}, {int(offset, 2)}({registers[rs]})"
                )
            elif op_code == "100111":  # pow $t0, $t1, imm
                rt, rd, imm = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                mips.append(f"pow {registers[rd]}, {registers[rt]}, {int(imm, 2)}")
            elif op_code == "100101":  # addii $t0, imm1, imm2
                rd, imm1, imm2 = bit_string[6:11], bit_string[11:21], bit_string[21:32]
                mips.append(f"addii {registers[rd]}, {int(imm1, 2)}, {int(imm2, 2)}")
            elif op_code == "101010":  # sqrt $t0, $t1
                rt, rd = bit_string[6:11], bit_string[11:16]
                mips.append(f"sqrt {registers[rd]}, {registers[rt]}")
            elif op_code == "110100":  # max $t0, $t1, $t2
                rs, rt, rd = bit_string[6:11], bit_string[11:16], bit_string[16:21]
                mips.append(f"max {registers[rd]}, {registers[rs]}, {registers[rt]}")
            elif op_code == "110101":  # min $t0, $t1, $t2
                rs, rt, rd = bit_string[6:11], bit_string[11:16], bit_string[16:21]
                mips.append(f"min {registers[rd]}, {registers[rs]}, {registers[rt]}")
            elif op_code == "110111":  # avg $t0, $t1, $t2
                rs, rt, rd = bit_string[6:11], bit_string[11:16], bit_string[16:21]
                mips.append(f"avg {registers[rd]}, {registers[rs]}, {registers[rt]}")
            elif op_code == "110001":  # abs $t0, $t1
                rt, rd = bit_string[6:11], bit_string[11:16]
                mips.append(f"abs {registers[rd]}, {registers[rt]}")
            elif op_code == "111001":  # mod $t0, $t1, imm
                rt, rd, imm = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                mips.append(f"mod {registers[rd]}, {registers[rt]}, {int(imm, 2)}")
            elif op_code == "011101":  # fac $t0, $t1
                rt, rd = bit_string[6:11], bit_string[11:16]
                mips.append(f"fac {registers[rd]}, {registers[rt]}")
            elif op_code == "010101":  # srt $t0, $t1
                rt, rd = bit_string[6:11], bit_string[11:16]
                mips.append(f"srt {registers[rd]}, {registers[rt]}")
            else:
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                mips.append(
                    f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}, {int(offset, 2)}"
                )

            bit_string = ""
    return mips


if __name__ == "__main__":
    input_file = "input.txt"
    handle_lines(input_file)
