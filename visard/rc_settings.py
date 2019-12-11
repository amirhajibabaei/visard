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
    'figure.subplot.bottom': 0.21,  # .11
    'figure.subplot.top': 0.9,  # 0.88
    # 'axes.labelpad': 3.0
}


def single_rc(journal, template='simple'):
    if type(template) == str:
        x = globals()[f'template_{template}'].copy()
    elif type(template) == dict:
        x = template.copy()
    x['figure.figsize'] = golden_height(journal['single'])
    return x


def example(rc=template_simple, save_as='rcsettings_example.pdf'):
    with mpl.rc_context(rc=rc):
        plt.xlabel('x')
        plt.ylabel('y')
        plt.plot([0, 1], [0, 1], label=r'f(x)')
        plt.legend()
        plt.savefig(save_as)


if __name__ == '__main__':
    example()