from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from user.models import Country, City
import requests


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        url = "http://www.citymayors.com/features/euro_cities1.html"

        # Make a GET request to fetch the raw HTML content
        content = requests.get(url).text

        # Parse HTML code for the entire site
        soup = BeautifulSoup(content, 'html.parser')

        table = soup.find("table", attrs={"width": "418"})
        tr_list = table.find_all('tr')

        for tr in tr_list[1:]:
            tds = tr.find_all('td')
            city = tds[1].text
            country = tds[2].text

            country_obj, _ = Country.objects.get_or_create(name=country.strip())

            city_obj = City.objects.create(country=country_obj, name=city)

        self.stdout.write(self.style.SUCCESS("Data add successfully..."))
