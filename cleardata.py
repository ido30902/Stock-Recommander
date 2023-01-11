import json


with open('data.json') as json_file:
    data = json.load(json_file)

    print(f'There are {len(data)} stocks in the list')

    for index, stock in enumerate(data):
        symbol = stock["ACT Symbol"]
        if '$' in symbol or '.' in symbol:
            #print(f'Deleted {symbol}')
            del data[index]
            
    print("=======================")


    for symbol in data:
        print(symbol["ACT Symbol"])


    print(f'There are {len(data)} stocks in the list')

with open('data.json', 'w') as json_file:
    json_file.write(json.dumps(data))