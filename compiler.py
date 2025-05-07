memoryAddress = 5000
tRegister = 0
vars = dict()
labelCounter = 0
dataSection = ""


def getNewLabel():
    global labelCounter
    labelCounter += 1
    return f"label{labelCounter}"



def getNewEndPrintLabel():
    global labelCounter
    labelCounter += 1
    return f"END_PRINT{labelCounter}"



def getInstructionLine(varName):
    global memoryAddress, tRegister
    tRegisterName = f"$t{tRegister}"
    setVariableRegister(varName, tRegisterName)
    returnText = f"addi {tRegisterName}, $zero, {memoryAddress}"
    tRegister += 1
    memoryAddress += 4
    return returnText


def setVariableRegister(varName, tRegister):
    global vars
    vars[varName] = tRegister


def getVariableRegister(varName):
    global vars
    if varName in vars:
        return vars[varName]
    else:
        return "ERROR"


def getAssignmentLinesImmediateValue(val, varName):
    global tRegister
    outputText = f"""addi $t{tRegister}, $zero, {val}
sw $t{tRegister}, 0({getVariableRegister(varName)})"""
    tRegister += 1
    return outputText


def getAssignmentLinesVariable(varSource, varDest):
    global tRegister
    outputText = ""
    registerSource = getVariableRegister(varSource)
    outputText += f"lw $t{tRegister}, 0({registerSource})\n"
    tRegister += 1
    registerDest = getVariableRegister(varDest)
    outputText += f"sw $t{tRegister - 1}, 0({registerDest})"
    return outputText


def parse_for_loop(line):
    global tRegister
    outputText = getInstructionLine("i") + "\n"
    outputText += getAssignmentLinesImmediateValue(1, "i") + "\n"
    loopStartLabel = getNewLabel()
    loopEndLabel = getNewLabel()
    outputText += f"{loopStartLabel}:\n"
    outputText += f"lw $t{tRegister}, 0({getVariableRegister('i')})\n"
    outputText += f"addi $t{tRegister + 1}, $zero, 100\n"
    outputText += f"slt $t{tRegister + 2}, $t{tRegister + 1}, $t{tRegister}\n"
    outputText += f"bne $t{tRegister + 2}, $zero, {loopEndLabel}\n"
    tRegister += 3
    return outputText, loopStartLabel, loopEndLabel



def parse_condition_if(expr):
    global tRegister
    outputText = ""
    var, mod_val = expr.split(" % ")
    var = var.strip()
    mod_val = mod_val.strip().split()[0]

    failLabel = getNewLabel()
    outputText += f"lw $t{tRegister}, 0({getVariableRegister(var)})\n"
    outputText += f"mod $t{tRegister + 1}, $t{tRegister}, {mod_val}\n"
    outputText += f"bne $t{tRegister + 1}, $zero, {failLabel}\n"
    tRegister += 2
    return outputText, failLabel



def parse_printf(line):
    global tRegister, dataSection
    if 'printf(' in line:
        if '"' in line:
            start = line.index('"') + 1
            end = line.index('"', start)
            string_value = line[start:end]
            label = getNewLabel()
            endPrintLabel = getNewEndPrintLabel()
            outputText = f"addi $v0, $zero, 4\n"
            outputText += f"la $a0, {label}\n"
            outputText += f"syscall\n"
            outputText += f"j {endPrintLabel}\n"
            dataSection += f"{label}: .asciiz \"{string_value}\"\n"
            outputText += f"{endPrintLabel}:\n"
            return outputText
        elif '%d' in line:
            endPrintLabel = getNewEndPrintLabel()
            outputText = f"addi $v0, $zero, 1\n"
            outputText += f"lw $a0, 0({getVariableRegister('i')})\n"
            outputText += f"syscall\n"
            outputText += f"addi $v0, $zero, 11\n"
            outputText += f"addi $a0, $zero, 10\n"
            outputText += f"syscall\n"
            outputText += f"j {endPrintLabel}\n"
            outputText += f"{endPrintLabel}:\n"
            return outputText



def parse_else_if(expr):
    conditionCode, failLabel = parse_condition_if(expr)
    return conditionCode, failLabel



outputText = ".text\nmain:\n"
dataSection = ".data\n"
loopStartLabel = loopEndLabel = ""

f = open("fizzbuzz.c", "r")
lines = f.readlines()

for line in lines:
    line = line.strip()

    if line.startswith("for ("):
        loopInit, loopStartLabel, loopEndLabel = parse_for_loop(line)
        outputText += loopInit

    elif line.startswith("if "):
        condition_expr = line.split("if ")[1].strip("()")
        ifCode, currentFailLabel = parse_condition_if(condition_expr)
        outputText += ifCode

    elif "else if" in line:
        outputText += f"{currentFailLabel}:\n"
        condition_expr = line.split("else if ")[1].strip("()")
        elseIfCode, currentFailLabel = parse_else_if(condition_expr)
        outputText += elseIfCode

    elif "else" in line:
        outputText += f"{currentFailLabel}:\n"

    elif 'printf(' in line:
        outputText += parse_printf(line)


    elif line == "}":
        outputText += f"lw $t{tRegister}, 0({getVariableRegister('i')})\n"
        outputText += f"addi $t{tRegister}, $t{tRegister}, 1\n"
        outputText += f"sw $t{tRegister}, 0({getVariableRegister('i')})\n"
        outputText += f"j {loopStartLabel}\n"
        if loopEndLabel not in outputText:
            outputText += f"{loopEndLabel}:\n"
            outputText += f"addi $v0, $zero, 10\nsyscall\n"
        tRegister += 1

outputText += dataSection

outputFile = open("output.asm", "w")
outputFile.write(outputText)
outputFile.close()