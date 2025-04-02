import requests

class Quote:
    def __init__(self, quote: str, author: str):
        self.quote = quote
        self.author = author

    def __str__(self):
        return f'"{self.quote}" - {self.author}'
    
    @staticmethod
    def getRandomQuote():
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                quote_data = data[0]
                return Quote(quote_data.get("q", ""), quote_data.get("a", ""))
        return None