from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import View
from datetime import datetime
from newsapi import NewsApiClient
from pathlib import Path
import environ
import requests

BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
env_file_path = BASE_DIR.parent / '.env'
env.read_env(env_file_path)

class ExchangeRateView(View):
    def get_exchange_rates(self):
        api_key_to_exchange_rate = env('api_key_to_exchange_rate')
        print('api_key_to_exchange_rate=', api_key_to_exchange_rate)
        exchange_rate_url = (f'http://data.fixer.io/api/latest?access_key={api_key_to_exchange_rate}'
                             f'&symbols=USD,EUR,PLN,UAH')

        cached_rates = cache.get('exchange_rates')
        print('cached_exchange_rates=', cached_rates)
        if cached_rates:
            return cached_rates

        try:
            response = requests.get(exchange_rate_url)
            response.raise_for_status()
            currency_data = response.json()

            if 'rates' in currency_data:
                usd_to_uah = round(
                    currency_data['rates']['UAH'] / currency_data['rates']['USD'], 2)
                eur_to_uah = round(
                    currency_data['rates']['UAH'] / currency_data['rates']['EUR'], 2)
                pln_to_uah = round(
                    currency_data['rates']['UAH'] / currency_data['rates']['PLN'], 2)

                rates = {
                    'usd_to_uah': usd_to_uah,
                    'eur_to_uah': eur_to_uah,
                    'pln_to_uah': pln_to_uah,
                }
                cache.set('exchange_rates', rates, timeout=1800)

                return rates
            else:
                return {'error': 'Failed to retrieve exchange rates. Please try again later.'}

        except (requests.exceptions.HTTPError, requests.exceptions.RequestException):
            return {'error': 'Failed to retrieve exchange rate data. Please try again later.'}


class NewsView(View):
    def get_news(self):
        newsapi = NewsApiClient(api_key=env('api_key'))
        print('api_key=',env('api_key'))
        categories = ['business', 'entertainment', 'general',
                      'health', 'science', 'sports', 'technology']
        news_by_category = {}

        cached_news = cache.get('news_data')
        if cached_news:
            return cached_news

        for category in categories:
            try:
                news_data = newsapi.get_top_headlines(category=category)
            except Exception as e:
                return {'error': 'Failed to retrieve news. Please try again later.'}

            articles = []
            for article in news_data.get('articles', []):
                if (article.get('title') == '[Removed]' or
                        article.get('description') == '[Removed]' or
                        (article.get('author') == '[Removed]' or not article.get('author'))):
                    continue

                published_at = article.get('publishedAt', None)
                if published_at:
                    date_object = datetime.fromisoformat(published_at[:-1])
                    formatted_date = date_object.strftime("%d %B %Y, %H:%M")
                else:
                    formatted_date = 'Unknown'

                articles.append({
                    'title': article.get('title', 'No title available'),
                    'description': article.get('description', 'No description available'),
                    'url': article.get('url', '#'),
                    'published_at': formatted_date,
                    'author': article.get('author', 'Unknown'),
                })

            news_by_category[category] = articles

        cache.set('news_data', news_by_category, timeout=1800)

        return news_by_category

class ExchangeRateNewsView(View):
    template_name = 'news.html'

    def get(self, request):
        exchange_view = ExchangeRateView()
        exchange_data = exchange_view.get_exchange_rates()

        news_view = NewsView()
        news_data = news_view.get_news()

        context = {
            **exchange_data,
            'news_by_category': news_data,
        }

        return render(request, self.template_name, context)
