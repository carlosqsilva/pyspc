from .ccharts import ccharts
from .tables import A2, D3, D4
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


class pearson(ccharts):
    def __init__(self, title="Pearson Chart"):
        super().__init__()
        self._title = title

    def plot(self, data, size, newdata=None):
        newvalues = None

        R, X = [], []  # values
        for xs in data:
            assert len(xs) == size
            X.append(np.mean(xs))

        if newdata:
            newvalues = [np.mean(xs) for xs in newdata]

        Xvar = np.var(X)
        Xbar = np.mean(X)
        Xskew = np.mean((X - Xbar) ** 3)  # 计算偏度

        # 计算皮尔森分位数
        interval = stats.pearson3.interval(0.9973, Xskew)  # 0.9973的置信区间
        lcl = Xbar + min(interval) * np.sqrt(Xvar)
        ucl = Xbar + max(interval) * np.sqrt(Xvar)
        mean = Xbar
        self.distplot(Xskew, Xvar, mean, lcl, ucl, self._title)
        return (X, mean, lcl, ucl, self._title)

    def distplot(self, Xskew, Xvar, mean, lcl, ucl, title):
        plt.figure()
        plt.title(title)
        plt.xlabel("Frequency")
        x = np.linspace(lcl-0.1, ucl+0.1, 1000)
        y = stats.pearson3.pdf(x, Xskew, mean, np.sqrt(Xvar))
        plt.plot(y, x, c="black")
        plt.axhline(mean, color="blue", linewidth=1.5, linestyle="-.")
        plt.axhline(lcl, color="red", linewidth=1.5, linestyle="--")
        plt.text(0.5, lcl+0.05, "LCL", fontsize=10)
        plt.axhline(ucl, color="red", linewidth=1.5, linestyle="--")
        plt.text(0.5, ucl+0.05, "UCL", fontsize=10)
        plt.savefig("result/{}-SPC.png".format(title), dpi=300)
