import requests
from flask import Flask, jsonify

app = Flask(__name__)

API_KEY = 'YOUR API KEY HERE'

top_ten_stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'V', 'JNJ']

@app.route('/buyRecommendation', methods=['GET'])
def buy_recommendation():
    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {"function":"TIME_SERIES_WEEKLY","symbol":"","datatype":"json"}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    for symbol in top_ten_stocks:
        querystring['symbol'] = symbol
        response = requests.get(url, headers=headers, params=querystring)
        #if response has an error return print error
        if 'Error Message' in response.json():
            return response.json()['Error Message']
        
        stock_recommendations = []    

        # get the stock decrease / increase percentage for the week
        data = response.json()
        if 'Weekly Time Series' in data:
            time_series = data['Weekly Time Series']
            ## print the first value in the time series
            stock_values = list(time_series.values())
            current_value = float(stock_values[0]['4. close'])
            previous_value = float(stock_values[1]['4. close'])

            percentage_change = ((current_value - previous_value) / previous_value) * 100

            if percentage_change > 0:
                recommendation = f"{symbol}" + " - " + f"Increased by {percentage_change}% this week"
                stock_recommendations.append(recommendation)
            
    return jsonify(stock_recommendations)


@app.route('/sellRecommendation', methods=['GET'])
def sell_recommendation():
    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {"function":"TIME_SERIES_WEEKLY","symbol":"","datatype":"json"}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    for symbol in top_ten_stocks:
        querystring['symbol'] = symbol
        response = requests.get(url, headers=headers, params=querystring)
        #if response has an error return print error
        if 'Error Message' in response.json():
            return response.json()['Error Message']
        
        stock_recommendations = []    

        # get the stock decrease / increase percentage for the week
        data = response.json()
        if 'Weekly Time Series' in data:
            time_series = data['Weekly Time Series']
            ## print the first value in the time series
            stock_values = list(time_series.values())
            current_value = float(stock_values[0]['4. close'])
            previous_value = float(stock_values[1]['4. close'])

            percentage_change = ((current_value - previous_value) / previous_value) * 100

            if percentage_change < 0:
                recommendation = f"{symbol}" + " - " + f"Decreased by {percentage_change}% this week"
                stock_recommendations.append(recommendation)
            
    return jsonify(stock_recommendations)



if __name__ == '__main__':
    app.run(debug=True)
