import pandas as pd
import matplotlib.pyplot as plt

def test():
    df = pd.read_csv('data.csv')
    df.plot()
    plt.show()

test()
