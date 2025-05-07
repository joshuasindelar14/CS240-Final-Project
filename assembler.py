import sys
import os

op_codes = {
    "add": "000000",
    "sub": "000000",
    "and:": "000000",
    "or:": "000000",
    "slt": "000000",
    "lw": "100011",
    "sw": "101011",
    "beq": "000100",
    "bne": "000101",
    "pow": "100011",
    "addii": "100101",
    "sqrt": "101010",
    "max": "110100",
    "min": "110101",
    "avg": "110111",
    "abs": "110001",
    "mod": "111001",
    "fac": "011101",
    "srt": "010101",
    "li": "001000",
    "j": "000010",
    "lui": "001111",
    "move": "000000",
    "syscall": "000000"
}

func_codes = {
    "add": "100000",
    "sub": "100010",
    "and:": "100100",
    "or:": "100101",
    "slt": "101010",
    "move": "100000",       
    "syscall": "001100"
}

registers = {
    "$zero": "00000",
    "$t1": "01001",
    "$t2": "01010",
    "$t3": "01011",
    "$t4": "01100",
    "$t5": "01101",
    "$t6": "01110",
    "$t7": "01111",
    "$s0": "10000",
    "$s1": "10001",
    "$s2": "10010",
    "$s3": "10011",
    "$s4": "10100",
    "$s5": "10101",
    "$s6": "10110",
    "$s7": "10111",
    "$a0": "00100",
    "$a1": "00101",
    "$a2": "00110",
    "$a3": "00111",
    "$v0": "00010"
}

shift_logic_amount = "00000"

def interpret_line(mips_file: str):
    input_file = open(mips_file, "r")
    output_file = open("assembler_output.bin", "w")
    for instruction in input_file:
        bin = assemble(instruction.strip())
        output_file.write(bin + "\n")

def assemble(line):
    line = line.split("#")[0].strip()

    if not line:
        return

    parts = line.split(" ")
    op_code = parts[0]

    if op_code in func_codes:
        if op_code == "move":
            rd, rs = parts[1], parts[2]
            return op_codes["add"] + registers[rs] + registers["$zero"] + registers[rd] + shift_logic_amount + func_codes["add"]
        elif op_code == "syscall":
            return op_codes["syscall"] + "00000000000000000000" + func_codes["syscall"]
        else:
            rd, rs, rt = parts[1], parts[2], parts[3]
            return op_codes[op_code] + registers[rs] + registers[rt] + registers[rd] + shift_logic_amount + func_codes[op_code]
    if op_code in ["pow", "max", "min", "avg", "mod"]:
        rd, rs, rt = parts[1], parts[2], parts[3]
        return op_codes[op_code] + registers[rs] + registers[rt] + registers[rd] + shift_logic_amount + "000000"
    if op_code in ["abs", "sqrt", "fac", "srt"]:
        rd, rs = parts[1], parts[2]
        return op_codes[op_code] + registers[rs] + "00000" + registers[rd] + shift_logic_amount + "000000"
    
    if op_code == "li":
        rt, imm = parts[1], int(parts[2])
        return op_codes[op_code] + registers["$zero"] + registers[rt] + format(imm & 0xFFFF, "016b")
    if op_code in ["addi", "addii"]:
        rt, rs, imm = parts[1], parts[2], int(parts[3])
        return op_codes["addii"] + registers[rs] + registers[rt] + format(imm & 0xFFFF, "016b")
    if op_code == "lui":
        rt, imm = parts[1], int(parts[2])
        return op_codes[op_code] + "00000" + registers[rt] + format(imm & 0xFFFF, "016b")
    if op_code in ["lw", "sw"]:
        rt = parts[1]
        offset, rs = parts[2].replace(")", "").split("(")
        offset_bin = format(int(offset), "016b")
        return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin
    if op_code in ["beq", "bne"]:
        rs, rt, offset = parts[1], parts[2], int(parts[3])
        return op_codes[op_code] + registers[rs] + registers[rt] + format(offset & 0xFFFF, "016b")
    if op_code == "j":
        addr = int(parts[1])
        return op_codes[op_code] + format(addr, "026b")

    return None


mips_file = "assembler_input.asm"
interpret_line(mips_file)
