import PySimpleGUI as sg
from language import lang
from investment import Investment
from common_util import compare_date_str


def show_price_update_window(product):
    last_update = product['last_update']

    layout = [
        [sg.Text(lang['Name']), sg.Text(product['name'])],
        [sg.Text(lang['Last Update']), sg.Text(last_update)],
        [sg.Text(lang['Last Price']), sg.Text(product['price'])],
        [sg.Text(lang['Date']), sg.InputText(key='Date'),
         sg.CalendarButton('...', target='Date', format='%Y-%m-%d')],
        [sg.Text(lang['Price']), sg.InputText(key='Price', enable_events=True)],
        [sg.Button(lang['Ok'], key='Ok'), sg.Button(lang['Cancel'], key='Cancel')]
    ]

    window = sg.Window(lang['Update Price'], layout)
    result = None

    while True:
        event, values = window.read()

        if event == 'Price':
            if len(values[event]) and values[event][-1] not in '0123456789.':
                window[event].update(values[event][:-1])

        if event == 'Ok':
            update_date = values['Date']
            if compare_date_str(update_date, last_update):
                Investment('money.db').update_price(product['id'], values['Date'], values['Price'])
                result = 'Refresh'
                break
            else:
                sg.popup(lang['Skip Update'])

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

    window.close()
    return result
