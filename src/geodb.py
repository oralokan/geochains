import re

class GeoIPDB(object):
    def search_cn_name(self, patterns):
        pass

    def search_as_names(self, patterns):
        pass

class GeoIPDBMaxMind(GeoIPDB):
    def __init__(self):
        # TODO: Download the files if necessary
        country_file = open('GeoIPCountryWhois.csv', 'r')
        as_file = open('GeoIPASNum2.csv', 'r')
        self.cn_db = country_file.read()
        self.as_db = as_file.read()
        country_file.close()
        as_file.close()

    def search_cn_name(self, patterns):
        names = set()
        for p in patterns:
            matched = re.compile(r'".*{}.*"'.format(p), re.IGNORECASE).findall(self.cn_db)
            cns = set([x.split(',')[-1] for x in matched])
            names = names.union(cns)
        return names

    def search_as_name(self, patterns):
        names = set()
        for p in patterns:
            matched = re.compile(r'".*{}.*"'.format(p), re.IGNORECASE).findall(self.as_db)
            cns = set([x.split(',')[-1] for x in matched])
            names = names.union(cns)
        return names

