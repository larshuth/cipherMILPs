import generateConstraints as gc
import visualizeMatrices as vism
import cipher as cip
import visualization as vis



def main (rounds, cipher, viz):
    '''
    Examines the structures of constraint matrices for given ciphers by generating constraints, the corresponding matrices and trying different sorting techniques.

    Parameters:
    -----------
    rounds      :   int
                    Number of rounds used for network
    
    ciphers     :   list of strings
                    Indicates the names of the ciphers used for the encryption
    
    constraints :   list of strings
                    Indicates the names of the methods used to generate the constraints
    
    structures  :   list
                    Indicates the names of the functions used to examine the structures of the constraint matrices

    dir         :   string
                    The name of the directory in which the results should be saved

    Returns:
    ----------
                :   files
                    Contains the constraints as a string and corresponding structured constraint matrices as tikz code (??)
    '''
    if viz == 1:
        vis.matplotlibvis(rounds, cipher)
    elif viz == 2:
        vis.gen_pdf(cipher, rounds) #UNGREGELMÄ?GITEIT FIXEN
    """
    # For every used cipher repeat the following three steps
    for c in ciphers:
        cipher = getattr(cip, c) #-- should this be a function or just a parameter for the constraint generating function?

        # 1. Generate constraints and corresponding matrix 
        for constraint in constraints:
            
            generatedConstraints, matrix = cipher(constraint) 
            
            # Save constraints to file in given directory
            fileName = c + constraint + rounds + ".txt"
            #-- Add save to file
        
            #-- Question: how to properly store the matrices?

            # 2. Try different sorting techniques 
            for struc in structures:
                structure = getattr(vism, struc)
                structuredMatrix = structure(matrix)
        
                # 3. Save sorted matrix to file
                #-- Add save to file, ensure that the current content is not overwritten every time

"""

if __name__ == "__main__":
    print("Do you want to see the matrix structures in detail(1) oder generate a pdf(2)?")
    viz = int(input())
    print("How many rounds do you want to generate?")
    rounds = int(input())
    print("Which cipher do you want to use? AES(1) or Enocoro(2)?")
    ciphelp= int(input())
    if ciphelp == 1:
        cipher=cip.Aes
    else: cipher = cip.Enocoro
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
