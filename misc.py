import multiprocessing


def branch_number_to_x_val(input_val):
    global branch_number_after_last_rounds

    print(input_val)
    input_bitstring = format(input_val, 'b').rjust(32, '0')
    input_1s = input_bitstring.count("1")

    # for efficiency's sake we stop if a lower branch number is impossible
    if input_1s > branch_number_after_last_rounds:
        return branch_number_after_last_rounds

    def bit_to_int(x):
        return int(x, 2)
    input_list = [bit_to_int(input_bitstring[i * 8:(i + 1) * 8]) for i in range(4)]
    output_list = [2 * input_list[0] + 3 * input_list[1] + 1 * input_list[2] + 1 * input_list[3],
                   1 * input_list[0] + 2 * input_list[1] + 3 * input_list[2] + 1 * input_list[3],
                   1 * input_list[0] + 1 * input_list[1] + 2 * input_list[2] + 3 * input_list[3],
                   3 * input_list[0] + 1 * input_list[1] + 1 * input_list[2] + 2 * input_list[3]]
    output_bitstring = format(output_list[0], 'b') + format(output_list[1], 'b') + format(output_list[2], 'b') + format(
        output_list[3], 'b')
    output_1s = output_bitstring.count('1')
    return input_1s + output_1s


def calculate_Aes_MixCoumns_branch_number():
    global branch_number_after_last_rounds

    branch_number = 2 ** (4*8)
    input_vals = list(range(1, (2 ** 10)))

    with multiprocessing.Pool(8) as p:
        all_numbers = p.map(branch_number_to_x_val, input_vals)
    branch_number = min(branch_number, min(all_numbers))

    # can be improved significantly by going over all pairs by ascending number of active bits and going until a first
    # one is reached
    for i in range(1, (2**(4*8) // (2**10)) + 1):
        input_vals = list(range(i*(2**10), (i+1)*(2**10)))
        with multiprocessing.Pool(8) as p:
            all_numbers = p.map(branch_number_to_x_val, input_vals)
        branch_number = min(branch_number, min(all_numbers))
        branch_number_after_last_rounds = branch_number
    return branch_number


def blocks_to_matrices(inequalities):
    for multipliers, _, _ in inequalities:
        string = ''
        for index, m in enumerate(multipliers):
            if m == 0:
                string += ' & '
            else:
                string += f'\\Block[fill=darkteal]{{1-1}}{{\\color{{white}} {m} }} &'
            if index == 3:
                string += '&'
            elif index == 7:
                string = string[:-1] + '\\\\'
        print(string)
    return None


# branch_number_after_last_rounds = 2**(4*8)
# bn = calculate_Aes_MixCoumns_branch_number()
# print('Branch Number of bit-oriented Aes =', bn)

