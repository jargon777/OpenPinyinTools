# -*- coding: utf-8 -*-
'''
Created on Nov 26, 2015

                       Pinyin Sub Tools
Copyright (C) 2015  Matthew Muresan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License, version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Pinyin tone marker function comes from:
https://stackoverflow.com/questions/8200349/convert-numbered-pinyin-to-pinyin-with-tone-marks 

@author: Matthew Muresan
'''

#for traditional chinese subtitles at the moment. This script may not be reliable.

import sqlite3
import sys
import codecs
import os
import re
from string import punctuation
import unicodedata

PinyinToneMark = {
    0: "aoeiuv\u00fc",
    1: "\u0101\u014d\u0113\u012b\u016b\u01d6\u01d6",
    2: "\u00e1\u00f3\u00e9\u00ed\u00fa\u01d8\u01d8",
    3: "\u01ce\u01d2\u011b\u01d0\u01d4\u01da\u01da",
    4: "\u00e0\u00f2\u00e8\u00ec\u00f9\u01dc\u01dc",
}

def decode_pinyin(s):
    s = s.lower()
    r = ""
    t = ""
    for c in s:
        if c >= 'a' and c <= 'z':
            t += c
        elif c == ':':
            assert t[-1] == 'u'
            t = t[:-1] + "\u00fc"
        else:
            if c >= '0' and c <= '5':
                tone = int(c) % 5
                if tone != 0:
                    m = re.search("[aoeiuv\u00fc]+", t)
                    if m is None:
                        t += c
                    elif len(m.group(0)) == 1:
                        t = t[:m.start(0)] + PinyinToneMark[tone][PinyinToneMark[0].index(m.group(0))] + t[m.end(0):]
                    else:
                        if 'a' in t:
                            t = t.replace("a", PinyinToneMark[tone][0])
                        elif 'o' in t:
                            t = t.replace("o", PinyinToneMark[tone][1])
                        elif 'e' in t:
                            t = t.replace("e", PinyinToneMark[tone][2])
                        elif t.endswith("ui"):
                            t = t.replace("i", PinyinToneMark[tone][3])
                        elif t.endswith("iu"):
                            t = t.replace("u", PinyinToneMark[tone][4])
                        else:
                            t += "!"
            r += t
            t = ""
    r += t
    return r

def main():
    dbcon = sqlite3.connect("dict/dict.sqlite")
    dbcur = dbcon.cursor()
    rootdir = os.path.dirname(os.path.realpath(__file__))
    parsedir = rootdir + "/parse"
    writedir = rootdir + "/write"
    
    try:
        for i in os.listdir(parsedir):
            #SRT PARSE MODE
            if i.endswith(".srt"):
                writesrtln = ("00:00:00,500 --> 00:00:10,500", "PinYin Added with OpenPinyinTools")
                writesrttime = "00:00:00,500 --> 00:00:10,500"
                writesrttextCN = "拼音"
                writesrttextPY = "Pinyin Added with OpenPinyinTools"
                writesrtfile = []
                with open(parsedir + "/" + i, mode="r", encoding="utf8") as readfile:                         
                    for line in readfile:
                        if line.startswith(u'\ufeff'): #remove the BOM
                            line = line[1:]
                        if line.rstrip('\n').isdigit():
                            writesrtfile.append((writesrttime, writesrttextCN, writesrttextPY))
                            print(writesrttextCN, " → ", writesrttextPY)
                            writesrttime = False
                            writesrttextCN = ""
                            writesrttextPY = ""
                            
                        
                        #check for timestamp
                        elif ":" in line:
                            writesrttime = line.rstrip('\n')
                        
                        elif line.rstrip('\n') != "":
                            if writesrttextCN != "":
                                writesrttextCN += "\n"
                            writesrttextCN += re.sub('{.*?}', '', line.rstrip('\n')) 
                            writesrttextPY = ""
                            
                            basestr = writesrttextCN
                            while(len(basestr) > 0):
                                teststr = basestr
                                rowvalid = False
                                while(rowvalid==False):
                                    try:
                                        if teststr in punctuation:  
                                            break #punctuation so break and let if statement catch.
                                        elif teststr == "\n":
                                            break
                                        else:
                                            for row in dbcur.execute("SELECT * FROM dict WHERE trad = '%s'" % teststr):
                                                writesrttextPY = writesrttextPY + " " + re.sub(',.*$', '', re.sub('.*?:', '', decode_pinyin(row[2])))
                                                rowvalid = True
                                                break;
                                        
                                        if rowvalid:
                                            break
                                        if len(teststr) == 1:
                                            #we have failed to find it...
                                            break
                                        
                                        teststr = teststr[:-1] #shrink the teststring
        
                                    except:
                                        break 
                                if rowvalid == False:
                                    writesrttextPY = writesrttextPY + teststr
                                
                                basestr = basestr[len(teststr):]
                            
                            
                            
                                
                                
                print("Done converting. Writing")            
                with open(writedir + "/" + i, mode="w", encoding="utf8") as writefile:
                    varcount = 0
                    for entry in writesrtfile:
                        varcount += 1
                        writefile.write(str(varcount))
                        writefile.write("\n")
                        writefile.write(entry[0])
                        writefile.write("\n")
                        writefile.write(entry[1])
                        writefile.write("\n")
                        writefile.write(entry[2])
                        writefile.write("\n\n")
                dec = input("Done. Press Enter to Finish")
    except:
        print("An error has occured. You should check which files are being updated in this set \n")
        raise

if __name__ == "__main__":
    main()