import numpy as np
import matplotlib.pyplot as plt

filepath = 'originaldata.txt'

def export(filepath):
    '''
    Takes filepath of included file of dataset used in McQuillan et al. 2014
    and extracts mass and rotation periods of each object and places them in 
    another file.
    '''

    with open(filepath, 'r') as source:
        with open('parseddata.txt', 'w') as target:
            line = source.readline()
            while line != '':
                line = line.split()
                target.write(f'{line[3]}\t{line[4]}\n')

                line = source.readline()

def main():
    if __name__ ==  '__main__':
        # places masses and periods in separate arrays
        array = np.loadtxt('parseddata.txt')
        masses, periods = np.split(array, 2, axis=1)

        plt.figure(figsize=(14,6))
        plt.title('Period vs. Mass 😛')

        plt.scatter(masses, periods, color='mediumslateblue', s=0.5)

        # formatting for plot
        plt.xlabel('Mass (Msol)')
        plt.ylabel('Period (days)')
        plt.yscale('log')
        plt.ylim(0, 2*10**2)
        plt.xlim(left=0.1, right=1.3)
        plt.gca().invert_xaxis()
        plt.gca().yaxis.set_ticks_position('both')
        plt.gca().xaxis.set_ticks_position('both')
        plt.gca().minorticks_on()

        plt.savefig('figure1')
        plt.show()
        

main()