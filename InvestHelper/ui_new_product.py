import PySimpleGUI as sg
from language import lang
from investment import Investment
from common_util import compare_date_str, event_queue


# Constants
VALID_INPUT_CHARS = '0123456789.'


class NewProductWindow:
    def __init__(self):
        self.investment = Investment('money.db')
        self.window = self.create_window()

    @staticmethod
    def create_window():
        layout = [
            [sg.Text(lang['Code']), sg.InputText(key='Code')],
            [sg.Text(lang['Name']), sg.InputText(key='Name')],
            [sg.Text(lang['Date']), sg.Input(key='Date'), sg.CalendarButton('...', target='Date', format='%Y-%m-%d')],
            [sg.Text(lang['Baseline']), sg.InputText(key='Baseline')],
            [sg.Text(lang['StocksPct']), sg.InputText(key='StocksPct')],
            [sg.Text(lang['BondsPct']), sg.InputText(key='BondsPct')],
            [sg.Text(lang['Rating']), sg.Combo(['R1', 'R2', 'R3', 'R4', 'R5'], default_value='R2', key='Rating')],
            [sg.Text(lang['Capital']), sg.InputText(key='Capital', enable_events=True)],
            [sg.Text(lang['Share']), sg.InputText(key='Share', enable_events=True)],
            [sg.Text(lang['Price']), sg.InputText(key='Price', enable_events=True)],
            [sg.Text(lang['Due']), sg.InputText(key='Due'), sg.CalendarButton('...', target='Due', format='%Y-%m-%d')],
            [sg.Button(lang['Ok'], key='Ok'), sg.Button(lang['Cancel'], key='Cancel')]
        ]
        return sg.Window(lang['Add'], layout)

    def validate_input(self, event, values):
        if event in ('Capital', 'Share', 'Price'):
            if len(values[event]) and values[event][-1] not in VALID_INPUT_CHARS:
                self.window[event].update(values[event][:-1])

    def handle_event(self, event, values):
        if event in (sg.WIN_CLOSED, 'Cancel'):
            return False

        if event == 'Ok':
            products = self.investment.fetch_products()
            if products and any(p['id'] == values['Code'] for p in products):
                sg.popup(lang['Existed'])
            elif compare_date_str(values['Date'], values['Due']):
                sg.popup(lang['Data Wrong'])
            else:
                self.investment.add_product(values)
                event_queue.put('Refresh')
                return False

        return True

    def run(self):
        while True:
            event, values = self.window.read()
            self.validate_input(event, values)
            if not self.handle_event(event, values):
                break

        self.window.close()


def show_new_product_window():
    new_window = NewProductWindow()
    new_window.run()