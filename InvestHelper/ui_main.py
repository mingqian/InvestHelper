import queue
import PySimpleGUI as sg
from language import lang
from investment import Investment
from ui_product import show_product_window
from ui_new_product import show_new_product_window
from report import generate_report
from common_util import event_queue

sg.theme('LightGrey2')


class MainWindow:
    def __init__(self):
        self.investment = Investment('money.db')
        self.products = self.fetch_products()
        self.plist = self.create_product_list()
        self.window = self.create_window()

    def fetch_products(self):
        products = self.investment.fetch_products()
        return products if products else []

    def create_product_list(self):
        return [[x['id'], x['name'], x['last_update']] for x in self.products if float(x['share']) > 0.0]

    def create_window(self):
        headings = [lang['Code'], lang['Name'], lang['Last Update']]
        colwidth = [16, 40, 16]
        layout = [
            [sg.Input(size=(95, 1), enable_events=True, key='Filter')],
            [sg.Table(values=self.plist, headings=headings,
                      border_width=3, num_rows=30, col_widths=colwidth,
                      auto_size_columns=False, justification='left',
                      alternating_row_color='lightblue', selected_row_colors='white on blue',
                      enable_events=True, key='ProductsTable')],
            [sg.Button(lang['Exit'], key='Exit'), sg.Button(lang['Add'], key='Add'),
             sg.Button(lang['Report'], key='Report'), sg.Button(lang['Refresh'], key='Refresh')]
        ]
        return sg.Window(lang['Home'], layout)

    def refresh_window(self):
        self.plist = self.create_product_list()
        self.window['ProductsTable'].update(self.plist)

    def filter_products(self, search):
        search = search.lower()
        # code: [0],  name: [1]
        return [x for x in self.plist if search in x[0].lower() or search in x[1].lower()]

    def handle_event(self, event, values):
        if event in (sg.WIN_CLOSED, 'Exit'):
            return False

        if event == 'Filter':
            filtered_list = self.filter_products(values['Filter']) if values['Filter'] else self.plist
            self.window['ProductsTable'].update(filtered_list)

        if event == 'ProductsTable' and values['ProductsTable']:
            product_id = self.plist[values['ProductsTable'][0]][0]
            product = next((x for x in self.products if x['id'] == product_id), None)
            if product:
                show_product_window(product)

        if event == 'Add':
            show_new_product_window()

        if event == 'Report':
            generate_report(self.products)

        if event == 'Refresh':
            self.products = self.fetch_products()
            self.refresh_window()

        return True

    def run(self):
        while True:
            event, values = self.window.read()
            if not self.handle_event(event, values):
                break
            try:
                event_from_queue = event_queue.get_nowait()
                if event_from_queue == 'Refresh':
                    self.products = self.fetch_products()
                    self.refresh_window()
            except queue.Empty:
                pass
        self.window.close()

def show_main_window():
    main_window = MainWindow()
    main_window.run()


show_main_window()