"""
Colormap customizations dealing with NaN.
"""

from matplotlib import cm

# May of the colormaps uses white or light gray color which
# makes it hard to distinguish from NaN also represented by
# white. Change NaN color to something else.
for name in cm.datad:
    cm.get_cmap(name).set_bad('gray')

# These uses all shades of gray.
cm.gray.set_bad('brown')
cm.gray_r.set_bad('brown')
cm.binary.set_bad('brown')
cm.binary_r.set_bad('brown')
