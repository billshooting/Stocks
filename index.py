#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import sys
import json
import requests
import re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

fundsSettingPath = "./funds.json"
dataPath = "test.html"
dataUrl = "http://fund.eastmoney.com/%s.html"
encoding = 'utf-8'
codeNameDic = {}
codeRateDic = {}

def loadFunds():
    with open(fundsSettingPath, 'r', encoding="utf-8") as file :
        setting = json.load(file)
        fundsInfo = setting["funds"]
        funds = []
        for info in fundsInfo:
            funds.append(info["code"])
        return funds

def getFundData(code):
    url = dataUrl % (code)
    res = requests.get(url)
    return res

def parseHtml(html):
    li = re.findall(r'<li class=\'position_shares\' id=\'position_shares\'.*?</li>', html)
    gourps = re.findall(r'<td class="alignLeft">\s+<a href="http://quote.eastmoney.com/.*?>(.*?)</a>\s+</td>\s+<td class="alignRight bold">(.*?)</td>  <td class="alignRight bold" stockcode="stock_(.*?)">', li[0])
    return gourps

def getFundsData():
    funds = loadFunds()
    for fund in funds:
        res = getFundData(fund)
        global encoding
        encoding = res.encoding
        data = parseHtml(res.text)
        for d in data:
            codeNameDic[d[2]] = d[0]
            rate = codeRateDic.get(d[2], 0)
            codeRateDic[d[2]] = rate + float(d[1].strip('%'))

def sortRate():
    array = []
    for key in codeRateDic.keys():
        array.append((key, codeRateDic[key]))
    return sorted(array, key=lambda ele: ele[1], reverse=True)
    #return array

getFundsData()
sortedRate = sortRate()

with open('./data.csv', 'w', encoding=encoding) as file:
    for d in sortedRate:
        file.write("%s,%s,%s\r" % (d[0], codeNameDic[d[0]], round(d[1], 2)))