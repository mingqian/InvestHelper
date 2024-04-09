import PySimpleGUI as sg
from language import lang
from investment import Investment
from common_util import compare_date_str


def show_subscription_window(product, history):
    layout = [
        [sg.Text(lang['Code']), sg.Text(product['id'])],
        [sg.Text(lang['Name']), sg.Text(product['name'])],
        [sg.Text(lang['Date']), sg.InputText(key='Date'),
         sg.CalendarButton('...', target='Date', format='%Y-%m-%d')],
        [sg.Text(lang['Capital']), sg.InputText(key='Capital', enable_events=True)],
        [sg.Text(lang['Share']), sg.InputText(key='Share', enable_events=True)],
        [sg.Text(lang['Price']), sg.InputText(key='Price', enable_events=True)],
        [sg.Text(lang['Due']), sg.InputText(key='Due'),
         sg.CalendarButton('...', target='Due', format='%Y-%m-%d')],
        [sg.Button(lang['Ok'], key='Ok'), sg.Button(lang['Cancel'], key='Cancel')]
    ]

    window = sg.Window(lang['Subscription'], layout)
    result = None

    while True:
        event, values = window.read()

        if event in ('Capital', 'Share', 'Price'):
            if len(values[event]) and values[event][-1] not in '0123456789.':
                window[event].update(values[event][:-1])

        if event == 'Ok':
            h = [float(x['capital']) for x in history if x['date'] == values['Date']]
            if len(h) > 0 and -float(values['Capital']) in h:
                sg.popup(lang['Duplicate'])
            elif compare_date_str(values['Date'], values['Due']):
                sg.popup(lang['Data Wrong'])
            else:
                Investment('money.db').add_subscription(product['id'], values)
                result = 'Refresh'
                break

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

    window.close()
    return result
