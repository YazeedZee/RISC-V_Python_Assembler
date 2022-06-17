# type i_1 and i_3 for instructions with funct3 and imm, i_3 for funct3 and shamt
# instruction : format:type
dic = {'lw': 'i_1', 'add': 'r', 'addi': 'i_1', 'lb': 'i_1', 'lh': 'i_1', 'lbu': 'i_1', 'lhu': 'i_1',
       'slli': 'i_3', 'srli': 'i_3', 'srai': 'i_3', 'sll': 'r', 'srl': 'r', 'sra': 'r', 'sub': 'r', 'xor': 'r',
       'or': 'r', 'and': 'r',
       'slt': 'r', 'sltu': 'r', 'xori': 'i_2', 'ori': 'i_2', 'andi': 'i_2', 'slti': 'i_2', 'sltiu': 'i_2', 'mul': 'r',
       'mulh': 'r',
       'mulhsu': 'r', 'mulhu': 'r', 'div': 'r', 'divu': 'r', 'rem': 'r', 'remu': 'r', 'sb': 's', 'sh': 's', 'sw': 's',
       'beq': 'sb', 'bne': 'sb', 'blt': 'sb', 'bge': 'sb', 'bltu': 'sb', 'bgeu': 'sb', 'lui': 'u', 'auipc': 'u',
       'jal': 'uj', 'jalr': 'uj'}

label = {}

# instruction : funct3
i_type_1 = {'op_code': '0000011', 'lw': '010', 'addi': '000', 'lb': '000', 'lh': '001', 'lbu': '100', 'lhu': '101'}
# instruction : funct3
i_type_2 = {'op_code': '0010011', 'xori': '100', 'ori': '110', 'andi': '111', 'slti': '010', 'sltiu': '011'}
# instruction : funct3,shamt
i_type_3 = (['op_code', '0010011'], ['slli', '001', '0000000'], ['srli', '101', '0000000'], ['srai', '101', '0100000'])
# instruction : :funct3,funct7
r_type = (['op_code', '0110011'], ['sll', '001', '0000000'], ['srl', '101', '0000000'], ['sra', '101', '0100000'],
          ['add', '000', '0000000'], ['sub', '000', '0100000'], ['xor', '100', '0000000'], ['or', '110', '0000000'],
          ['and', '111', '0000000'], ['slt', '010', '0000000'], ['sltu', '011', '0000000'], ['mul', '000', '0000001'],
          ['mulh', '001', '0000001'], ['mulhsu', '010', '0000001'], ['mulhu', '011', '0000001'],
          ['div', '100', '0000001'], ['divu', '101', '0000001'], ['rem', '110', '0000001'], ['remu', '111', '0000001'])
# instruction : funct3
s_type = {'op_code': '0100011', 'sb': '000', 'sh': '001', 'sw': '010'}
sb_type = {'op_code': '1100011', 'beq': '000', 'bne': '001', 'blt': '100', 'bge': '101', 'bltu': '110', 'bgeu': '111'}
u_type = {'op_code': '0110111', 'lui': 'no value', 'auipc': 'no value'}
uj_type = {'op_code': '1101111', 'jal': 'no value', 'jalr': 'no value'}

pc = 0
file = []
instructions = open('Bubble-Sort.txt')
result = open('result.txt.','w')
# the next "for loop" reads the file and saves all labels with their pc
for line in instructions:
    index_of_label = 0
    if line.count(':') > 0:
        index_of_label = line.index(":")
        label.update({line[:index_of_label]: pc})
        line = line[index_of_label + 1:]

    start = 0
    for q in line:
        #print(line)
        if q == ' ':
            line = line[start + 1:]
        else:
            break
    file.append(line)
    pc = pc + 1
#print(file)
#print(label)
#print(pc)

pc = 0  # restart the pc
args = ''
op = ''
op_code = ''
Type = ''
# the next "if" makes sure that every op is in the dic,otherwise it terminate the program, num 8 is number of types
if len(dic) != len(r_type) + len(i_type_1) + len(i_type_2) + len(i_type_3) + len(s_type) + len(sb_type) + len(
        u_type) + len(uj_type) - 8:
    for b in r_type[1:]:
        if dic.get(b[0], 'stop') == 'stop':
            print(b, 'is not found in dic')
    for b in i_type_1:
        if i_type_1.get(b) == "0000011":  # just to ignore the first element
            continue
        if dic.get(b, 'stop') == 'stop':
            print(b, 'is not in the dic')
    for b in i_type_2:
        if i_type_2.get(b) == '0010011':  # just to ignore the first element
            continue
        if dic.get(b, 'stop') == 'stop':
            print(b, 'is not in the dic')
    for b in i_type_3[1:]:
        if dic.get(b[0], 'stop') == 'stop':
            print(b, 'is not found in dic')
    for b in s_type:
        if s_type.get(b) == '0100011':  # just to ignore the first element
            continue
        if dic.get(b, 'stop') == 'stop':
            print(b, 'is not in the dic')
    for b in sb_type:
        if sb_type.get(b) == '1100011':  # just to ignore the first element
            continue
        if dic.get(b, 'stop') == 'stop':
            print(b, 'is not in the dic')
    exit()



# method for i/s type instructions, it creates the machine code for this instruction type
def i_type_1_2_method():
    rd_index = args.find(" ")
    rd = args[0:rd_index]
    if rd.find('x') >= 0:
        rd = rd.replace('x', '')
    rs1_before_conversion = args[rd_index + 1:]
    # assign the value of rs1 and imm if there's an offset. written as num1(num2)
    if rs1_before_conversion.find('(') > 0:
        start = rs1_before_conversion.index('(')
        end = rs1_before_conversion.index(')')
        rs1 = rs1_before_conversion[start + 1:end]  # rs1
        imm = rs1_before_conversion[:start]  # imm
        if rs1.find('x') >= 0:
            rs1 = rs1.replace('x', '')
        rs1 = int(rs1, 16)  # converts from hexadecimal to decimal
    # assign value of rs1 and imm if the values are separated, written as xXX, xYY
    else:
        sep = rs1_before_conversion.index(' ')
        rs1 = rs1_before_conversion[:sep]  # rs1
        imm = rs1_before_conversion[sep + 1:]  # imm
        rs1 = rs1.replace('x', '')
        imm = imm.replace('x', '')

    imm = bin(int(imm))[2:]
    rs1 = bin(int(rs1))[2:]
    rd = bin(int(rd))[2:]
    funct3 = ''
    # the next three "if statement" checks that each variable has the correct number of digits
    if len(rd) < 5:
        missing = 5 - len(rd)
        rd = missing * str(0) + rd
    if len(rs1) < 5:
        missing = 5 - len(rs1)
        rs1 = missing * str(0) + rs1
    if len(imm) < 12:
        missing = 12 - len(imm)
        imm = missing * str(0) + imm
    if Type == 'i_1':
        op_code = i_type_1.get('op_code')
        funct3 = i_type_1.get(op)
    if Type == 'i_2':
        op_code = i_type_2.get('op_code')
        funct3 = i_type_2.get(op)

    # else: op_code = i_type_2.get('op_code')
    # print('imm:', imm, 'rs1:', rs1, 'funct3:', funct3, 'rd:', rd, 'opcode:', op_code, end=' ### ')
    print(imm, rs1, funct3, rd, op_code, sep='')
    result.writelines(imm+ rs1+ funct3+ rd+ op_code+'\n')


# method for r/i_3 type instructions, it creates the machine code for this instruction type
def r_i_type_method():
    op_index = 0
    # this loop finds the index of the operation if its r type list
    if type == 'r':
        for x in r_type:
            if x[0] == op:
                break
            op_index = op_index + 1
    # this loop finds the index of the operation if its i type list
    else:
        for x in i_type_3:
            if x[0] == op:
                break
            op_index = op_index + 1
    separated = args.split()
    rd = separated[0].replace('x', '')
    rs1 = separated[1].replace('x', '')
    rs2 = separated[2].replace('x', '')
    rd = bin(int(rd))[2:]
    rs1 = bin(int(rs1))[2:]
    rs2 = bin(int(rs2))[2:]
    # the next three "if statement" checks that each variable has the correct number of digits
    if len(rd) < 5:
        missing = 5 - len(rd)
        rd = missing * str(0) + rd
    if len(rs1) < 5:
        missing = 5 - len(rs1)
        rs1 = missing * str(0) + rs1
    if len(rs2) < 5:
        missing = 5 - len(rs2)
        rs2 = missing * str(0) + rs2
    funct3 = '' #3-bits
    funct7 = '' #7-bits
    # for r type instructions, assign values of funct3 and funct7
    if dic.get(op) == 'r':
        op_code = r_type[0][1]
        funct3 = r_type[op_index][1]
        funct7 = r_type[op_index][2]
    # for i type instructions, assign values of funct3 and funct7
    else:
        op_code = i_type_3[0][1]
        funct3 = i_type_3[op_index][1]
        funct7 = i_type_3[op_index][2]
    # print('funct7:', funct7, 'rs2/shamt:', rs2, 'rs1:', rs1, 'funct3:', funct3, 'rd:', rd, 'opcode:', op_code,
    #       end=' ### ')
    print(funct7, rs2, rs1, funct3, rd, op_code, sep='')
    result.writelines(funct7+ rs2+ rs1+ funct3+ rd+ op_code+'\n')


# method for sb type instructions, it creates the machine code for this instruction type
def s_type_method():
    imm = ''
    rs1 = ''
    rs2_index = args.find(" ")
    #print(args)
   # print(rs2_index)
    rs2 = args[0:rs2_index]
    #print(rs2)
    if rs2.find('x') >= 0:
        rs2 = rs2.replace('x', '')
    rs1_before_conversion = args[rs2_index + 1:]  # rs1 + offset
    # assign the value of rs1 and imm if there's an offset. written as offset(rs1)
    if rs1_before_conversion.find('(') > 0:
        start = rs1_before_conversion.index('(')
        end = rs1_before_conversion.index(')')
        rs1 = rs1_before_conversion[start + 1:end]  # rs1
        imm = rs1_before_conversion[:start]  # imm
        if rs1.find('x') >= 0:
            rs1 = rs1.replace('x', '')
        rs1 = int(rs1, 16)  # converts from hexadecimal to decimal
    imm = bin(int(imm))[2:]
    rs1 = bin(int(rs1))[2:]
    rs2 = bin(int(rs2))[2:]

    if len(rs1) < 5:
        missing = 5 - len(rs1)
        rs1 = missing * str(0) + rs1
    if len(rs2) < 5:
        missing = 5 - len(rs2)
        rs2 = missing * str(0) + rs2
    if len(imm) < 12:
        missing = 12 - len(imm)
        imm = missing * str(0) + imm
    # print('imm[11:5]:', imm[0:7], 'rs2:', rs2, 'rs1:', rs1, 'funct3:', s_type.get(op), 'imm[4:0]:', imm[7:],
    #       'opcode:', s_type.get('op_code'), end=' ### ')
    print(imm[0:7], rs2, rs1, s_type.get(op), imm[7:], s_type.get('op_code'), sep='')
    result.writelines(imm[0:7]+rs2+rs1+s_type.get(op)+imm[7:]+s_type.get('op_code')+'\n')

# method for sb type instructions, it creates the machine code for this instruction type
def sb_type_method():
    imm = 0
    isNegative = False
    separated = args.split()
    #print(separated)
    rs1 = separated[0].replace('x', '')
    rs2 = separated[1].replace('x', '')
    branchTo = separated[2]  # branch to this label
    # assign the value of pc to branchTo
    for x in label:
        if x == branchTo:
            imm = (4 * label.get(x)) - (4 * pc)
    print(pc * 4, imm,label.get(x),label.get(x)*4)
    if imm < 0:
        isNegative = True
        imm = bin(int(imm))[3:]
    else:
        imm = bin(int(imm))[2:]
    rs1 = bin(int(rs1))[2:]
    rs2 = bin(int(rs2))[2:]

    if len(rs1) < 5:
        missing = 5 - len(rs1)
        rs1 = missing * str(0) + rs1
    if len(rs2) < 5:
        missing = 5 - len(rs2)
        rs2 = missing * str(0) + rs2
    # print(imm)
    # print(len(imm))
    if len(imm) < 13:
        missing = 13 - len(imm)
        imm = missing * str(0) + imm
    if isNegative:
        imm = list(imm)
        imm[0] = '1'
        print(imm)
        imm = "".join(imm)
    print(imm)
    # print('imm[12]:', imm[0], 'imm[10:5]:', imm[2:8], 'rs2', rs2, 'rs1', rs1, 'funct3', sb_type.get(op),
    #       'imm[4:1]:', imm[8:12], 'imm[11]', imm[1], 'opcode:', sb_type.get('op_code'), end=' ### ') # imm[0] is ignored
    print(imm[0], imm[2:8], rs2, rs1, sb_type.get(op), imm[8:12], imm[1], sb_type.get('op_code'), sep='')
    result.writelines(imm[0]+imm[2:8]+rs2+rs1+sb_type.get(op)+imm[8:12]+imm[1]+sb_type.get('op_code')+'\n')


# method for u type instructions, it creates the machine code for this instruction type
def u_type_method():
    imm = ''
    rd_index = args.find(" ")
    rd = args[0:rd_index]
    if rd.find('x') >= 0:
        rd = rd.replace('x', '')
    imm = args[rd_index + 1:]
    imm = imm[imm.find('x') + 1:]
    imm = int(imm, 16)  # converts from hexadecimal to decimal
    imm = bin(int(imm))[2:]
    rd = bin(int(rd))[2:]
    if len(rd) < 5:
        missing = 5 - len(rd)
        rd = missing * str(0) + rd
    if len(imm) < 20:
        missing = 20 - len(imm)
        imm = missing * str(0) + imm
    # print('imm[31:12]:',imm,'rd:',rd,'opcode:',u_type.get('op_code'),end=' ### ')
    print(imm, rd, u_type.get('op_code'), sep='')
    result.writelines(imm+rd+ u_type.get('op_code')+'\n')


# method for uj type instructions, it creates the machine code for this instruction type
def uj_type_method():
    isNegative = False
    op_code = uj_type.get('op_code')
    imm = ''
    rd = ''
    rs1 = ''  # only used for 'jalr' instruction
    separated = args.split()
    rd = separated[0]
    rd = rd.replace('x', '')
    if op == 'jal':
        callee = separated[1]
        for x in label:
            if x == callee:
                imm = (4 * label.get(x)) - (4 * pc)  # compare current pc with the location of the label
        if imm < 0:  # if the label is before the current pc
            isNegative = True
            imm = bin(int(imm))[3:]  # this number is negative
        else:  # if the label is after the current pc
            imm = bin(int(imm))[2:]
    else:  # for 'jalr' op
        start = separated[1].index('(')
        end = separated[1].index(')')
        rs1 = separated[1][start + 1:end]  # rs1
        imm = separated[1][:start]  # imm
        if rs1.find('x') >= 0:
            rs1 = rs1.replace('x', '')
        imm = bin(int(imm))[2:]
    imm_length = 21  # imm length is for jal as default
    if op == 'jalr':
        imm_length = 12
        rs1 = bin(int(rs1))[2:]
    rd = bin(int(rd))[2:]
    if len(rs1) < 5:
        missing = 5 - len(rs1)
        rs1 = missing * str(0) + rs1
    if len(rd) < 5:
        missing = 5 - len(rd)
        rd = missing * str(0) + rd
    if len(imm) < imm_length:
        missing = imm_length - len(imm)
        imm = missing * str(0) + imm
    if op == 'jal':
        if isNegative:
            imm = list(imm)
            imm[0] = '1'
            imm = "".join(imm)
        # print('imm[20]:',imm[0],'imm[10:1]:',imm[10:20],'imm[11]:',imm[9],'imm[19:12]:',imm[1:9],
        # 'rd:',rd,'opcode:',op_code,end=' ### ')
        print(imm[0], imm[10:20], imm[9], imm[1:9], rd, op_code, sep='')
    else:
       # print('imm:', imm, 'rs1', rs1, 'funct3', '000', 'rd', rd, 'opcode:', op_code, end=' ### ')
        print(imm, rs1, '000', rd, op_code, sep='')
        result.writelines(imm+rs1+'000'+rd+op_code+'\n')






# the next "for loop" is to extract an operation and its arguments and store each of them in different variables
for line in file:
    #print(line)
    no_comma = line.replace(',', ' ')  # replaces each every comma with a blank space
    #print(no_comma)
    first_word_index = no_comma.find(' ')  # find the index of the operation
    #print(first_word_index)
    op = no_comma[0:first_word_index]  # this variable contains the operation of each line
    #print(op)
    args_index = no_comma[first_word_index + 1:]  # the arguments for the operations
    #print(args_index)
    # print(op, end=' ')
    # check if the op is valid, return stop if not.
    if dic.get(op, 'stop') == 'stop':
        print('error: instruction not found in dictionary')
        exit()  # terminate the program
    Type = dic.get(op)  # saves the type of the operation
    # print(Type, end='    ')
    args = ''  # delete previous value
    # store all arguments in string "args" and makes sure there's no comments

    for word in args_index.split():
        #print(word)
        if (word == '//') or (0 <= word.find('//')):  # check if there's a comment
            break  # break the loop to go to the next line if instructions
        args = args + word + " "  # store a string with no comments
    #print(args, end='')
    #print('')  # new line

    if dic.get(op) == 'i_1':
        i_type_1_2_method()
    if dic.get(op) == 'i_2':
        i_type_1_2_method()
    if dic.get(op) == 'i_3':
        r_i_type_method()  # calling r_type_method because both types use rd,rs1 and rs2/shamt
    if dic.get(op) == 'r':
        r_i_type_method()
    if dic.get(op) == 's':
        s_type_method()
    if dic.get(op) == 'sb':
        sb_type_method()
    if dic.get(op) == 'u':
        u_type_method()
    if dic.get(op) == 'uj':
        uj_type_method()
    pc = pc + 1

#print(pc)
print(label)