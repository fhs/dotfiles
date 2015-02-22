"""
Interactive image plots.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons

def intimage(img, **kwargs):
    """Interactive imshow with widgets.
    """
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0, bottom=0.20)
    im = ax.imshow(img, **kwargs)
    cbar = fig.colorbar(im)

    rax = plt.axes([0.025, 0.025, 0.13, 0.13])
    cmap_names = [im.get_cmap().name, 'gray', 'binary']
    c = im.get_cmap().name
    active = 0
    for i, name in enumerate(cmap_names):
        if c == name:
            active = i
            break
    radio = RadioButtons(rax, cmap_names, active=active)
    def cmapfunc(label):
        im.set_cmap(label)
        fig.canvas.draw_idle()
    radio.on_clicked(cmapfunc)

    low, high = im.get_clim()
    bot = min(low, np.nanmin(img))
    top = max(high, np.nanmax(img))
    axmin = plt.axes([0.25, 0.025, 0.60, 0.03])
    axmax  = plt.axes([0.25, 0.07, 0.60, 0.03])
    smin = Slider(axmin, 'Min', bot, top, valinit=low)
    smax = Slider(axmax, 'Max', bot, top, valinit=high)

    def update(val):
        im.set_clim(smin.val, smax.val)
        fig.canvas.draw_idle()
    smin.on_changed(update)
    smax.on_changed(update)

    flipxbut = Button(plt.axes([0.25, 0.12, 0.1, 0.04]), 'Flip X')
    def flipx(event):
        img = im.get_array()
        im.set_data(img[:,::-1])
        fig.canvas.draw_idle()
    flipxbut.on_clicked(flipx)

    flipybut = Button(plt.axes([0.36, 0.12, 0.1, 0.04]), 'Flip Y')
    def flipx(event):
        img = im.get_array()
        im.set_data(img[::-1,:])
        fig.canvas.draw_idle()
    flipybut.on_clicked(flipx)

    # return these so we keep a reference to them.
    # otherwise the widget will no longer be responsive
    return im, radio, smin, smax, flipxbut, flipybut
