# Covid-19 statistics in France
#
# this module retrieves regional data from a Github repository
# https://github.com/opencovid19-fr/data

import datetime
import copy
import urllib
import yaml

class FranceData:
    def __init__(self):
        self.loaded_data = {}
        self.config = yaml.load(open('france.yaml').read()) or {}

    def latest_date(self):
        if self.config.get('forced_date'):
            return self.config['forced_date']
        else:
            return self.load_date(date.today().isoformat())

    def load_latest(self):
        latest_date = self.latest_date()
        self.load_date(latest_date)
        return self.clean_data()[latest_date]


    def load_date(self, date):
        self.loaded_data[date] = {'processed': 0, 'errors': 0}
        for directory in self.config['region_directories']:
            self.load_region(date, directory)

    def load_region(self, date, region):
        try:
            region_data = yaml.load(urllib.request.urlopen(self.config['url_template'].format(region=region, date=date)).read())
            self.loaded_data[date][region_data['donneesRegionales']['code']] = region_data
        except:
            self.loaded_data[date]['errors'] += 1

        self.loaded_data[date]['processed'] += 1

    def clean_data(self):
        result = copy.deepcopy(self.loaded_data)
        for date in result.keys():
            result[date].pop('processed')
            result[date].pop('errors')
        return result
