import visualization
from cipher.differential.aes import Aes as AesDifferential
from cipher.differential.lblock import LBlock as LBlockDifferential
from cipher.differential.gift import Gift64 as Gift64Differential
from cipher.linear.aes import Aes as AesLinear
from cipher.linear.lblock import LBlock as LBlockLinear
from cipher.linear.gift import Gift64 as Gift64Linear

import visualization as vis
import generate_constraints as gc
import matplotlib.pyplot as plt

import pickle

DEBUG = True

AVAILABLE = [AesDifferential, LBlockDifferential, Gift64Differential, AesLinear, LBlockLinear]
BIT_ORIENTED = [AesDifferential, LBlockDifferential, Gift64Differential, AesLinear, LBlockLinear, Gift64Linear]


def retrieve_cipher(rounds, cipher, bit_oriented, chosen_type, **kwargs):
    title = [str(cipher)[15:-2], str(rounds)]
    filename = f'{title[0]}{title[1]}rounds_bitoriented_{str(bit_oriented)}_{chosen_type.replace(" ", "")}'
    filename += ''.join([f'{key}_{val}' for key, val in kwargs.items()])

    try:
        file = open(f'{filename}_matrix.pkl', 'rb')
        matrix = pickle.load(file)
        file.close()

        file = open(f'{filename}_variables.pkl', 'rb')
        variables = pickle.load(file)
        file.close()

        # TODO: add retrieving a cipher instance
        cipher_instance = None

    except FileNotFoundError:
        cipher_instance = gc.generate_constraints(rounds, cipher, bit_oriented, chosen_type, **kwargs)
        matrix = cipher_instance.M
        variables = cipher_instance.V

        file = open(f'{filename}_matrix.pkl', 'wb')
        pickle.dump(cipher_instance.M.copy(), file)
        file.close()

        file = open(f'{filename}_variables.pkl', 'wb')
        pickle.dump(cipher_instance.V.copy(), file)
        file.close()

    return matrix, variables, cipher_instance, filename


def __main__(arguments, keyworded_arguments_for_ciphers, create_visualization=False, sort_visualization=False,
             create_constraints_as_text=False, **kwargs):
    print(kwargs)
    """
    Examines the structures of constraint matrices for given ciphers by generating constraints, the corresponding 
    matrices and trying different sorting techniques.

    Parameters:
    -----------
    rounds      :   int
                    Number of rounds used for cipher

    cipher      :   class
                    Class that represents the wanted cipher

    viz         :   int
                    Indicates the desired visualization

    Returns:
    ----------
    Opens a new window or creates a new pdf file in the same directory of this file.
    """

    matrix, variables, cipher_instance, filename = gc.generate_constraints(**arguments,
                                                                           **keyworded_arguments_for_ciphers,
                                                                           **kwargs)
    if create_visualization:
        if sort_visualization:
            fig = vis.rearrange(**arguments, **keyworded_arguments_for_ciphers, **kwargs)
        else:
            fig = vis.matplotlibvis(**arguments, **keyworded_arguments_for_ciphers, **kwargs)
        fig.savefig(f"{filename}_sorted.png")
        plt.show()
        print("plot should have been shown")

    if create_constraints_as_text:
        constraint_text = visualization.generate_constraints_as_text(**arguments, **keyworded_arguments_for_ciphers,
                                                                     **kwargs)

    return cipher_instance


def terminal_user_input_call():
    try:
        # Asking the user what to generate
        print(
            "Do you want to see/generate the constraint matrix structure(1) or generate a list of all constraints(2)?\n")
        while True:
            try:
                viz = int(input())
                if viz not in {1, 2}:
                    print("I like the spirit but that is not a 1 or 2. Enter a valid Request.\n")
                else:
                    break
            except ValueError:
                print("I like the spirit but that is not a number. Enter a valid Request.\n")
        print("How many rounds do you want to generate?\n")
        while True:
            try:
                rounds = int(input())
                if rounds < 1:
                    print("Not enough rounds. Enter a valid Request.\n")
                else:
                    break
            except ValueError:
                print("I like the spirit but that is not a number. Enter a valid Request.\n")

        # generalizing the cipher question for the possible addition of more ciphers
        cipher_question = "Which cipher do you want to use? "
        for index, cipher in enumerate(AVAILABLE):
            cipher_question += " %s (%s)" % (
                cipher.__name__, index) + " or"  # Adds e.g. "SKINNY-128 (1)" to the list of all options
        cipher_question = cipher_question[:-3] + "?\n"

        print(cipher_question)
        while True:
            try:
                ciphelp = int(input())
                if ciphelp not in set(range(len(AVAILABLE))):
                    print(
                        "I like the spirit but that is not a number corresponding with one of the ciphers. Enter a valid Request.\n")
                else:
                    break
            except ValueError:
                print("I like the spirit but that is not a number. Enter a valid Request.\n")

        chosen_cipher = AVAILABLE[ciphelp]
        available_modelings = {"Baksi 2020", "Boura 2020 Algo 2", "SunEtAl 2013", "SunEtAl 2013 Greedy",
                               "Logical condition modeling", "Exclusion of impossible transitions"}
        if chosen_cipher in BIT_ORIENTED:
            print("Would you like to model the cipher word/byte-oriented (0) or bit-oriented (1)?\n")
            while True:
                try:
                    bit_oriented = int(input())
                    if bit_oriented not in {0, 1}:
                        print(
                            "I like the spirit but that is not a 0 or 1. Enter a valid Request.\n")
                    else:
                        bit_oriented = bool(bit_oriented)
                        break
                except ValueError:
                    print("I like the spirit but that is not a number. Enter a valid Request.\n")
        else:
            bit_oriented = False

        print(f'choose a type of modelling: {available_modelings}\n')
        while True:
            chosen_type = input()
            if chosen_type not in available_modelings:
                print('try again')
            else:
                break
    except Exception as e:
        print(e)
        raise Exception('!!! Error in input, restart script!!!')
    arguments = {'rounds': rounds,
                 'cipher': chosen_cipher,
                 'viz': viz,
                 'bit_oriented': bit_oriented,
                 'chosen_type': chosen_type}

    __main__(arguments=arguments, keyworded_arguments_for_ciphers={}, )
    return


def generate_all_visualizations():
    viz = 1
    for cipher in [LBlockDifferential, Gift64Differential, LBlockLinear, Gift64Linear]:
        for type in ["Baksi 2020", "Boura 2020 Algo 2", "SunEtAl 2013", "SunEtAl 2013 Greedy",
                     "Logical condition modeling", "Exclusion of impossible transitions"]:
            try:
                __main__(2, cipher, viz, True, type)
            except:
                print(2, cipher, viz, True, type, "Failed")
    return


def quick_code_input_call():
    arguments = {'rounds': 4,
                 'cipher': LBlockLinear,
                 'viz': 1,
                 'bit_oriented': True,
                 'chosen_type': "Logical condition modeling"}

    keyworded_arguments_for_ciphers = {"overwrite_equals": False,
                                       "permutation_as_constraints": False}
    cipher_instance = __main__(arguments=arguments, keyworded_arguments_for_ciphers=keyworded_arguments_for_ciphers)
    return cipher_instance


if __name__ == "__main__":
    if DEBUG:
        quick_code_input_call()
    else:
        terminal_user_input_call()
