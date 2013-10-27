# -*- coding: utf-8 -*-
# Sublime Text 3 test
try:
    from urllib import urlopen, urlencode
except:
    from urllib.request import urlopen
    from urllib.parse import urlencode
import json
from urllib.request import Request
import re


# curl -A "Mozilla/5.0" 'http://translate.google.com/translate_a/t?client=t&text=I%20am%20Hank.&hl=en&sl=auto&tl=zh-CN&ie=UTF-8&oe=UTF-8&multires=1&otf=2&ssel=0&tsel=0&sc=1'


api_url = 'http://translate.google.com.hk/translate_a/t?client=t&hl=en&sl=auto&ie=UTF-8&oe=UTF-8&multires=1&otf=2&ssel=0&tsel=0&sc=1&%s'


text = "你好 北京"
lang = "en"


data = urlencode({'text': text, 'tl': lang})

request = Request(api_url % data)
request.add_header('User-Agent', 'Mozilla/5.0')

result = urlopen(request).read().decode("utf-8")
fixed_json = re.sub(r',{2,}', ',', result).replace(',]', ']')
jsons = json.loads(fixed_json)
text = (json.dumps(jsons[0][0][0], ensure_ascii = False)).strip('"').replace('\\n', "\n").replace('\\t', "\t").replace('\\"', '"')
#m = re.search('^\[+"(.+?)",', result)
print (text)