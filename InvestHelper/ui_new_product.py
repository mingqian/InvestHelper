import PySimpleGUI as sg
from language import lang
from investment import Investment
from common_util import compare_date_str, event_queue


def show_new_product_window():
    investment = Investment('./money.db')

    layout = [
        [sg.Text(lang['Code']), sg.InputText(key='Code')],
        [sg.Text(lang['Name']), sg.InputText(key='Name')],
        [sg.Text(lang['Date']), sg.Input(key='Date'),
         sg.CalendarButton('...', target='Date', format='%Y-%m-%d')],
        [sg.Text(lang['Baseline']), sg.InputText(key='Baseline')],
        [sg.Text(lang['StocksPct']), sg.InputText(key='StocksPct')],
        [sg.Text(lang['BondsPct']), sg.InputText(key='BondsPct')],
        [sg.Text(lang['Rating']),
         sg.Combo(['R1', 'R2', 'R3', 'R4', 'R5'], default_value='R2', key='Rating', )],
        [sg.Text(lang['Capital']), sg.InputText(key='Capital', enable_events=True)],
        [sg.Text(lang['Share']), sg.InputText(key='Share', enable_events=True)],
        [sg.Text(lang['Price']), sg.InputText(key='Price', enable_events=True)],
        [sg.Text(lang['Due']), sg.InputText(key='Due'), sg.CalendarButton('...', target='Due', format='%Y-%m-%d')],
        [sg.Button(lang['Ok'], key='Ok'), sg.Button(lang['Cancel'], key='Cancel')]
    ]

    window = sg.Window(lang['Add'], layout)
    result = None

    while True:
        event, values = window.read()

        if event in ('Capital', 'Share', 'Price'):
            if len(values[event]) and values[event][-1] not in '0123456789.':
                window[event].update(values[event][:-1])

        if event == 'Ok':
            products = investment.fetch_products()
            existed = False
            if products is not None:
                for p in products:
                    if values['Code'] == p['id']:
                        sg.popup(lang['Existed'])
                        existed = True
                        break
            if not existed:
                if compare_date_str(values['Date'], values['Due']):
                    sg.popup(lang['Data Wrong'])
                else:
                    investment.add_product(values)
                    result = 'Refresh'
                    break

        if event in (sg.WIN_CLOSED, 'Cancel'):  # always check for closed window
            break

    event_queue.put('Refresh')
    window.close()