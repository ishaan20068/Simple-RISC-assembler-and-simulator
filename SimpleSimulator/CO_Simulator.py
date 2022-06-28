import sys
import matplotlib.pyplot as plt

memory=["0000000000000000"]*256#this list represents the 512 byte memory
#for bonus
memory_access = []
special_access = []
special_cycle = []
cycle = []

PC=0#this variable represents the program counter

RF={"000":"0000000000000000",
    "001":"0000000000000000",
    "010":"0000000000000000",
    "011":"0000000000000000",
    "100":"0000000000000000",
    "101":"0000000000000000",
    "110":"0000000000000000",
    "111":"0000000000000000"}#this dictionary represents the register file

#this is a helper function for loading the input into memory
def loadmemory(inputlist):
    for i in range(len(inputlist)):
        memory[i]=inputlist[i]
#################################################

#this function represents the execution engine
def execution_engine(x):
    return(memory[x])
#################################################

#below function gives the string that contains current state of PC and registers
def state():
    s=bin(PC)
    s=s[2:]
    s=(8-len(s))*"0"+s
    for i in RF:
        s+=" "
        s+=RF[i]
    return s
#####################################################

def execute(instruction):
    global PC
    opcode=instruction[0:5]
    #below case is for halt
    if opcode=="10011":
        RF["111"]="0000000000000000"
        print(state())
        return -1;
    
    #below case is for jump instructions or memory address type instructions
    elif opcode=="01111" or opcode=="10000" or opcode=="10001" or opcode=="10010":
        memory_address=instruction[-8:]
        memory_address=int(memory_address,2)
        if opcode=="01111":
            RF["111"]="0000000000000000"
            print(state())
            PC=memory_address
        elif opcode=="10000":
            if RF["111"]=="0000000000000100":
                RF["111"]="0000000000000000"
                print(state())
                PC=memory_address
            else:
                RF["111"]="0000000000000000"
                print(state())
                PC+=1
        elif opcode=="10001":
            if RF["111"]=="0000000000000010":
                RF["111"]="0000000000000000"
                print(state())
                PC=memory_address
            else:
                RF["111"]="0000000000000000"
                print(state())
                PC+=1
        elif opcode=="10010":
            if RF["111"]=="0000000000000001":
                RF["111"]="0000000000000000"
                print(state())
                PC=memory_address
            else:
                RF["111"]="0000000000000000"
                print(state())
                PC+=1
    
    #below case is for register and memory type instructions
    elif opcode=="00101" or opcode=="00100":
        memory_address=instruction[-8:]
        memory_address=int(memory_address,2)
        special_access.append(memory_address)
        special_cycle.append(cycle_num - 1)
        if opcode=="00100":
            RF["111"]="0000000000000000"
            data=memory[memory_address]
            register=instruction[5:8]
            RF[register]=data
            print(state())
            PC+=1
        else:
            register=instruction[5:8]
            data=RF[register]
            memory[memory_address]=data
            RF["111"]="0000000000000000"
            print(state())
            PC+=1
    
    #below case is for 2 register type instructions
    elif opcode=="01101" or opcode=="01110" or opcode=="00111" or opcode=="00011":
        reg1=instruction[-6:-3]
        reg2=instruction[-3:]
        if opcode=="00011":
            RF[reg1]=RF[reg2]
            RF["111"]="0000000000000000"
            print(state())
            PC+=1
        elif opcode=="00111":
            value1=int(RF[reg1],2)
            value2=int(RF[reg2],2)
            quotient=value1//value2
            remainder=value1%value2
            quotient=bin(quotient)
            quotient=quotient[2:]
            quotient = "0"*(16-len(quotient))+quotient
            remainder=bin(remainder)
            remainder=remainder[2:]
            remainder="0"*(16-len(remainder))+remainder
            RF["000"]=quotient
            RF["001"]=remainder
            RF["111"]="0000000000000000"
            print(state())
            PC+=1
        elif opcode=="01101":
            value=RF[reg2]
            value=value.replace("1","x")
            value=value.replace("0","1")
            value=value.replace("x","0")
            RF[reg1]=value
            RF["111"]="0000000000000000"
            print(state())
            PC+=1
        else:
            value1=int(RF[reg1],2)
            value2=int(RF[reg2],2)
            if value1>value2:
                RF["111"]="0000000000000010"
            elif value1==value2:
                RF["111"]="0000000000000001"
            elif value1<value2:
                RF["111"]="0000000000000100"
            print(state())
            PC+=1
    
    #below case is for register and immediate type instructions
    elif opcode=="00010" or opcode=="01000" or opcode=="01001":
        immediate=instruction[-8:]
        reg1=instruction[5:8]
        if opcode=="00010":
            RF[reg1]="00000000"+immediate
            RF["111"]="0000000000000000"
            print(state())
            PC+=1
        elif opcode=="01000":
            bits = int(immediate,2);
            RF[reg1]=RF[reg1][:-bits]
            RF[reg1]='0'*(16-len(RF[reg1])) + RF[reg1]
            RF["111"]="0000000000000000"
            print(state())
            PC+=1
        else:
            bits = int(immediate,2);
            RF[reg1] = RF[reg1] + '0'*bits
            RF[reg1]=RF[reg1][-16:]
            RF["111"]="0000000000000000"
            print(state())
            PC+=1
    
    #below case if for type A instructions
    else:
        reg1=instruction[7:10]
        reg2=instruction[10:13]
        reg3=instruction[13:]
        if opcode=="00000":
            value1=int(RF[reg2],2)
            value2=int(RF[reg3],2)
            RF["111"]="0000000000000000"
            value=value2+value1
            value=bin(value)
            value=value[2:]
            if len(value)>16:
                RF["111"]="0000000000001000"
                value=value[-16:]
            value="0"*(16-len(value))+value
            RF[reg1]=value
            print(state())
            PC+=1
        elif opcode=="00001":
            value1=int(RF[reg2],2)
            value2=int(RF[reg3],2)
            RF["111"]="0000000000000000"
            value=value1-value2
            if value<0:
                RF["111"]="0000000000001000"
                value=0
            value=bin(value)
            value=value[2:]
            value="0"*(16-len(value))+value
            RF[reg1]=value
            print(state())
            PC+=1
        elif opcode=="00110":
            value1=int(RF[reg2],2)
            value2=int(RF[reg3],2)
            RF["111"]="0000000000000000"
            value=value1*value2
            value=bin(value)
            value=value[2:]
            if len(value)>16:
                RF["111"]="0000000000001000"
                value=value[-16:]
            value="0"*(16-len(value))+value
            RF[reg1]=value
            print(state())
            PC+=1
        elif opcode=="01010":
            value1=int(RF[reg2],2)
            value2=int(RF[reg3],2)
            RF["111"]="0000000000000000"
            value=value1^value2
            value=bin(value)
            value=value[2:]
            value="0"*(16-len(value))+value
            RF[reg1]=value
            print(state())
            PC+=1
        elif opcode=="01011":
            value1=int(RF[reg2],2)
            value2=int(RF[reg3],2)
            RF["111"]="0000000000000000"
            value=value1|value2
            value=bin(value)
            value=value[2:]
            value="0"*(16-len(value))+value
            RF[reg1]=value
            print(state())
            PC+=1
        else:
            value1=int(RF[reg2],2)
            value2=int(RF[reg3],2)
            RF["111"]="0000000000000000"
            value=value1&value2
            value=bin(value)
            value=value[2:]
            value="0"*(16-len(value))+value
            RF[reg1]=value
            print(state())
            PC+=1

if __name__=="__main__":
    #this segment inputs and loads the memory with binary instructions
    complete_input = sys.stdin.readlines()
    binary_code_input = []
    for string in complete_input:
        if string[-1]=="\n":
            binary_code_input.append(string[0:-1])
        else:
            binary_code_input.append(string)
    loadmemory(binary_code_input)
    #########################################################
    cycle_num = 0
    #this segment is actually running the code
    while True:
        instruction=execution_engine(PC)
        #saving for bonus-------
        memory_access.append(PC)
        cycle.append(cycle_num)
        cycle_num += 1
        #-----------------------
        if(execute(instruction)==-1):
            break
    for data in memory:
        print(data)

# bonus plotting
    plt.scatter(cycle, memory_access, c='red', edgecolors='black')
    plt.scatter(special_cycle, special_access, c='red', edgecolors='black')
    font = {'family': 'serif', 'color': 'blue', 'size': 12}
    plt.title("Memory Access v/s Cycles")
    plt.xlabel("Cycle Number", fontdict=font)
    plt.ylabel("Memory Address (in base10)", fontdict=font)
    plt.show()
    plt.savefig("Result.png")
