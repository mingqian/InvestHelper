import PySimpleGUI as sg
from language import lang
from investment import Investment


def show_dividend_window(product, history):
    layout = [
        [sg.Text(lang['Code']), sg.Text(product['id'])],
        [sg.Text(lang['Name']), sg.Text(product['name'])],
        [sg.Text(lang['Date']), sg.InputText(key='Date'),
         sg.CalendarButton('...', target='Date', format='%Y-%m-%d')],
        [sg.Text(lang['Dividend']), sg.InputText(key='Capital', enable_events=True)],
        [sg.Button(lang['Ok'], key='Ok'), sg.Button(lang['Cancel'], key='Cancel')]
    ]

    window = sg.Window(lang['Dividend'], layout)
    result = None

    while True:
        event, values = window.read()

        if event == 'Capital':
            if len(values[event]) and values[event][-1] not in '0123456789.':
                window[event].update(values[event][:-1])

        if event == 'Ok':
            h = [float(x['capital']) for x in history if x['date'] == values['Date']]
            if len(h) > 0 and float(values['Capital']) in h:
                sg.popup(lang['Duplicate'])
            else:
                Investment('money.db').add_dividend(product['id'], values)
                result = 'Refresh'
                break

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

    window.close()
    return result
