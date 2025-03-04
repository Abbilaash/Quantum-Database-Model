def dr_no_to_binary(dr_no, bit_size=28):
    return format(int(dr_no), f'0{bit_size}b')

print(dr_no_to_binary(250504051, 28))