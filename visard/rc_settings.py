import matplotlib as mpl
import pylab as plt


inches_per_pt = 1 / 72.27
inches_per_cm = 0.393701
golden_ratio = (5**.5-1)/2  # 0.618


def pt_to_inches(pt):
    return inches_per_pt * pt


def cm_to_inches(cm):
    return inches_per_cm * cm


def golden_height(width):
    return width, golden_ratio * width


def same_height(width):
    return width, width


template_simple = {
    'font.family': 'serif',
    'font.size': 10,
    'mathtext.fontset': 'custom',
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    # 'savefig.format': 'pdf',
    'figure.figsize': golden_height(3.5),
    'axes.xmargin': .0,
    'axes.ymargin': .0,
    'figure.subplot.left': 0.15,  # 0.125
    'figure.subplot.right': 0.9,  # 0.9
    'figure.subplot.bottom': 0.25,  # .11
    'figure.subplot.top': 0.9,  # 0.88
    # 'axes.labelpad': 3.0
}


preamble_common = [r"\usepackage{siunitx}"]


def regular_rc(journal, template='simple', left=None, double=False, height=None, tex=False, preamble='common'):
    if type(template) == str:
        x = globals()[f'template_{template}'].copy()
    elif type(template) == dict:
        x = template.copy()

    # fig size
    if left:
        x['figure.subplot.left'] = left
    w, h = golden_height(journal['single'])
    if double:
        c = journal['double']/journal['single']
        w *= c
        x['figure.subplot.left'] /= c
        x['figure.subplot.right'] = 1-(1-x['figure.subplot.right'])/c
        x['figure.subplot.wspace'] = 0.2 + x['figure.subplot.left']

    if height:
        assert type(height) == int and height > 0
        h *= height
        x['figure.subplot.bottom'] /= height
        x['figure.subplot.top'] = 1-(1-x['figure.subplot.top'])/height
        x['figure.subplot.hspace'] = 0.3 + x['figure.subplot.bottom']
    x['figure.figsize'] = (w, h)

    # latex
    if tex:
        x['text.usetex'] = True
        if preamble is not None:
            if type(preamble) == str:
                x['text.latex.preamble'] = globals(
                )[f'preamble_{preamble}'].copy()
            elif type(preamble) == list:
                x['text.latex.preamble'] = preamble
            mpl.rcParams.update(
                {'text.latex.preamble': x['text.latex.preamble']})
    return x


single_rc = regular_rc


def example(rc=template_simple, save_as='rcsettings_example.pdf'):
    with mpl.rc_context(rc=rc):
        plt.xlabel('x')
        plt.ylabel('y')
        plt.plot([0, 1], [0, 1], label=r'f(x)')
        plt.legend()
        plt.savefig(save_as)


if __name__ == '__main__':
    example()