from database import DbHandler
from common_util import compare_date_str


class Investment:
    def __init__(self, dbname):
        self._dbname = dbname

    def fetch_product(self, code):
        with DbHandler(self._dbname) as db:
            sql = f'SELECT id, name, last_update, capital, share, price, first_due FROM portfolio WHERE id = "{code}"'
            return db.fetchone(sql)

    def fetch_products(self):
        with DbHandler(self._dbname) as db:
            sql = ('SELECT id, name, last_update, capital, share, price, first_due, baseline,'
                   'stocks_pct, bonds_pct FROM portfolio')
            return db.fetchall(sql)

    def fetch_history(self, code):
        with DbHandler(self._dbname) as db:
            sql = (f'SELECT date, type, capital FROM history WHERE id = "{code}" '
                   f'ORDER BY date ASC')
            return db.fetchall(sql)

    def add_product(self, values):
        with DbHandler(self._dbname) as db:
            # Add to portfolio table
            sql = 'CREATE TABLE IF NOT EXISTS portfolio (id TEXT, name TEXT, baseline TEXT, ' \
                  'stocks_pct TEXT, bonds_pct TEXT, rating TEXT, ' \
                  'capital FLOAT, share FLOAT, price FLOAT, irr FLOAT, ' \
                  'last_update DATE, first_due DATE)'
            db.execute(sql)

            try:
                code = values['Code']
                name = values['Name']
                baseline = values['Baseline']
                stocks_pct = values['StocksPct']
                bonds_pct = values['BondsPct']
                rating = values['Rating']
                capital = values['Capital']
                share = values['Share']
                price = values['Price']
                update = values['Date']
                due = values['Due']

                sql = (f'INSERT INTO portfolio (id, name, baseline, '
                       f'stocks_pct, bonds_pct, rating,'
                       f'capital, share, price, '
                       f'last_update, first_due) '
                       f'VALUES ("{code}", "{name}", "{baseline}",'
                       f'"{stocks_pct}", "{bonds_pct}", "{rating}", '
                       f'{capital}, {share}, {price},'
                       f'"{update}", "{due}")')
                db.execute(sql)

                # Add first transaction to history table
                sql = ('CREATE TABLE IF NOT EXISTS history (id TEXT, date DATE, type TEXT, capital FLOAT, '
                       'share FLOAT, price FLOAT, due DATE)')
                db.execute(sql)

                sql = (f'INSERT INTO history (id, date, type, capital, share, price, due) '
                       f'VALUES ("{code}", "{update}", "subscription", -{capital},'
                       f'{share}, {price}, "{due}")')
                db.execute(sql)

                db.commit()

            except IndexError:
                print('IndexError')
                pass

    def update_price(self, code, date, price):
        with DbHandler(self._dbname) as db:
            sql = (f'UPDATE portfolio SET price = {price}, last_update="{date}" '
                   f'WHERE id = "{code}"')
            db.run(sql)

    def add_subscription(self, code, values):
        with DbHandler(self._dbname) as db:
            date = values['Date']
            capital = values['Capital']
            share = values['Share']
            price = values['Price']
            due = values['Due']
            # Add transaction to history table
            sql = (f'INSERT INTO history (id, date, type, capital, share, price, due) '
                   f'VALUES ("{code}", "{date}", "subscription", -{capital}, {share}, {price}, "{due}")')
            db.execute(sql)

            # adjust total capital, share, due date
            # in portfolio table
            p = self.fetch_product(code)
            new_capital = p['capital'] + float(capital)
            new_share = p['share'] + float(share)
            new_due = due if compare_date_str(p['first_due'], due) else p['first_due']

            sql = (f'UPDATE portfolio SET capital = {new_capital},'
                   f'share = {new_share}, '
                   f'first_due = "{new_due}" '
                   f'WHERE id = "{code}"')
            db.execute(sql)

            db.commit()

    def add_redemption(self, code, values):
        with DbHandler(self._dbname) as db:
            date = values['Date']
            capital = values['Capital']
            share = values['Share']
            price = values['Price']
            # Add transaction to history table
            sql = (f'INSERT INTO history (id, date, type, capital, share, price) '
                   f'VALUES ("{code}", "{date}", "redemption", {capital}, {share}, {price})')
            db.execute(sql)

            # adjust total share
            # in portfolio table
            p = self.fetch_product(code)
            new_share = p['share'] - float(share)

            sql = (f'UPDATE portfolio SET share = {new_share} '
                   f'WHERE id = "{code}"')
            db.execute(sql)

            db.commit()

    def add_dividend(self, code, values):
        with DbHandler(self._dbname) as db:
            date = values['Date']
            capital = values['Capital']
            # Add transaction to history table
            sql = (f'INSERT INTO history (id, date, type, capital) '
                   f'VALUES ("{code}", "{date}", "dividend", {capital})')
            db.run(sql)
