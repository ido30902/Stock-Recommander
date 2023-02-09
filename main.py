import requests
import smtplib
import json
import time


def main():


    days_count = 0

    print("Starting the scan...")
    stocks_list = get_stocks_db()

    #Once a day the program loops through the next 499 stocks and updated their data
    #Once a week the program sends a mail
    
    daily_stock_count = 0
    while True:  
        days_count += 1
        
        # Update stocks
        for index in stocks_list[last_stock_index(stocks_list):]:

            new_data = update_stock_data(index['symbol'])
            update_stock_db(index['symbol'],new_data[0],new_data[1],new_data[2])
            set_last_stock(index['symbol'])

            daily_stock_count += 1

            # 500 daily limit
            if daily_stock_count == 499:
                print('499')
                break
            
            # API limit - Every 14 seconds a new request is sent
            time.sleep(14)

        # Week check
        if days_count == 7:
            days_count = 0
            choose_stocks(stocks_list)
        time.sleep(60 * 60 * 24)
        days_count += 1


def last_stock_index(stock_list):
    with open('util.json') as json_file:
        data =  json.load(json_file)

        symbol = data['last_stock']

        for i,stock in enumerate(stock_list):
            if stock['symbol'] == symbol:
                return i



def set_last_stock(symbol):
    with open('util.json', 'w') as json_file:
        data = {"last_stock" : symbol}
        json_file.write(json.dumps(data))

def create_stock_json_in_db(symbol):
    with open('stocks.json') as json_file:
        stocks = json.load(json_file)
        
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
def choose_stocks(stocks_list):

    selected_stocks = []

    # Iterate through each stock and check if it meets the criteria
    for stock in stocks_list:

        if stock['PE'] > 0 and stock['ROA'] > 0:
            # Check if the stock has a market capitalization greater than $100 million and add it to the list if it does
            selected_stocks.append((stock['symbol'], stock['PE'], stock['ROA']))

    # Sort the list of stocks by the combination of lowest PE ratio and highest ROA
    selected_stocks.sort(key=lambda x: (x[1], -x[2]))

    count = 0
    msg = "The following stocks have a market capitalization greater than $100 million and are sorted by the combination of lowest PE ratio and highest ROA:\n"
    for stock in selected_stocks:
        if count > 5:
            break
        msg += f"{stock[0]},{get_name_by_symbol(stock[0])}: PE ratio={stock[1]:.2f}, ROA={stock[2]:.2f}\n"
        count += 1

    print(msg)
    #send_mail(msg)

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
    if ('MarketCapitalization' in stock) and ('PERatio' in stock) and ('PERatio' in stock) and ('ReturnOnAssetsTTM' in stock):
        if (stock['MarketCapitalization'] == 'None') or (stock['PERatio'] == 'None') or (stock['ReturnOnAssetsTTM'] == 'None') or (stock['EPS'] == 'None'):
            return 0,0,0

        market_cap = float(stock['MarketCapitalization'])
        pe_ratio = float(stock['PERatio']) / float(stock['EPS'])
        roa = float(stock['ReturnOnAssetsTTM'])
        print_border()        
        print(f'Stock updated: {symbol} \nMarket Capitalization: {market_cap:,}$\nPE ratio: {pe_ratio}\nReturn on assets: {roa}')
        return pe_ratio,roa,market_cap
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
        

def update_stock_db(symbol,pe,roa,market_cap):
     # load json file
    with open("stocks.json") as json_file:
        stocks = json.load(json_file)

    # find the stock by symbol
    for i, stock in enumerate(stocks):
        if stock["symbol"] == symbol:
            stocks[i] = {"symbol": symbol, "PE": pe, "ROA": roa, "market_cap": roa }
            break
    else:
        # if stock not found add it to the list
        stocks.append({"symbol": symbol, "PE": pe, "ROA": roa, "market_cap": market_cap })
    # write the updated stocks to the json file
    with open("stocks.json", "w") as file:
        json.dump(stocks, file)

#This function get the stocks from the database
def get_stocks_db():
    with open('stocks.json') as json_file:
        return json.load(json_file)

def get_name_by_symbol(symbol):
    with open('nyse_data.json') as json_file:
        data = json.load(json_file)

        for stock in data:
            if stock["ACT Symbol"] == symbol:
                return stock["Company Name"]

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