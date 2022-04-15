import numpy as np

if __name__ == '__main__':
    # JAB Problem 1
    # JAB Read in data file
    filepath = '/d/scratch/ASTR5160/week13/line.data'
    data = np.loadtxt(filepath, unpack=True)
    
    # JAB Calculate the covariance matrix
    c = np.cov(data)
    # JAB The covariance matrix should be 10x10 (which it is) because it is
    # finding the variances of each bin of which there are 10
    
    # JAB Calculate the variances of each bin
    v = np.array([np.var(i, ddof=1) for i in data])
    
    # JAB Confirm the diagonal elements of the martix are the variances
    good = [round(c[i][i],6) == round(v[i],6) for i in range(len(v))]
    if good:
        print('The diagonals of the covariance matrix are equal to the variances')
    
    # JAB Problem 2
    
