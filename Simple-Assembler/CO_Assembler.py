# opcode,no.of registers,no. of imm,memory
opcode = {
    "add": ("00000", 3, 0, 0),
    "sub": ("00001", 3, 0, 0),
    "movi": ("00010", 1, 1, 0),
    "movr": ("00011", 2, 0, 0),
    "ld": ("00100", 1, 0, 1),
    "st": ("00101", 1, 0, 1),
    "mul": ("00110", 3, 0, 0),
    "div": ("00111", 2, 0, 0),
    "rs": ("01000", 1, 1, 0),
    "ls": ("01001", 1, 1, 0),
    "xor": ("01010", 3, 0, 0),
    "or": ("01011", 3, 0, 0),
    "and": ("01100", 3, 0, 0),
    "not": ("01101", 2, 0, 0),
    "cmp": ("01110", 2, 0, 0),
    "jmp": ("01111", 0, 0, 1),
    "jlt": ("10000", 0, 0, 1),
    "jgt": ("10001", 0, 0, 1),
    "je": ("10010", 0, 0, 1),
    "hlt": ("10011", 0, 0, 0),
    "mov": ("dummy", 0, 0, 0)
}
# Flag register to be taken care separately
registers = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
}

error_type = {
    1: "Typos in instruction name or register name",
    2: "Use of undefined variables",
    3: "Use of undefined labels",
    4: "Illegal use of FLAGS register",
    5: "Illegal Immediate values (less than 0 or more than 255)",
    6: "Misuse of labels as variables or vice-versa",
    7: "Variables not declared at the beginning",
    8: "Missing hlt instruction",
    9: "hlt not being used as the last instruction",
    10: "Wrong syntax used for instructions (For example, add instruction being used as a type B instruction )"
}

try:
    import sys

    complete_input = sys.stdin.readlines()
    code_input = []
    for string in complete_input:
        code_input.append(string.split())

    label_dict = {}
    var_dict = {}


    def check_name(s):
        if (s in opcode or s == 'var' or s in registers):
            return False
        if s.isnumeric():
            return False
        for i in s:
            if not (i.isalnum() or i == '_'):
                return False
        return True


    while ([] in code_input):
        code_input.remove([])

    if len(code_input) > 256:
        print("Max_Instructions.... Memory Overflow (instructions > 256)")
        exit()

    PC = 0
    for i in range(0, len(code_input) - 1):
        PC += 1
        if ('hlt' in code_input[i]):
            print(error_type[9])
            print("Error in Line - ", PC)
            exit()

    if ('hlt' not in code_input[-1]):
        print(error_type[8])
        exit()

    count = 0
    for i in code_input:
        if ('var' not in i):
            count += 1

    c = 0
    PC = 0
    for i in code_input:
        PC += 1
        if ('var' in i):
            if check_name(i[i.index('var') + 1]):
                if (i[i.index('var') + 1] not in var_dict):
                    b = bin(count + c)
                    b = b[2:len(b)]
                    b = '0' * (8 - len(b)) + b
                    var_dict[i[i.index('var') + 1]] = b
                    c += 1
                else:
                    print("Variable name can not be redifined")
                    print("Error in Line - ", PC)
                    exit()

            else:
                print("Wrong Syntax for Variable Name")
                print("Error in Line - ", PC)
                exit()

    PC = 0
    for i in range(0, len(code_input)):
        PC += 1
        if (':' in code_input[i][0]):
            if (check_name(code_input[i][0][0:-1])):
                if (code_input[i][0][0:-1] not in label_dict):
                    b = bin(i - c)
                    b = b[2:len(b)]
                    b = '0' * (8 - len(b)) + b
                    if (b in label_dict.keys()):
                        print("Two Labels name can not be defined at same memory location")
                        print("Error in Line - ", PC)
                        exit()
                    label_dict[code_input[i][0][0:-1]] = b
                else:
                    print("Label name can not be redifined")
                    print("Error in Line - ", PC)
                    exit()

            else:
                print("Wrong Syntax for Label Name")
                print("Error in Line - ", PC)
                exit()

    ins = False
    PC = 0
    for i in code_input:
        PC += 1
        for j in opcode:
            if j in i:
                ins = True
        if ('var' in i):
            if (ins):
                print(error_type[7])
                print("Error in Line - ", PC)
                exit()

    machine_code = []
    PC = 0
    for i in code_input:
        PC += 1
        instruction = ''
        if ('add' in i):
            op = 'add'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 4 or index > 1):
                print("Illegeal syntax for add operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers and i[index + 2] in registers and i[index + 3] in registers):
                instruction += un_used + registers[i[index + 1]] + registers[i[index + 2]] + registers[i[index + 3]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 2] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 3] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()

        elif ('sub' in i):
            op = 'sub'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))

            if (len(i) != index + 4 or index > 1):
                print("Illegeal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers and i[index + 2] in registers and i[index + 3] in registers):
                instruction += un_used + registers[i[index + 1]] + registers[i[index + 2]] + registers[i[index + 3]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 2] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 3] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()

        elif ('mul' in i):
            op = 'mul'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 4 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers and i[index + 2] in registers and i[index + 3] in registers):
                instruction += un_used + registers[i[index + 1]] + registers[i[index + 2]] + registers[i[index + 3]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 2] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 3] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()

        elif ('xor' in i):
            op = 'xor'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 4 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers and i[index + 2] in registers and i[index + 3] in registers):
                instruction += un_used + registers[i[index + 1]] + registers[i[index + 2]] + registers[i[index + 3]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 2] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 3] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()

        elif ('or' in i):
            op = 'or'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 4 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers and i[index + 2] in registers and i[index + 3] in registers):
                instruction += un_used + registers[i[index + 1]] + registers[i[index + 2]] + registers[i[index + 3]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 2] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 3] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()

        elif ('and' in i):
            op = 'and'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 4 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers and i[index + 2] in registers and i[index + 3] in registers):
                instruction += un_used + registers[i[index + 1]] + registers[i[index + 2]] + registers[i[index + 3]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 2] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 3] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()

        elif ('cmp' in i):
            op = 'cmp'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 3 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers and i[index + 2] in registers):
                instruction += un_used + registers[i[index + 1]] + registers[i[index + 2]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 2] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()

        elif ('not' in i):
            op = 'not'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 3 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers and i[index + 2] in registers):
                instruction += un_used + registers[i[index + 1]] + registers[i[index + 2]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 2] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()

        elif ('div' in i):
            op = 'div'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 3 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers and i[index + 2] in registers):
                instruction += un_used + registers[i[index + 1]] + registers[i[index + 2]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            elif (i[index + 2] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()

        elif ('ld' in i):
            op = 'ld'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 3 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers):
                instruction += un_used + registers[i[index + 1]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()
            mem = i[index + 2]
            if (mem in var_dict):
                instruction += var_dict[mem]
            elif (mem in label_dict):
                print(error_type[6])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Variable Name undefined")
                print("Error in Line - ", PC)
                exit()

        elif ('st' in i):
            op = 'st'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 3 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers):
                instruction += un_used + registers[i[index + 1]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()
            mem = i[index + 2]
            if (mem in var_dict):
                instruction += var_dict[mem]
            elif (mem in label_dict):
                print(error_type[6])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Variable Name undefined")
                print("Error in Line - ", PC)
                exit()


        elif ('jmp' in i):
            op = 'jmp'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            instruction += un_used
            if (len(i) != index + 2 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            mem = i[index + 1]
            if (mem in label_dict):
                instruction += label_dict[mem]
            elif (mem in var_dict):
                print(error_type[6])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Label Name undefined")
                print("Error in Line - ", PC)
                exit()


        elif ('jlt' in i):
            op = 'jlt'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            instruction += un_used
            if (len(i) != index + 2 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            mem = i[index + 1]
            if (mem in label_dict):
                instruction += label_dict[mem]
            elif (mem in var_dict):
                print(error_type[6])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Label Name undefined")
                print("Error in Line - ", PC)
                exit()

        elif ('jgt' in i):
            op = 'jgt'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            instruction += un_used
            if (len(i) != index + 2 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            mem = i[index + 1]

            if (mem in label_dict.keys()):
                instruction += label_dict[mem]
            elif (mem in var_dict):
                print(error_type[6])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Label Name undefined")
                print("Error in Line - ", PC)
                exit()

        elif ('je' in i):
            op = 'je'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            instruction += un_used
            if (len(i) != index + 2 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            mem = i[index + 1]
            if (mem in label_dict):
                instruction += label_dict[mem]
            elif (mem in var_dict):
                print(error_type[6])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Label Name undefined")
                print("Error in Line - ", PC)
                exit()

        elif ('rs' in i):
            op = 'rs'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 3 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers):
                instruction += un_used + registers[i[index + 1]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)

                exit()
            imm = i[index + 2]
            if (imm[0] == '$'):
                num = imm[1:]
                if (num.isnumeric() and int(num) >= 0 and int(num) < 256):
                    b = bin(int(num));
                    b = b[2:len(b)]
                    b = '0' * (8 - len(b)) + b;
                    instruction += b
                else:
                    print(error_type[5])
                    print("Error in Line - ", PC)
                    exit()
            else:
                print("Illegal syntax for immediate name")
                print("Error in Line - ", PC)
                exit()

        elif ('ls' in i):
            op = 'ls'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 3 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            if (i[index + 1] in registers):
                instruction += un_used + registers[i[index + 1]]
            elif (i[index + 1] == "FLAGS"):
                print(error_type[4])
                print("Error in Line - ", PC)
                exit()
            else:
                print("Illegal syntax for register name")
                print("Error in Line - ", PC)
                exit()

            imm = i[index + 2]
            if (imm[0] == '$'):
                num = imm[1:]
                if (num.isnumeric() and int(num) >= 0 and int(num) < 256):
                    b = bin(int(num))
                    b = b[2:len(b)]
                    b = '0' * (8 - len(b)) + b;
                    instruction += b
                else:
                    print(error_type[5])
                    print("Error in Line - ", PC)
                    exit()
            else:
                print("Illegal syntax for immediate name")
                print("Error in Line - ", PC)
                exit()

        elif ('hlt' in i):
            op = 'hlt'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 1 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            instruction += un_used

        elif ('mov' in i):
            op = 'mov'
            index = i.index(op)
            instruction = opcode[op][0]
            un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
            if (len(i) != index + 3 or index > 1):
                print("Illegal syntax for " + op + " operation")
                print("Error in Line - ", PC)
                exit()
            else:
                if (i[index + 1] in registers):
                    if (i[index + 2] in registers):
                        op = 'movr'
                        instruction = opcode[op][0]
                        un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
                        instruction += un_used + registers[i[index + 1]] + registers[i[index + 2]]

                    elif (i[index + 2] == "FLAGS"):
                        op = 'movr'
                        instruction = opcode[op][0]
                        un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
                        instruction += un_used + registers[i[index + 1]] + '111'

                    else:
                        op = 'movi'
                        instruction = opcode[op][0]
                        un_used = '0' * (11 - (opcode[op][1] * 3 + opcode[op][2] * 8 + opcode[op][3] * 8))
                        instruction += un_used + registers[i[index + 1]]
                        imm = i[index + 2]
                        if (imm[0] == '$'):
                            num = imm[1:]
                            if (num.isnumeric() and int(num) >= 0 and int(num) < 256):
                                b = bin(int(num))
                                b = b[2:len(b)]
                                b = '0' * (8 - len(b)) + b
                                instruction += b
                            else:
                                print(error_type[5])
                                print("Error in Line - ", PC)
                                exit()
                        else:
                            print("Illegal syntax for immediate name")
                            print("Error in Line - ", PC)
                            exit()
                else:
                    print("Illegal syntax for " + op + " operation")
                    print("Error in Line - ", PC)
                    exit()

        elif "var" in i:
            continue
        elif (len(instruction) != 16):
            print("Illegal instruction Syntax (General Syntax Error)")
            print("Error in Line - ", PC)
            exit()
        else:
            print("Illegal instruction Name (General Syntax Error)")
            print("Error in Line - ", PC)
            exit()
        machine_code.append(instruction)

    for i in machine_code:
        print(i)

except Exception:
    print("(General Syntax Error)")
