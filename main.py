import visualization as vis
from cipher.differential.aes import Aes as AesDifferential
from cipher.differential.lblock import LBlock as LBlockDifferential
from cipher.differential.gift import Gift64 as Gift64Differential
from cipher.linear.aes import Aes as AesLinear
from cipher.linear.lblock import LBlock as LBlockLinear
from cipher.linear.gift import Gift64 as Gift64Linear

DEBUG = False

AVAILABLE = [AesDifferential, LBlockDifferential, Gift64Differential, AesLinear, LBlockLinear]
BIT_ORIENTED = [AesDifferential, LBlockDifferential, Gift64Differential, AesLinear, LBlockLinear, Gift64Linear]


def main(rounds, cipher, viz, bit_oriented, chosen_type):
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
        return vis.no_viz_just_testrun(rounds, cipher, bit_oriented, chosen_type)
    elif viz == 1:
        vis.matplotlibvis(rounds, cipher, bit_oriented, chosen_type)
    elif viz == 2:
        vis.gen_pdf(rounds, cipher, bit_oriented, chosen_type)
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

        print(
            'choose a type of modelling: "SunEtAl 2013",  "SunEtAl 2013 Greedy", "SunEtAl with 2013 Baksi extension 2020", "SunEtAl 2013 with Baksi extension 2020 Greedy", "Baksi 2020", and "Boura 2020 Algo 2"')
        while True:
            chosen_type = input()
            if chosen_type not in {"SunEtAl 2013", "SunEtAl 2013 Greedy", "SunEtAl with 2013 Baksi extension 2020",
                                   "SunEtAl 2013 with Baksi extension 2020 Greedy", "Baksi 2020", "Boura 2020 Algo 2"}:
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
    for cipher in [LBlockDifferential, Gift64Differential, LBlockLinear, Gift64Linear, AesLinear, AesDifferential]:
        for type in ["Baksi 2020", "Boura 2020 Algo 2", "SunEtAl 2013", "SunEtAl 2013 Greedy",
                     "SunEtAl 2013 with Baksi extension 2020", "SunEtAl 2013 with Baksi extension 2020 Greedy"]:
            try:
                main(2, cipher, viz, True, type)
            except:
                print(2, cipher, viz, True, type, "Failed")
    return


def generate_rijndael_convex_hull():
    rounds, chosen_cipher, viz, bit_oriented, chosen_type = 3, AesDifferential, 1, True, "SunEtAl 2013"
    main(rounds, chosen_cipher, viz, bit_oriented, chosen_type)
    return


def rearrange_matrix():
    rounds, chosen_cipher, bit_oriented, chosen_type = 2, LBlockDifferential, True, "SunEtAl 2013"
    vis.rearrange(rounds, chosen_cipher, bit_oriented, chosen_type)
    return


if __name__ == "__main__":
    if DEBUG:
        rounds, chosen_cipher, viz, bit_oriented, chosen_type = 2, LBlockDifferential, 1, True, "SunEtAl 2013 with Baksi extension 2020"
        main(rounds, chosen_cipher, viz, bit_oriented, chosen_type)
    else:
        rearrange_matrix()
