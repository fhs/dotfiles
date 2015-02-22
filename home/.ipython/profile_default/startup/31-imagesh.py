"""
Shared axes image plots that provides synchronized zoom/pan.
"""

import matplotlib.pyplot as plt
import numpy as np

def cbar():
    """Alternative to plt.colorbar() function because
    it seems like that function only work with plt.imshow
    and not with ax.imshow (used by Fig class below).
    """
    ax = plt.gca()
    # get the mappable, the 1st and the 2nd are the x and y axes
    # XXX: maybe use ax.get_images() instead of ax.get_children()?
    im = ax.get_children()[2]
    plt.colorbar(im, ax=ax)

# Remove colorbar.
# Doesn't work well. leaves empty space where the colorbar was.
#def nocbar():
#    fig = plt.gcf()
#    fig.delaxes(fig.axes[1])

def cmap(name):
    """Set colormap to name
    """
    plt.gca().get_children()[2].set_cmap(name)
    plt.draw()

def clim(low, high):
    """Set colorbar min/max to low/high.
    Overwrite the standard plt.clim because gci() returns None
    for Fig class figures.
    """
    plt.gca().get_children()[2].set_clim(low, high)
    plt.draw()

def flipx():
    """Flip x-axis (rows) of image.
    """
    im = plt.gca().get_children()[2]
    img = im.get_array()
    im.set_data(img[:,::-1])
    plt.draw()

def flipy():
    """Flip y-axis (columns) of image.
    """
    im = plt.gca().get_children()[2]
    img = im.get_array()
    im.set_data(img[::-1,:])
    plt.draw()

class Fig(object):
    """Wrapper around imshow with synchronized pan/zoom.
    """
    def __init__(self, img, ticks=None, **kwargs):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        im = ax.imshow(img, **kwargs)
        #ax.autoscale(False)
        ax.set_adjustable('box-forced')
        plt.colorbar(im, ticks=ticks, ax=ax)
        self.ax = ax

    def imshow(self, img, ticks=None, **kwargs):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, sharex=self.ax, sharey=self.ax)
        im = ax.imshow(img, **kwargs)
        #ax.autoscale(False)
        ax.set_adjustable('box-forced')
        plt.colorbar(im, ticks=ticks, ax=ax)
        return ax


_SHAREDFIG = None

def imagesh(img, **kwargs):
    """imshow wrapper
    """
    global _SHAREDFIG

    if _SHAREDFIG is None:
        _SHAREDFIG = Fig(img, **kwargs)
        return _SHAREDFIG.ax
    return _SHAREDFIG.imshow(img, **kwargs)

def imageshdiv(img, **kwargs):
    """imshow wrapper with divergent colormap
    """
    return imagesh(img, cmap='RdBu_r', **kwargs)

# https://gist.github.com/jakevdp/91077b0cae40f8f8244a
# By Jake VanderPlas
# License: BSD-style
def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map"""

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

def imageshdis(img, **kwargs):
    """imshow wrapper with discrete colormap
    """
    n = len(np.unique(img[np.isfinite(img)]))
    kwargs['cmap'] = discrete_cmap(n, kwargs.get('cmap', 'Accent'))
    imagesh(img, ticks=range(n), **kwargs)
    low = int(np.floor(np.nanmin(img)))
    high = int(np.ceil(np.nanmax(img)))
    clim(low-0.5, high+0.5)
