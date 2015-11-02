import re

class GeoIPDB(object):
    def query_cn_ip(self, patterns):
        pass

    def query_as_ip(self, patterns):
        pass

    def search_cn_name(self, patterns):
        pass

    def search_as_names(self, patterns):
        pass

    def cn_ip_range(self, name):
        pass

    def as_ip_range(self, name):
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

    def query_cn_ip(self, patterns):
        names = self.search_cn_name(patterns)
        results = []
        for cn in names:
            cn_ips = self.cn_ip_range(cn)
            print cn_ips
            results += cn_ips
        return results

    def query_as_ip(self, patterns):
        pass

    def search_cn_name(self, patterns):
        names = set()
        for p in patterns:
            matched = re.compile(r'".*{}.*"'.format(p), re.IGNORECASE).findall(self.cn_db)
            cns = set([x.split(',')[-1][1:-1] for x in matched])
            names = names.union(cns)
        return names

    def search_as_name(self, patterns):
        names = set()
        for p in patterns:
            matched = re.compile(r'".*{}.*"'.format(p), re.IGNORECASE).findall(self.as_db)
            cns = set([x.split(',')[-1] for x in matched])
            names = names.union(cns)
        return names

    def cn_ip_range(self, name):
        results = []
        records = re.compile(r'.*{}.*'.format(name)).findall(self.cn_db)
        results = ["{}-{}".format(x.split(',')[0][1:-1], x.split(',')[1][1:-1]) for x in records] 
        return results

    def as_ip_range(self, name):
        # FIXME: AS numbers and IP addresses might get mixed up in regex
        pass
