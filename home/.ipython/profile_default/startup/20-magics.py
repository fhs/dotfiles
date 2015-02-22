"""
Magic commands.
"""

from __future__ import print_function

from IPython.core.magic import Magics, magics_class, line_magic

@magics_class
class MyMagics(Magics):

    @line_magic
    def loadnpz(self, params=''):
        """Load a npz file into user namespace.

        %loadnpz <filename.npz>
        """
        import numpy as np
        ip = get_ipython()

        args = params.split()
        if len(args) == 0:
            return
        filename, = args
        ip.push(dict(np.load(filename)), interactive=True)


    @line_magic
    def loadmat(self, params=''):
        """Load a MATLAB file into user namespace.

        %loadmat [-s] <filename.mat>

        The -s option squeezes unit matrix dimensions.
        """
        from scipy.io import loadmat
        ip = get_ipython()

        args = params.split()
        squeeze_me = False
        if len(args) > 0 and args[0] == '-s':
            squeeze_me = True
            args = args[1:]

        if len(args) == 0:
            print("no filename specified")
            return
        ip.push(loadmat(args[0], squeeze_me=squeeze_me), interactive=True)

    @line_magic
    def savemat(self, params=''):
        """Save interactive variables to a MATLAB file.

        %savemat [-c] <filename.mat>
                - Saves all interactive variables.
        %savemat [-c] <filename.mat> <var1 var2 ...>
                - Saves selected variables var1, var2, etc. only.

        The -c option turns on compression of the resulting MATLAB file.
        """
        import scipy.io as sio
        ip = get_ipython()

        args = params.split()
        do_compression = False
        if len(args) > 0 and args[0] == '-c':
            do_compression = True
            args = args[1:]

        if len(args) == 0:
            print("no filename specified")
            return
        filename, vars = args[0], args[1:]

        if len(vars) == 0:
            sel = dict((k, ip.user_ns[k]) for k in ip.magic('%who_ls'))
            print("Saving variables:", list(sel.keys()))
            sio.savemat(filename, sel, do_compression=do_compression)
        else:
            sel = dict((k, ip.user_ns[k]) for k in vars)
            print("Saving variables:", list(sel.keys()))
            sio.savemat(filename, sel, do_compression=do_compression)

    @line_magic
    def imshow(self, params=''):
        """Shows given image in matplotlib.

        %imshow [options] name ...

        -t <title>  Set title of all figures. The default title
                    is the name of the image.
        -c <cmap>   Set colormap of all figures (e.g. gray).

        """
        import matplotlib.pyplot as plt
        from matplotlib import cm

        opts, args = self.parse_options(params, 'c:t:')
        names = args.split()

        cmap = cm.get_cmap()
        if 'c' in opts:
            cmap = cm.get_cmap(name=opts.c)
            if cmap is None:
                print("invalid colormap:", opts.c)
                return

        titles = names
        if 't' in opts:
            titles = len(names)*[opts.t]

        ip = get_ipython()
        for name, tl in zip(names, titles):
            img = np.squeeze(ip.user_ns[name])
            if img.ndim != 2:
                print("%s is not 2-D; skipping" % (name,))
                continue
            plt.figure()
            plt.imshow(img, cmap=cmap)
            plt.colorbar()
            plt.title(tl)

if __name__ == '__main__':
    ip = get_ipython()
    ip.register_magics(MyMagics)

    # clean up ipython's namespace
    del ip, MyMagics
