import PySimpleGUI as sg
from language import lang
from ui_price_update import show_price_update_window
from ui_subscription import show_subscription_window
from ui_redemption import show_redemption_window
from ui_dividend import show_dividend_window
from investment import Investment
from common_util import event_queue


def update_color(window, history):
    index_subscription = [i for (i, x) in enumerate(history) if x['type'] == 'subscription']
    index_redemption = [i for (i, x) in enumerate(history) if x['type'] == 'redemption']
    index_dividend = [i for (i, x) in enumerate(history) if x['type'] == 'dividend']
    for i in index_subscription:
        window.set_index_color(i, background_color='green')
    for i in index_redemption:
        window.set_index_color(i, background_color='orange')
    for i in index_dividend:
        window.set_index_color(i, background_color='red')


def refresh_window(window, product, history):
    h = [f"{x['date']}:\t\t\t{x['capital']}" for x in history]
    window['LastUpdate'].update(product['last_update'])
    window['Price'].update(product['price'])
    window['Capital'].update(product['capital'])
    window['Share'].update(product['share'])
    window['History'].update(h)
    update_color(window['History'], history)


def show_product_window(product):
    code = product['id']
    investment = Investment('money.db')
    history = investment.fetch_history(code)
    h = [f"{x['date']}:\t\t\t{x['capital']}" for x in history]

    col1 = sg.Column([
        # Information pane
        [
            sg.Frame(lang['Information'],
                     [
                         [sg.Text(lang['Code']), sg.Text(code)],
                         [sg.Text(lang['Name']), sg.Text(product['name'])],
                         [sg.Text(lang['Last Update']), sg.Text(product['last_update'], key='LastUpdate')],
                         [sg.Text(lang['Capital']), sg.Text(product['capital'], key='Capital')],
                         [sg.Text(lang['Share']), sg.Text(product['share'], key='Share')],
                         [sg.Text(lang['Price']), sg.Text(product['price'], key='Price')],
                     ])
        ]
    ])

    col2 = sg.Column([
        # Information pane
        [
            sg.Frame(lang['History'],
                     [
                         [sg.Listbox(h, size=(32, 15), key='History')]
                     ])
        ]
    ])

    col3 = sg.Column([
        [
            # Buttons pane
            sg.Frame(lang['Actions'],
                     [
                         [sg.Button(lang['Update Price'], key='UpdatePrice'),
                          sg.Button(lang['Add Subscription'], key='Subscription'),
                          sg.Button(lang['Add Redemption'], key='Redemption'),
                          sg.Button(lang['Add Dividend'], key='Dividend'),
                          sg.Button(lang['Cancel'], key='Cancel')]
                     ])
        ]
    ])

    layout = [
        [col1, col2],
        [col3]
    ]

    window = sg.Window(lang['Product'], layout, finalize=True)
    update_color(window['History'], history)

    result = None

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Cancel'):  # always check for closed window
            break

        if event == 'UpdatePrice':
            result = show_price_update_window(product)

        if event == 'Subscription':
            result = show_subscription_window(product, history)

        if event == 'Redemption':
            result = show_redemption_window(product, history)

        if event == 'Dividend':
            result = show_dividend_window(product, history)

        if result == 'Refresh':
            investment = Investment('money.db')
            product = investment.fetch_product(code)
            history = investment.fetch_history(code)
            refresh_window(window, product, history)

    event_queue.put('Refresh')
    window.close()