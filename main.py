import generateConstraints as gc
import cipher as cip
import visualization as vis


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


if __name__ == "__main__":
    print("Do you want to see the matrix structures in detail(1) oder generate a pdf(2)?")
    viz = int(input())
    print("How many rounds do you want to generate?")
    rounds = int(input())
    print("Which cipher do you want to use? AES(1) or Enocoro(2)?")
    ciphelp = int(input())
    if ciphelp == 1:
        cipher = cip.Aes
    else:
        cipher = cip.Enocoro
    main(rounds, cipher, viz)

###### Structure #####

# def aes(....)
#   matrix = generateConstraints( dummy, rounds, variablesPerRound, shift )

# def enocoro(....)
#   matrix = generateConstraints( dummy, rounds, variablesPerRound, shiftBit )


# def generateConstraints( dummy, rounds, variablesPerRound, function="" )
#  Code for one round
#  After each round, execute function, e.g. shift or shiftBit
#  if function != ""
#       func = getattr(, function)
#       
#       func(matrix)
