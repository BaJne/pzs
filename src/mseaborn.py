import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import threading as trd
import time


def split_data(x, y):
    y = y.sort_values(axis=0)

    indexes = pd.RangeIndex(start=0, stop=len(y), step=1)
    indexes = indexes % 3 == 0
    indexes[0] = False

    y_test = y.iloc[indexes]
    y_train = y[~indexes]

    y_test_indexes = y_test.index
    y_train_indexes = y_train.index

    return x.iloc[y_test_indexes], x.iloc[y_train_indexes], y_test, y_train


def update(hl):
    alpha = [0.5, 0.5]

    for i in range(0,100):
        lock.acquire()
        if finished:
            print('Thread is finished')
            lock.release()
            return
        lock.release()

        alpha[1] = alpha[1]-0.0035
        alpha[0] = alpha[0]+350
        print(alpha[0])

        xx = np.array([0, 800000])
        yy = xx * alpha[1] + alpha[0]

        hl.set_xdata(xx)
        hl.set_ydata(yy)
        plt.draw()
        time.sleep(0.1)


finished = False

if __name__ == '__main__':
    data_frame = pd.read_csv('../data/dm_office_sales.csv')
    y = data_frame['salary']

    X = data_frame['sales']
    X = X.to_frame()
    X['x0'] = 1

    X = X.rename(columns={'sales': 'x1'})
    split_data(X, y)
    X_test, X_train, y_test, y_train = split_data(X, y)

    plt.figure(figsize=(14,5), dpi=180)
    plt.scatter(x=X_test['x1'], y=y_test, marker='x')
    plt.scatter(x=X_train['x1'], y=y_train, marker='x', color='orange')

    alpha = [0.5, 0.5]
    xx = np.array([0, 800000])
    yy = xx * alpha[1] + alpha[0]

    h1 = plt.plot(xx, yy)

    lock = trd.Lock()
    t1 = trd.Thread(target=update, args=(h1))
    t1.start()

    plt.show()

    print('Finish work')
    lock.acquire()
    finished = True;
    lock.release()

    t1.join()
