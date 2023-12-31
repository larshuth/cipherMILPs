import visualization as vis
from cipher.differential.aes import Aes as AesDifferential
from cipher.differential.lblock import LBlock as LBlockDifferential
from cipher.differential.gift import Gift64 as Gift64Differential
from cipher.linear.aes import Aes as AesLinear
from cipher.linear.lblock import LBlock as LBlockLinear
from cipher.linear.gift import Gift64 as Gift64Linear

DEBUG = True

AVAILABLE = [AesDifferential, LBlockDifferential, Gift64Differential, AesLinear, LBlockLinear]
BIT_ORIENTED = [AesDifferential, LBlockDifferential, Gift64Differential, AesLinear, LBlockLinear, Gift64Linear]


def main(rounds, cipher, viz, bit_oriented, chosen_type, **kwargs):
    print(kwargs)
    """
    Examines the structures of constraint matrices for given ciphers by generating constraints, the corresponding matrices and trying different sorting techniques.

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

    if viz == 0:
        return vis.no_viz_just_testrun(rounds, cipher, bit_oriented, chosen_type, **kwargs)
    elif viz == 1:
        vis.matplotlibvis(rounds, cipher, bit_oriented, chosen_type, **kwargs)
    elif viz == 2:
        vis.gen_pdf(rounds, cipher, bit_oriented, chosen_type, **kwargs)
    return


def safe_call():
    try:
        # Asking the user what to generate
        print("Do you want to see the matrix structures in detail(1) oder generate a pdf(2)?")
        while True:
            try:
                viz = int(input())
                if viz not in {1, 2}:
                    print("I like the spirit but that is not a 1 or 2. Try again, fool.")
                else:
                    break
            except ValueError:
                print("I like the spirit but that is not a number. Try again, fool.")
        print("How many rounds do you want to generate?")
        while True:
            try:
                rounds = int(input())
                if rounds < 1:
                    print("Not enough rounds. Try again, fool.")
                else:
                    break
            except ValueError:
                print("I like the spirit but that is not a number. Try again, fool.")

        # generalizing the cipher question for the possible addition of more ciphers
        cipher_question = "Which cipher do you want to use? "
        for index, cipher in enumerate(AVAILABLE):
            cipher_question += " %s (%s)" % (
                cipher.__name__, index) + " or"  # Adds e.g. "SKINNY-128 (1)" to the list of all options
        cipher_question = cipher_question[:-3] + "?"

        print(cipher_question)
        while True:
            try:
                ciphelp = int(input())
                if ciphelp not in set(range(len(AVAILABLE))):
                    print(
                        "I like the spirit but that is not a number corresponding with one of the ciphers. Try again, fool.")
                else:
                    break
            except ValueError:
                print("I like the spirit but that is not a number. Try again, fool.")

        chosen_cipher = AVAILABLE[ciphelp]
        available_modelings = {"Baksi 2020", "Boura 2020 Algo 2", "SunEtAl 2013", "SunEtAl 2013 Greedy",
                     "Logical condition modeling", "Exclusion of impossible transitions"}
        if chosen_cipher in BIT_ORIENTED:
            print("Would you like to model the cipher word/byte-oriented (0) or bit-oriented (1)?")
            while True:
                try:
                    bit_oriented = int(input())
                    if bit_oriented not in {0, 1}:
                        print(
                            "I like the spirit but that is not a 0 or 1. Try again, fool.")
                    else:
                        bit_oriented = bool(bit_oriented)
                        break
                except ValueError:
                    print("I like the spirit but that is not a number. Try again, fool.")
        else:
            bit_oriented = False

        print(f'choose a type of modelling: {available_modelings}')
        while True:
            chosen_type = input()
            if chosen_type not in available_modelings:
                print('try again')
            else:
                break
    except Exception as e:
        print(e)
        raise Exception('!!! Error in input, restart script!!!')

    main(rounds, chosen_cipher, viz, bit_oriented, chosen_type)
    return


def generate_all_visualizations():
    viz = 1
    for cipher in [LBlockDifferential, Gift64Differential, LBlockLinear, Gift64Linear]:
        for type in ["Baksi 2020", "Boura 2020 Algo 2", "SunEtAl 2013", "SunEtAl 2013 Greedy",
                     "Logical condition modeling", "Exclusion of impossible transitions"]:
            try:
                main(2, cipher, viz, True, type)
            except:
                print(2, cipher, viz, True, type, "Failed")
    return


def generate_rijndael_convex_hull():
    rounds, chosen_cipher, viz, bit_oriented, chosen_type = 1, AesDifferential, 1, True, "Baksi 2020"
    main(rounds, chosen_cipher, viz, bit_oriented, chosen_type)
    return


def rearrange_matrix():
    arguments = {'rounds': 4,
                 'cipher': LBlockLinear,
                 'viz': 1,
                 'bit_oriented': True,
                 'chosen_type': "Logical condition modeling"}

    keyworded_arguments_for_ciphers = {"overwrite_equals": True,
                                       "permutation_as_constraints": True}
    vis.rearrange(**arguments, **keyworded_arguments_for_ciphers)
    return


if __name__ == "__main__":
    rearrange_matrix()

    # if DEBUG:
    #     arguments = {'rounds': 4,
    #                  'cipher': LBlockLinear,
    #                  'viz': 1,
    #                  'bit_oriented': True,
    #                  'chosen_type': "Logical condition modeling"}
    #
    #     keyworded_arguments_for_ciphers = {"overwrite_equals": False,
    #                                        "permutation_as_constraints": False}
    #     main(**arguments, **keyworded_arguments_for_ciphers)
    # else:
    #     safe_call()
