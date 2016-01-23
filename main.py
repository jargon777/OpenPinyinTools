# coding: utf-8
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

@author: Matthew Muresan
'''
import sqlite3
import sys
import codecs
import os
import re
from string import punctuation

def main():
    dbcon = sqlite3.connect("dict/hanzi.sqlite")
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
                        #check first for the number.
                        if line.rstrip('\n').isdigit():
                            writesrtfile.append((writesrttime, writesrttextCN, writesrttextPY))
                            print(writesrttextCN, " → ", writesrttextPY)
                            writesrttime = False
                            writesrttextCN = False
                            writesrttextPY = False
                            
                        
                        #check for timestamp
                        elif ":" in line:
                            writesrttime = line.rstrip('\n')
                        
                        elif line.rstrip('\n') != "":
                            writesrttextCN = re.sub('{.*?}', '', line.rstrip('\n')) 
                            writesrttextPY = ""
                            for cp in writesrttextCN:
                                try:
                                    if cp in punctuation:
                                        writesrttextPY = writesrttextPY + cp                      
                                    else:
                                        rowvalid = False
                                        for row in dbcur.execute("SELECT * FROM dict WHERE hanzi = '%s'" % cp):
                                            writesrttextPY = writesrttextPY + " " + re.sub(',.*$', '', re.sub('.*?:', '', row[1]))
                                            rowvalid = True
                                        if rowvalid == False:
                                            writesrttextPY = writesrttextPY + cp    
                                except:
                                    pass 
                                
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
    except:
        print("An error has occured. You should check which files are being updated in this set \n")
        raise
if __name__ == "__main__":
    main()