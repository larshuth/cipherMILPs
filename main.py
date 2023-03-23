import cipher
import generateConstraints as gc
import cipher as cip
import visualization as vis

DEBUG = True


def main(rounds, cipher, viz):
    '''
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
    '''
    if viz == 1:
        vis.matplotlibvis(rounds, cipher)
    elif viz == 2:
        vis.gen_pdf(rounds, cipher)

def safe_call():
    try:
        # Asking the user what to generate
        print("Do you want to see the matrix structures in detail(1) oder generate a pdf(2)?")
        viz = int(input())
        print("How many rounds do you want to generate?")
        rounds = int(input())

        # generalizing the cipher question for the possible addition of more ciphers
        cipher_question = "Which cipher do you want to use? "
        for index, cipher in enumerate(cip.AVAILABLE):
            cipher_question += " %s (%s)" % (
                cipher.__name__, index) + " or"  # Adds e.g. "SKINNY-128 (1)" to the list of all options
        cipher_question = cipher_question[:-3] + "?"

        print(cipher_question)
        ciphelp = int(input())
        chosen_cipher = cip.AVAILABLE[ciphelp]

        main(rounds, chosen_cipher, viz)
    except Exception as e:
        print('\n\n!!! Error in input, restart script !!!\n\n')
        print(e)
    return

if __name__ == "__main__":
    if DEBUG:
        rounds, chosen_cipher, viz = 1, cip.Enocoro, 1
        main(rounds, chosen_cipher, viz)
    else:
        safe_call()
