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
    else:
        print('The diagonals of the covariance matrix are not the variances')
    
    # JAB Problem 2
    # JAB Calculate the correlation matrix
    s = np.array([np.std(i, ddof=1) for i in data])
    cor = np.array([[c[i][j]/(s[i]*s[j]) for i in range(len(c))] for j in range(len(c))])

    # JAB Find the most correlated and anti correlated columns
    mins = np.array([min(i) for i in cor])
    maxs = np.array([max(i[i < 0.99]) for i in cor])
    
    all_max = max(maxs)
    all_min = min(mins)
    
    max_cols = [i+1 for i in range(len(cor)) if all_max in cor[i]]
    min_cols = [i+1 for i in range(len(cor)) if all_min in cor[i]]
    
    print('The most correlated columns are {} and {}, with value of {}'.format(
        max_cols[0], max_cols[1], all_max))
    print('The most anti-correlated columns are {} and {}, with value of {}'.
          format(min_cols[0], min_cols[1], all_min))
    
    # JAB Problem 3
    
    
