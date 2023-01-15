import yfinance as yf
import smtplib
from email.message import EmailMessage
### Testing


stock_symbols = ["csco", "tsla", "zm", "xom", "zs","lcid", "roku", "gbtc", "nio", "chpt"]
stock_price_summary = []
stock_news_summary = []

my_email = "<EMAIL_USERNAME_HERE>"
my_password = "<EMAIL PASSWORD HERE>"


# TODO: Note I am not error checking here because I will be providing the data
# in the final project

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    stock_info = stock.info
    # hist = stock.history(period="2mo")
    price = stock_info['regularMarketPrice']
    return price

def stock_price_dashboard():
    '''
    Create a List of Dictionaries containing a Symbol and a Price
    :return: The List of Dictionaries
    '''
    for symbol in stock_symbols:
        price = get_stock_price(symbol)
        stock_price_summary.append({symbol : price})

    return stock_price_summary

def get_stock_news():
    '''

    :param stock_symbols: This is a list of Stock Symbols
    :return:
    '''
    latest_articles = []

    for symbol in stock_symbols:
        latest_articles = []
        stock = yf.Ticker(symbol)

        # Get the latest news articles for the stock
        for news in stock.news:
            # print(f"{news['title']} : {news['link']}")
            latest_articles.append({news['title'] : news['link']})

        stock_news_summary.append(latest_articles)

    return stock_news_summary


def send_news_alert(stock_price_summary, stock_news_summary):

    alert_string = "-------  Mike Stock Dashboard ---------\n"

    for entry in stock_price_summary:
        for key, value in entry.items():
            alert_string += f'* {key}: {value}\n   -----\n'

    alert_string += "-------  Mike News Dashboard ---------\n"
    # For all the lists of dictionaries

    for entries in stock_news_summary:
        stock_symbol = stock_symbols.pop(0)
        alert_string += f"\n------------- News for {stock_symbol} -------------\n"
        # For each list containing a dictionary
        for entry in entries:
            # for each Artcle and Link in the Dictionary
            for article, link in entry.items():
                alert_string += f'{article}: {link}\n'
        alert_string += "\n ----------------\n"

    msg = EmailMessage()
    # Set the subject and body of the email message
    msg['Subject'] = "Stock Dashboard"
    msg.set_content(alert_string)
    # Set the recipient and sender of the email message
    msg['To'] = "<TARGET_EMAIL_HERE>"
    msg['From'] = "<TARGET_FROM_HERE>"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(my_email, my_password)
        smtp.send_message(msg)

def main():
    # Populate the Stocks and their Prices
    stock_price_summary = stock_price_dashboard()
    stock_news_summary = get_stock_news()

    send_news_alert(stock_price_summary, stock_news_summary)

if __name__ == "__main__":
    main()
