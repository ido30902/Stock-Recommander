import requests
import smtplib
import json
import time

min_market_cap = 100000000

def main():


    print("Starting the scan...")
    stocks_list = get_stocks_db()


    
    
    




def scan_50_stocks():
    for stock in range(50):
        print()


def extract_symbols(list):
    new_list = []
    for symbol in list:
        newlist.append(symbol["ACT Symbol"])
    return new_list


def set_last_stock(symbol):
    with open('stocks.json', 'w') as json_file:
        data = json.loads(json_file)
        data["last_stock"].update(symbol)
        json_file.write(data)

def create_stock_json_in_db(symbol):
    with open('stocks.json') as json_file:
        data = json.load(json_file)

        stocks = data["stocks"]
        
        exists = False
        for stock in stocks:
            if symbol in stock["symbol"]:
                exists = True
        if not exists:
            print(f'Symbol added: {symbol}')
            new_obj = {"symbol": symbol, "PE": 0, "ROA": 0, "market_cap": 0}
            data["stocks"].append(new_obj)

    with open('stocks.json', 'w') as json_file:
        json_file.write(json.dumps(data))


# This function displays all the stocks in the list
def display_stocks(stocks):
    for stock in stocks:
        print(stock["symbol"])

#This function chooses the stocks based on the parameters given.
def choose_stocks(stocks):

    selected_stocks = []

    # Iterate through each stock and check if it meets the criteria
    for symbol in stocks:
        
        print_border()
        print(f'Scanning now: {symbol["ACT Symbol"]} , {symbol["Company Name"]}')
        
                
        
        # Check if the stock has a market capitalization greater than $100 million and add it to the list if it does
        if stock.market_cap > min_market_cap:
            selected_stocks.append((stock['Symbol'], stock.pe_ratio, stock.roa))

    # Sort the list of stocks by the combination of lowest PE ratio and highest ROA
    selected_stocks.sort(key=lambda x: (x[1], -x[2]))

    count = 0
    msg = "The following stocks have a market capitalization greater than $100 million and are sorted by the combination of lowest PE ratio and highest ROA:\n"
    for stock in selected_stocks:
        if count > 5:
            break
        msg += f"{stock[0]}: PE ratio={stock[1]:.2f}, ROA={stock[2]:.2f}\n"
        count += 1

    print(msg)

#This function uses the Alpha Vantage API to fetch the data nesseecry for the program
def update_stock_data(symbol):
    # Set the API endpoint URL and your API key
    endpoint = "https://www.alphavantage.co/query"
    api_key = "D1IUPOZ619PG5ZHQ"

    # Set the parameters for the API request
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "datatype": "json",
        "apikey": api_key,
    }

    # Send the GET request to the API endpoint
    response = requests.get(endpoint, params=params)
    
    stock = response.json()

    # Update the database accordingly to the symbol and then fetch the data regularly from the db
    if 'MarketCapitalization' in stock:
        market_cap = float(stock['MarketCapitalization'])
        pe_ratio = float(stock['PERatio']) / float(stock['EPS'])
        roa = float(stock['ReturnOnAssetsTTM'])
        print(f'Market Capitalization: {market_cap:,}$\nPE ratio: {pe_ratio}\nReturn on assets: {roa}')
        return market_cap,pe_ratio,roa
    return 0, 0, 0

#This function takes the nyse data file and converts it to list the program can handle.
def convert_json_to_list():
    with open('nyse_data.json') as json_file:
        data = json.load(json_file)
        stocks = data['stocks']
        list = []
        for stock in stocks:
            list.append(stock["ACT Symbol"])
        return list
        

#This function updates the database with the newly check stocks
def update_db(stock_list):
    pass

#This function get the stocks from the database
def get_stocks_db():
    with open('stocks.json') as json_file:
        return json.load(json_file)["stocks"]


def get_symbols_from_raw_data():
    with open('nyse_data.json') as json_file:
        data = json.load(json_file)
        new_list = []
        for stock in data:
            new_list.append(stock["ACT Symbol"])
        return new_list

#This function prints the border
def print_border():
    print('==================================================================')

#This function sends the mail
def send_mail(msg):

    # Send an email with the list of stocks
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("your_email_address@gmail.com", "your_email_password")
    
    server.sendmail("from_email@gmail.com", "to_email@gmail.com", msg)
    server.quit()


if __name__ == '__main__':
    main()
