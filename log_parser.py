import argparse
import os
import re
import json
from collections import defaultdict
from collections import Counter

parser = argparse.ArgumentParser(description='Log or logs parser')
parser.add_argument('--path', dest='path', help='the input directory')
parser.add_argument('--file', dest='file', action='store', help='the destination')
args = parser.parse_args()

dict_ip = defaultdict(lambda: {"IP": '', "METHOD": '', "URL": '', "STATUS_CODE": 0})
list_of_dick = []

if args.path:
    for path, dirs, files in os.walk(args.path):
        for filename in files:
            if filename.endswith('.log'):
                fullname = os.path.join(path, filename)
                with open(fullname) as file:
                    for index, line in enumerate(file.readlines()):
                        ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                        if ip is not None:
                            ip = ip.group()
                        else:
                            url = 'None'
                        status_code = re.search(r"\s[1-5][0-1][0-9]\s", line)
                        if status_code is not None:
                            status_code = status_code.group()
                        else:
                            status_code = ' 000 '
                        method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD)", line)
                        if method is not None:
                            method = method.groups()[0]
                        else:
                            method = 'None'
                        regex_url = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
                                    r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                        url = re.search(regex_url, line)
                        if url is not None:
                            url = url.group()
                        else:
                            url = 'None'
                        dict_ip['IP'] = ip
                        dict_ip['METHOD'] = method
                        dict_ip['STATUS_CODE'] = int(status_code.split(None, 2)[0])
                        dict_ip['URL'] = url
                        list_of_dick.append(dict(dict_ip))
elif args.file:
    with open(args.file) as file:
        for index, line in enumerate(file.readlines()):
            ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip is not None:
                ip = ip.group()
            else:
                url = 'None'
            status_code = re.search(r"\s[1-5][0-1][0-9]\s", line)
            if status_code is not None:
                status_code = status_code.group()
            else:
                status_code = ' 000 '
            method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD)", line)
            if method is not None:
                method = method.groups()[0]
            else:
                method = 'None'
            regex_url = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
                        r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            url = re.search(regex_url, line)
            if url is not None:
                url = url.group()
            else:
                url = 'None'
            dict_ip['IP'] = ip
            dict_ip['METHOD'] = method
            dict_ip['STATUS_CODE'] = int(status_code.split(None, 2)[0])
            dict_ip['URL'] = url
            list_of_dick.append(dict(dict_ip))
else:
    "Поддерживаете только один аргумент или --path или --file !!!"



ip = Counter(foo['IP'] for foo in list_of_dick)
meth = Counter(foo['METHOD'] for foo in list_of_dick)
code = Counter(foo['STATUS_CODE'] for foo in list_of_dick)

most_common_code = code.most_common(10)

client_errors_codes = [item[0] for item in most_common_code if str(item[0]).startswith('4')]
server_errors_codes = [item[0] for item in most_common_code if str(item[0]).startswith('5')]

client_errors = [elem for elem in list_of_dick if elem['STATUS_CODE'] in client_errors_codes]
server_errors = [elem for elem in list_of_dick if elem['STATUS_CODE'] in server_errors_codes]

final_dic = defaultdict(lambda: {"Count": 0,
                                 "Count_methods": [],
                                 "Top 10 IP": [],
                                 "Top 10 user errors": [],
                                 "Top 10 server errors": []})

final_dic['Count'] = index + 1
final_dic['Count_methods'] = meth
final_dic['Top 10 IP'] = ip.most_common(10)
final_dic['Top 10 user errors'] = client_errors
final_dic['Top 10 server errors'] = server_errors

if args.file:
    file_name = str(args.file)
elif args.path:
    file_name = fullname

with open("%s.json" % file_name, "w+") as outfile:
    json.dump(final_dic, outfile, indent=4)

# json = json.dumps(final_dic, indent=4)
