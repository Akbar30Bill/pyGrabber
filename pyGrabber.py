### Web page Downloader ###

import sys
import urllib.request as urllib
import re

search_level = 0
url = ""
file_format = ""
files_to_download = []

def is_url(__str__):
    if re.match('https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?',__str__):
        return True
    return False

for x in range(0,len(sys.argv)):
    if sys.argv[x-1] == '-l' or sys.argv[x-1] == '-f':
        continue
    if sys.argv[x] == '-l':
        print ('search level  : ' , end = '')
        print (sys.argv[x+1])
        search_level = int(sys.argv[x+1])
    elif is_url(sys.argv[x]):
        print ("search url    : " , end = '' )
        print (sys.argv[x] )
        url = sys.argv[x]
    elif sys.argv[x] == '-f':
        print ("search format : " , end = '')
        print (sys.argv[x+1])
        file_format = sys.argv[x+1]

file_content = urllib.urlopen(url)
file_content = file_content.read().decode('utf-8' , 'ignore')
file_content = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', file_content)

for x in file_content:
    if x.endswith(file_format):
        files_to_download.append(x)

print('from:')
print(file_content)
print('downloading:')
print(files_to_download)

a = 0
for x in files_to_download:
    print("downloading : " , end = '')
    print(x)
    print('\tas  : ' , end = '')
    print(str(a) + '.' + file_format + '\n')
    urllib.urlretrieve(x , str(a) + '.' + file_format)
    a = a+1
