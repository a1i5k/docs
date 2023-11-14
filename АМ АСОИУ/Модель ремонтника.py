import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import base64
import sys
from functools import partial
from io import BytesIO
import pyperclip
import PySimpleGUI as sg
from functools import reduce


def factorial(N):
    if N < 2: return 1
    return reduce(lambda x, y: x * y, [i for i in range(1, N + 1)])


def get_table_elem(x):
    if isinstance(x, int):
        return str(x)
    if str(x).isdigit() or '.' in str(x) or '-' in str(x):
        return ('%.4f' % (x)).replace('.', ',')
    return str(x)


def p0(N=50, psi=0.005, C=1):
    # k = np.arange(C)
    pk = [[0] for i in range(N + 1)]  # np.empty(N+1)
    res = 0
    for k in range(C + 1):
        pk[k] = factorial(N) * psi ** k / (factorial(k) * factorial(N - k))
    for k in range(C + 1, N + 1):
        pk[k] = factorial(N) * psi ** k / (C ** (k - C) * factorial(C) * factorial(N - k))
    pk = [elem / sum(pk) for elem in pk]
    return pk


def q(pk, C=1, N=50):
    q = 0
    for k in range(C + 1, N + 1):
        q += (k - C) * pk[k]
    return q


def l(pk, C=1, N=50):
    l = 0
    for k in range(1, N + 1):
        l += k * pk[k]
    return l


def u(l, q):
    return l - q


def rho0(u, C=1):
    return u / C


def tp(l, N=50, tno=1000):
    return l * tno / (N - l)


def w(tp, to=5):
    return tp - to


def tc(tp, tno=1000):
    return tp + tno


def rhoe(Tc, tno=1000):
    return tno / Tc


def n_(N, L):
    return N - L


def rhoe2rho0(rhoe, rho0):
    return rhoe / rho0


def y(L, S1=400, S=2000, C=1):
    return C * S1 + L * S


FONT_STYLE = 'Times New Roman'
BIG_FONT = (FONT_STYLE, 18)
MEDIUM_FONT = (FONT_STYLE, 15)
SMALL_FONT = (FONT_STYLE, 12)
TINY_FONT = (FONT_STYLE, 10)
sg.theme('SystemDefault')

if __name__ == '__main__':
    text_element_left = partial(sg.Text, font=MEDIUM_FONT, justification='left')
    text_element_right = partial(sg.Text, font=MEDIUM_FONT, justification='right')
    button_element = partial(sg.Button, focus=True, visible=True, enable_events=True)
    combo_element = partial(sg.Combo, font=MEDIUM_FONT, auto_size_text=True)
    inputtext = partial(sg.InputText, size=(8, 4), justification='right')

    # layout for main_prog
    col1 = [[sg.Text('tno')],
            [sg.Text('to')],
            [sg.Text('N')],
            [sg.Text('C1')],
            [sg.Text('C2')],
            [sg.Text('C3')],
            [sg.Text('S1')],
            [sg.Text('S')], ]

    col2 = [[inputtext(default_text='1000', key='Tno')],
            [inputtext(default_text='8', key='To')],
            [inputtext(default_text='100', key='N')],
            [inputtext(default_text='2', key='C1')],
            [inputtext(default_text='3', key='C2')],
            [inputtext(default_text='4', key='C3')],
            [inputtext(default_text='350', key='S1')],
            [inputtext(default_text='1000', key='S')]]

    perems = ['C', u'P0', 'Q', 'L', 'U', u'ρ0', 'n', u'ρe', 'W', u'Tp', u'Tц', u'(ρe)/ρ0', 'Y']
    data = [[p] + ['-'] * 3 for p in perems]
    headings = ['Параметры', 'Вар1', 'Вар2', 'Вар3']
    #
    fig = plt.figure(figsize=(10.25, 10), facecolor="#f0f0f0")
    ax = fig.add_subplot(1, 1, 1)
    ax.patch.set_facecolor('#f0f0f0')

    b = BytesIO()
    plt.savefig(b, format='PNG', dpi=50)
    b.seek(0)
    b64string = base64.b64encode(b.read())

    layout = [
        [
            sg.Column([
                [sg.Text('Исходные данные')],
                [sg.Column(col) for col in [col1, col2]], ], element_justification='left'),
            sg.Column([
                [sg.Table(values=data,
                          headings=headings,
                          max_col_width=50,
                          select_mode='extended',
                          auto_size_columns=False,
                          justification='right',
                          hide_vertical_scroll=True,
                          vertical_scroll_only=False,
                          num_rows=min(len(data), 20),
                          key='table',
                          background_color="#f0f0f0")
                 ],
            ]
            ),
            sg.Column([
                [
                    button_element('Рассчитать', key='calculate', size=(40, 3))
                ],
                [
                    button_element('Скопировать', key='copy', size=(40, 3))
                ]
            ]),

        ],
        [
            [sg.Image(data=b64string, key='plot'), button_element('Сохранить', key='save', size=(40, 3))],
        ]
    ]

    win = sg.Window('Модель ремонтной службы', layout)

    while True:
        events, values = win.read()
        if events is None:
            break
        if events == 'calculate':
            N = int(values['N'])
            To = int(values['To'])
            Tno = int(values['Tno'])
            S1 = int(values['S1'])
            S = int(values['S'])
            Cs = [int(values[k]) for k in ['C1', 'C2', 'C3']]
            psi = To / Tno
            Y = []
            perems = [perems]
            for C in Cs:
                pk = p0(N=N, psi=psi, C=C)
                Q = q(pk, C=C)
                L = l(pk, C=C)
                U = u(L, Q)
                Rho0 = rho0(U, C=C)
                Tp = tp(L, N=N, tno=Tno)
                W = w(Tp, to=To)
                Tc = tc(Tp, tno=Tno)
                Rhoe = rhoe(Tc, tno=Tno)
                n = n_(N=N, L=L)
                Re2R0 = rhoe2rho0(Rhoe, Rho0)
                Y.append(y(L=L, S1=S1, S=S, C=C))
                perems.append([C, pk[0], Q, L, U, Rho0, n, Rhoe, W, Tp, Tc, Re2R0, Y[-1]])

            plt.cla()
            ax.plot(Cs, Y)
            ax.grid(True)
            ax.set_xticks([_ for _ in range(0, max(Cs) + 1)])

            Ydiff = max(Y) - min(Y)
            ax.set_title('График затрат')
            ax.set_xlabel('Кол-во ремонтников, человек', fontsize=15)
            ax.set_ylabel('Затраты, руб/час', fontsize=15)
            ax.patch.set_facecolor('#f0f0f0')
            ax.yaxis.set_major_locator(MultipleLocator(Ydiff // 10 - ((Ydiff // 10) % 5)))
            ax.yaxis.set_minor_locator(MultipleLocator(Ydiff // 20 - ((Ydiff // 20) % 10)))
            ax.set_ylim([min(Y) // 10 * 10 - 50, max(Y) // 10 * 10 + 50])
            ax.set_xlim([min(Cs) - 1, max(Cs) + 1])
            ax.minorticks_on()
            ax.xaxis.grid(which='major', linestyle='-', linewidth='0.5', color='black', alpha=0.35)
            ax.yaxis.grid(which='major', linestyle='-', linewidth='0.5', color='black', alpha=0.35)
            ax.yaxis.grid(which='minor', linestyle='-', linewidth='0.5', color='black', alpha=0.15)
            b = BytesIO()
            plt.savefig(b, format='PNG', dpi=50)
            b.seek(0)
            b64string = base64.b64encode(b.read())
            win['plot'].update(data=b64string)
            win['table'].update(values=[x for x in zip(*perems)])
        if events == 'save':
            layout = [
                [sg.Text('Имя файла', size=(15, 1)), sg.InputText()],
                [sg.Submit(size=(30, 3), button_text="Сохранить"), sg.Cancel(size=(30, 3), button_text="Закрыть")]
            ]
            window = sg.Window('Сохранить', layout)
            saveevent, savevalues = window.Read()
            window.Close()

            if saveevent == 'Submit':
                name_file = savevalues[0]
                if '.' not in name_file[-5:]:
                    plt.savefig(name_file + '.png', format='PNG', dpi=150)
                else:
                    plt.savefig(name_file, dpi=150)
        if events == 'copy':
            pyperclip.copy('\n'.join(
                ['\t'.join([get_table_elem(x) for x in row])
                 for row in win['table'].get()]))

    win.close()
