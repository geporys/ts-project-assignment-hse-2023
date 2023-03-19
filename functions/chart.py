import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def plot_nick_rate_nic(nick, rates, nic):
    host = host_subplot(111, axes_class=axisartist.Axes)
    plt.subplots_adjust(right=0.75)
    
    par1 = host.twinx()
    par2 = host.twinx()
    
    par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(60, 0))
    
    par1.axis["right"].toggle(all=True)
    par2.axis["right"].toggle(all=True)
    
    p1, = host.plot(nic.index, nic['Close'], label="Nickel Industries Limited", color="blue")
    p2, = par1.plot(nic.index, nick['Close'], label="Nickel Price", color="#f8962f")
    p3, = par2.plot(nic.index, rates['rate'], label="Australia - Key rates", color="red")
    
    host.set_xlabel("time")
    host.set_ylabel("Nickel Industries Limited")
    par1.set_ylabel("Nickel Price")
    par2.set_ylabel("Australia - Key rates")
    
    host.legend()
    
    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())
    
    host.axis["left"].label.set(fontsize=12, fontweight='bold', fontfamily="Georgia")
    par1.axis["right"].label.set(fontsize=12, fontweight='bold', fontfamily="Georgia")
    par2.axis["right"].label.set(fontsize=12, fontweight='bold', fontfamily="Georgia")
    
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.set_dpi(200)
    
    plt.show()