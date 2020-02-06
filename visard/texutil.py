import os
import re


def dot_tex(file):
    if file.endswith('.tex'):
        return file
    else:
        return file + '.tex'


def get_1tex(file, target, issub=0, keepfiles=[]):

    prefix = os.path.dirname(file)
    with open(dot_tex(file)) as f:
        lines = f.readlines()
    main = []

    for line in lines:
        if line.startswith('%'):
            if not issub:
                main += [line]
            continue
        elif '\\import' in line:
            assert line.startswith('\\')
            assert line.count('{') == line.count('}') == 2
            assert line.split('}')[-1] == '\n' or line.split('}')[-1] == ''
            s = re.search("import{(.*?)}{(.*?)}", line.strip())
            d, b = s.group(1), s.group(2)
            sub = dot_tex(os.path.join(prefix, d, b))
            main += get_1tex(sub, target, issub=1)
        elif line.strip().startswith('\\includegraphics'):
            s = re.search("includegraphics(.*?){(.*?)}", line.strip())
            f = s.group(2)
            if os.path.dirname(f) in keepfiles:
                main += [line]
            else:
                g = os.path.join(prefix, os.path.basename(f))
                gg = os.path.join('figures', os.path.basename(f))
                os.system(f'cp {g} {os.path.join(target, gg)}')
                assert os.path.isfile(g)
                ll = ''
                for c in line:
                    if c != ' ':
                        break
                    ll += ' '
                ll += f"\\includegraphics{s.group(1)}"+'{' + gg + '}'
                if line.endswith('\n'):
                    ll += '\n'
                main += [ll]
        else:
            main += [line]

    main += [3*'\n']
    return main


def make_1tex(main, target, keepfiles=[]):

    prefix = os.path.dirname(main)
    if not os.path.isdir(target):
        os.system(f'mkdir {target}')
    for x in keepfiles:
        os.system(f'cp -r {prefix}/{x} {target}')
    for d in ['figures']:
        if not os.path.isdir(os.path.join(target, d)):
            os.system(f'mkdir {os.path.join(target, d)}')

    with open(os.path.join(target, 'main.tex'), 'w') as f:
        for line in get_1tex(main, target, keepfiles=keepfiles):
            f.write(line)


def compile_tex(main):
    prefix = os.path.dirname(main)
    base = os.path.basename(main)
    base_ = base.replace('.tex', '')
    cwd = os.getcwd()
    os.chdir(prefix)
    #
    os.system(f'pdflatex {base}')
    os.system(f'bibtex {base_}')
    os.system(f'pdflatex {base}')
    os.system(f'pdflatex {base}')
    #
    os.chdir(cwd)
