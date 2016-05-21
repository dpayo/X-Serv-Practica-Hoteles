#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib
from  models import Hotel
from  models import Image

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.record=None;

        self.theContent = ""
        self.titulo=""
        self.url=""
        self.dir=""
        self.img=""
        self.tipo=""
        self.body=""
        self.email=""
        self.phone=""
        self.recimg=None
        self.is_star=False;
        self.is_img=False;
        self.is_cat =False;
    def startElement (self, name, attrs):

        self.theContent=name
        if name =='basicData':
            self.record = Hotel(name="", url="",body="", address="",source="",stars="",tipo="",numbercom=0,email="",phone="")

        if name =="item":
            if attrs['name']== "SubCategoria":
                self.is_star=True;
        if name =="item":
            if attrs['name']== "Categoria":
                self.is_cat=True;
        if name =='media':
            if attrs['type']== "image":
                self.is_img=True
                self.recimg=Image(hid=0,img=self.record,url="")

    def endElement (self, name):
            if self.theContent=='phone':
                self.record.phone=self.phone;
                self.record.save()
            if self.theContent =='email':
                self.record.email=self.email;
                self.record.save()
            if self.theContent=='body':
                self.record.body=self.body;
                self.record.save()

            if self.theContent=='item' and self.is_star:
                self.record.stars=self.tipo
                self.record.save();
                self.is_star=False;

            if self.theContent=='item' and self.is_cat:

                self.record.tipo=self.tipo
                self.record.save();
                self.is_cat=False;
            if self.theContent == 'url' and self.is_img:
                self.record.source=self.img
                self.recimg.img=self.record
                self.recimg.url=self.img;
                self.recimg.hid=self.record.id;
                self.record.save()
                self.recimg.save()

                self.is_img=False
            if self.theContent == 'title':
                self.record.name=self.titulo;
                self.record.save()
                #print self.titulo
            elif self.theContent == 'web':
                self.record.url=self.url
                self.record.save()
                #print self.url
            elif self.theContent == 'address':
                self.record.address=self.dir
                self.record.save()

                #print self.theContent
            self.theContent=""

            #record.save()
    def characters (self, chars):
        if self.theContent == 'phone':
            self.phone=chars
        if self.theContent == 'email':
            self.email=chars
        if self.theContent == 'body':
            self.body=chars

        if self.theContent == 'title':
            self.titulo=chars

        elif self.theContent == 'web':
            self.url=chars

        elif self.theContent == 'address':
            self.dir=chars

        elif self.theContent == 'url':
            self.img=chars
        elif self.theContent == 'item':
            self.tipo=chars
