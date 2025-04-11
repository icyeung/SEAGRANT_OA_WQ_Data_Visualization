def autocorrelation(x,y):
    """Compute autocorrelation for each spatial point independently."""
    n_t, n_x, n_y = x.shape
    result = np.zeros((n_x, n_y, n_t))  


    for I in range(n_t):
        ac = np.correlate(x[:, i,], y[:, i], mode='full')
        ac = ac[ac.size // 2:]  # Keep non-negative lags
        result[i, :] = ac / ac[0]  # Normalize


def cross_correlation_with_lags(x, y, max_lag):
    lags = np.arange(-max_lag, max_lag + 1)
    corr = [np.corrcoef(x[max_lag:-max_lag], y[max_lag + lag : -max_lag + lag])[0, 1] for lag in lags]
    return lags, corr

'''
def autocorrelation(x):
    """Compute autocorrelation for each spatial point independently."""
    n_t, n_x, n_y = x.shape
    result = np.zeros((n_x, n_y, n_t))  

    for i in range(n_x):
        for j in range(n_y):
            ac = np.correlate(x[:, i, j], x[:, i, j], mode='full')
            ac = ac[ac.size // 2:]  # Keep non-negative lags
            result[i, j, :] = ac / ac[0]  # Normalize

def autocorrelation(x,y):
    """Compute autocorrelation for each spatial point independently."""
    n_t, n_x, n_y = x.shape
    result = np.zeros((n_x, n_y, n_t))  

    for i in range(n_x):
        for j in range(n_y):
            ac = np.correlate(x[:, i, j], y[:, i, j], mode='full')
            ac = ac[ac.size // 2:]  # Keep non-negative lags
            result[i, j, :] = ac / ac[0]  # Normalize
'''