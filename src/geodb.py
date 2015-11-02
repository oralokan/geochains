import re

def int2ipv4(i):
    ip=[]
    for j in range(4):
        ip += [i/256**(3-j)]
        i -= ip[j] * 256**(3-j)
    ips = [str(x) for x in ip]
    return '.'.join(ips)


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
            results += cn_ips
        return results

    def query_as_ip(self, patterns):
        names = self.search_as_name(patterns)
        results = []
        for a in names:
            a_ips = self.as_ip_range(a) 
            results += a_ips
        return results

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
        results = []
        records = re.compile(r'.*{}.*'.format(name)).findall(self.as_db)
        for a in records:
            l = a.split(',')
            start_ip = int2ipv4(int(l[0]))
            end_ip = int2ipv4(int(l[1]))
            results.append("{}-{}".format(start_ip, end_ip))
        return results
