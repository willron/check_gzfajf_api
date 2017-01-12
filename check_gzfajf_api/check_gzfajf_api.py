#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
import json
import re
'''
by:willron
'''
__author__ = 'zxp'
cici_cici
URL = 'http://bzflh.szjs.gov.cn/TylhW/lhmcAction.do?method=queryYgbLhmcList'


def check_gzfajf_api(sfzh):
    SFZH = sfzh
    idcard = ''
    xingm = ''
    if not (SFZH.startswith('ajf') or SFZH.startswith('gzf')):
        return 4
    if len(SFZH) != 0:
        SFZH = SFZH.strip().replace(',', ' ').replace(':', ' ').split()
    else:
        return 2


    waittype = '1' if str(SFZH[0]).lower() == 'ajf' else '2'
    try:
        for i in SFZH:
            if re.match(r'\d{17}[\dxX]', i):
                idcard = i
            else:
                if re.match(r'gzf|ajf', i, re.IGNORECASE):
                    pass
                else:
                    xingm = i
    except IndexError:
        return 2
    if idcard == '':
        return 3
    postdata = {'pageNumber': '1', 'pageSize': '10', 'waittype': waittype, 'xingm': xingm, 'idcard': idcard, 'shoulbahzh': ''}
    req = requests.post(url=URL, data=postdata)
    req_json = json.loads(req.text)
    if req_json['total'] != 0:
        return str(req_json['rows'][0]['PAIX'])
    return 1

