import matplotlib.pyplot as plt

def plot_scatter_chart(x_list, y_list, title,
                       node_shape = 'o', x_ulim = None, y_ulim = None):
    plt.scatter(x_list, y_list, marker=node_shape)
    plt.title(title)
    if x_ulim:
        plt.xlim(0, x_ulim)
    if y_ulim:
        plt.ylim(0, y_ulim)
    plt.show()
