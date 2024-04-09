import PySimpleGUI as sg
from language import lang
from investment import Investment
from ui_product import show_product_window
from ui_new_product import show_new_product_window
from report import generate_report

sg.theme('LightGrey2')


def refresh_window(window, plist):
    window['ProductsTable'].update(plist)
    return None


def get_field(item, field_str):
    if field_str == 'code':
        return item[0]
    elif field_str == 'name':
        return item[1]


def show_main_window():
    investment = Investment('money.db')
    products = investment.fetch_products()
    if products is None:
        plist = []
    else:
        plist = [[x['id'], x['name'], x['last_update']] for x in products]

    headings = [lang['Code'], lang['Name'], lang['Last Update']]
    colwidth = [16, 40, 16]
    layout = [
        [sg.Input(size=(95, 1), enable_events=True, key='Filter')],
        [sg.Table(values=plist, headings=headings,
                  border_width=3,
                  num_rows=30,
                  col_widths=colwidth,
                  auto_size_columns=False,
                  justification='left',
                  alternating_row_color='lightblue',
                  selected_row_colors='white on blue',
                  enable_events=True,
                  key='ProductsTable')],
        [sg.Button(lang['Exit'], key='Exit'), sg.Button(lang['Add'], key='Add'),
         sg.Button(lang['Report'], key='Report'),
         sg.Button(lang['Refresh'], key='Refresh')]
    ]

    window = sg.Window(lang['Home'], layout)
    result = None

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if values['Filter'] != '':  # if a keystroke entered in search field
            search = values['Filter'].lower()
            this_plist = [x for x in plist
                          if (search in get_field(x, 'code').lower()
                              or search in get_field(x, 'name').lower())]
        else:
            # display original unfiltered list
            this_plist = plist
        window['ProductsTable'].update(this_plist)  # display in the listbox

        # if a list item is chosen
        if event == 'ProductsTable' and len(values['ProductsTable']):
            try:
                product = [x for x in products
                           if x['id'] == get_field(this_plist[values['ProductsTable'][0]], 'code')][0]
                result = show_product_window(product)
            except IndexError:
                print('show_main_win: skip error')

        if event == 'Add':
            result = show_new_product_window()

        if event == 'Report':
            generate_report(products)

        if result == 'Refresh' or event == 'Refresh':
            products = investment.fetch_products()
            plist = [[x['id'], x['name'], x['last_update']] for x in products]
            result = refresh_window(window, plist)

    window.close()


show_main_window()
