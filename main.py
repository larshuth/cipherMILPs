import visualization as vis
from cipher.differential.enocoro import Enocoro as EnocoroDifferential
from cipher.differential.aes import Aes as AesDifferential
from cipher.differential.lblock import LBlock as LBlockDifferential
from cipher.differential.gift import Gift64 as Gift64Differential
from cipher.linear.enocoro import Enocoro as EnocoroLinear
from cipher.linear.aes import Aes as AesLinear
from cipher.linear.lblock import LBlock as LBlockLinear

DEBUG = True

AVAILABLE = [AesDifferential, LBlockDifferential, Gift64Differential, AesLinear, LBlockLinear]
BIT_ORIENTED = [AesDifferential, LBlockDifferential, Gift64Differential, AesLinear, LBlockLinear]


def main(rounds, cipher, viz, bit_oriented):
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
        return vis.no_viz_just_testrun(rounds, cipher, bit_oriented)
    elif viz == 1:
        vis.matplotlibvis(rounds, cipher, bit_oriented)
    elif viz == 2:
        vis.gen_pdf(rounds, cipher, bit_oriented)
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
                if viz not in set(range(len(AVAILABLE))):
                    print("I like the spirit but that is not a number corresponding with one of the ciphers. Try again, fool.")
                else:
                    break
            except ValueError:
                print("I like the spirit but that is not a number. Try again, fool.")

        chosen_cipher = AVAILABLE[ciphelp]
        if chosen_cipher in BIT_ORIENTED:
            print("Would you like to model the cipher bit-oriented (0) or word/byte-oriented (1)?")
            while True:
                try:
                    bit_oriented = bool(int(input()))
                    if bit_oriented not in {0, 1}:
                        print(
                            "I like the spirit but that is not a 0 or 1. Try again, fool.")
                    else:
                        break
                except ValueError:
                    print("I like the spirit but that is not a number. Try again, fool.")

        main(rounds, chosen_cipher, viz, bit_oriented)
    except Exception as e:
        print('\n\n!!! Error in input, restart script !!!\n\n')
        print(e)
    return


if __name__ == "__main__":
    if DEBUG:
        rounds, chosen_cipher, viz, bit_oriented = 1, Gift64Differential, 2, True
        main(rounds, chosen_cipher, viz, bit_oriented)
    else:
        safe_call()
