# -*- coding: utf-8 -*-
# author:mtimer
# https://github.com/MtimerCMS/SublimeText-Google-Translate-Plugin

import sublime
import sublime_plugin
try:
    from urllib import urlopen, urlencode
except:
    from urllib.request import urlopen
    from urllib.parse import urlencode
from urllib.request import Request
import json
import re

settings = sublime.load_settings("goTranslate.sublime-settings")
api_url = 'http://translate.google.com.hk/translate_a/t?client=t&hl=en&ie=UTF-8&oe=UTF-8&multires=1&otf=2&ssel=0&tsel=0&sc=1&%s'

class GoTranslateCommand(sublime_plugin.TextCommand):
    
    def run(self, edit, source_language = settings.get("source_language"), target_language = settings.get("target_language")):
        if not source_language:
            source_language = settings.get("source_language")
        if not target_language:
            target_language = settings.get("target_language")

        for region in self.view.sel():
            if not region.empty():

                v = self.view
                selection = v.substr(region)

                result = translate(selection, source_language, target_language)

                text = (json.dumps(result[0][0][0], ensure_ascii = False)).strip('"').replace('\\n', "\n").replace('\\t', "\t").replace('\\"', '"')

                # print (text)
                v.replace(edit, region, text)


    def is_visible(self):
        for region in self.view.sel():
            if not region.empty():
                return True
        return False


def translate(text, sl, tl):
        if sl:
            data = urlencode({'text': text, 'sl': sl, 'tl': tl})
        else:
            data = urlencode({'text': text, 'sl': 'auto', 'tl': tl})

        request = Request(api_url % data)
        request.add_header('User-Agent', 'Mozilla/5.0')
        if sublime.version() < '3':
            result = urlopen(request).read()
            fixed_json = re.sub(r',{2,}', ',', result).replace(',]', ']')
            jsons = json.loads(fixed_json.decode("utf-8"))
        else:
            result = urlopen(request).read().decode("utf-8")
            fixed_json = re.sub(r',{2,}', ',', result).replace(',]', ']')
            jsons = json.loads(fixed_json)
        return jsons


def plugin_loaded():
    global settings
    settings = sublime.load_settings("goTranslate.sublime-settings")