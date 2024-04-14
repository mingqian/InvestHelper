from string import ascii_uppercase
from datetime import datetime as dt
from openpyxl import Workbook
from openpyxl.worksheet import table
from openpyxl.styles import Font, PatternFill
import scipy.optimize
from language import lang
from investment import Investment


# Reference:
# https://stackoverflow.com/questions/8919718/financial-python-library-that-has-xirr-and-xnpv-function/
def xnpv(rate, values, dates):
    """
    Similar to Excel's XNPV function.
    dates: list of dt objects
    """
    if rate <= -1.0:
        return float('inf')
    d0 = dates[0]  # dates in ASC order
    return sum(
        [
            vi / ((1.0 + rate) ** ((di - d0).days / 365.0))
            for vi, di in zip(values, dates)
        ]
    )


def xirr(values, dates):
    """
    Similar to Excel's XIRR function.
    dates: list of dt objects
    """
    try:
        return scipy.optimize.newton(lambda r: xnpv(r, values, dates), 0.0)
    except RuntimeError:
        return scipy.optimize.brentq(lambda r: xnpv(r, values, dates), -1.0, 1e10)


def irr_color(irr):
    RED = (0xe0, 0x07, 0x07)
    GREEN = (0x66, 0xff, 0x00)
    print(irr)
    if irr >= 0.04:
        r = GREEN[0]
        g = GREEN[1]
        b = GREEN[2]
    elif irr <= 0.02:
        r = RED[0]
        g = RED[1]
        b = RED[2]
    else:
        r = RED[0] + int((GREEN[0] - RED[0]) * (100 * irr - 2) / 2)
        g = RED[1] + int((GREEN[1] - RED[1]) * (100 * irr - 2) / 2)
        b = RED[2] + int((GREEN[2] - RED[2]) * (100 * irr - 2) / 2)

    color = f'{r:02x}{g:02x}{b:02x}'
    print(r, g, b)
    return color


def calc_financials(product):
    history = Investment('money.db').fetch_history(product['id'])
    values = [h['capital'] for h in history]
    incomes = [h['capital'] for h in history if h['type'] != 'subscription']
    dates = [dt.strptime(h['date'], '%Y-%m-%d') for h in history]

    current_date = product['last_update']
    current_value = round(product['price'] * product['share'], 4)
    values.append(current_value)
    incomes.append(current_value)
    dates.append(dt.strptime(current_date, '%Y-%m-%d'))
    value = sum(incomes)
    profit = sum(values)
    irr = xirr(values, dates)
    return value, profit, irr


def generate_report_header(ws):
    headers = (lang['Code'], lang['Name'], lang['Due'],
               lang['Capital'], lang['Value'], lang['Profit'], lang['IRR'],
               lang['Baseline'], lang['StocksPct'], lang['BondsPct'])
    columns = list(ascii_uppercase)
    for i, h in enumerate(headers):
        ws[f'{columns[i]}1'] = h
        ws[f'{columns[i]}1'].style = 'Headline 2'


def generate_report(products):
    wb = Workbook()
    ws = wb.active
    generate_report_header(ws)
    for i, p in enumerate(products):
        value, profit, irr = calc_financials(p)
        ws[f'A{2 + i}'] = p['id']
        ws[f'B{2 + i}'] = p['name']
        ws[f'C{2 + i}'] = p['first_due']
        ws[f'D{2 + i}'] = p['capital']
        ws[f'E{2 + i}'] = value
        ws[f'F{2 + i}'] = profit
        cell = f'G{2 + i}'
        ws[cell] = f'{irr:.2%}'
        ws[cell].font = Font(bold=True)
        ws[cell].fill = PatternFill(fill_type='solid', fgColor=irr_color(irr))
        ws[f'H{2 + i}'] = p['baseline']
        ws[f'I{2 + i}'] = p['stocks_pct']
        ws[f'J{2 + i}'] = p['bonds_pct']
    tab = table.Table(displayName='RunningProducts', ref=f'A1:G{len(products) + 1}')  # header uses line 1
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 40
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 10
    ws.column_dimensions['H'].width = 20
    ws.column_dimensions['I'].width = 10
    ws.column_dimensions['J'].width = 15
    ws.add_table(tab)
    ws.title = 'Running Products'
    wb.save(f'Report_{dt.now().strftime("%Y-%m-%d")}.xlsx')
