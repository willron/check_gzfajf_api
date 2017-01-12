#coding=utf-8
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import time
import receive
import reply
from check_gzfajf_api import check_gzfajf_api


# URL = 'http://bzflh.szjs.gov.cn/TylhW/lhmcAction.do?method=queryYgbLhmcList'
#
#
# def check_gzfajf_api(sfzh):
#     SFZH = sfzh
#     print SFZH
#     idcard = ''
#     xingm = ''
#     if len(SFZH) != 0:
#         SFZH = SFZH.strip().replace(',', ' ').replace(':', ' ').split()
#
#     waittype = '1' if str(SFZH[0]).lower() == 'ajf' else '2'
#     try:
#         for i in SFZH:
#             if re.match(r'\d{17}[\dxX]', i):
#                 idcard = i
#             else:
#                 if re.match(r'gzf|ajf', i, re.IGNORECASE):
#                     pass
#                 else:
#                     xingm = i
#     except IndexError:
#         return 2
#     if idcard == '':
#         return 3
#     postdata = {'pageNumber': '1', 'pageSize': '10', 'waittype': waittype, 'xingm': xingm, 'idcard': idcard, 'shoulbahzh': ''}
#     print postdata
#     req = requests.post(url=URL, data=postdata)
#     req_json = json.loads(req.text)
#     if req_json['total'] != 0:
#         return str(req_json['rows'][0]['PAIX'])
#     return 1

@csrf_exempt  
def test(request):
    if request.method == 'GET':
        print 'i am get'
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        
        token = '20121225zxplovezyh1314'
        
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        
        hashstr = ''.join([s for s in hashlist])
        
        hashstr = hashlib.sha1(hashstr).hexdigest()
        
        if hashstr == signature:
            return HttpResponse(echostr)

    else:
        #print 'i am port', request.body
        msgReceive = receive.parse_xml(request.body)
        # str_xml = ET.fromstring(request.body)
        # fromUser = str_xml.find('ToUserName').text
        # toUser = str_xml.find('FromUserName').text
        # content = str_xml.find('Content').text
        
        nowtime = str(int(time.time()))
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{rep[ToUserName]}]]></ToUserName>
        <FromUserName><![CDATA[{rep[FromUserName]}]]></FromUserName>
        <CreateTime>{rep[CreateTime]}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{rep[Content]}]]></Content>
        </xml>
        """
        if msgReceive.MsgType == 'text':
            paiming = check_gzfajf_api(msgReceive.Content)
        if not isinstance(paiming, int):
            msgReceive.Content = paiming
        else:
            msgReceive.Content = '请提供正确的身份证号' if paiming == 3 \
                else '查询不到信息' if paiming == 1 \
                else '请以 ajf,身份证号 或 gzf,身份证号 为输入格式' if paiming == 4 \
                else '输入有误'

        msgReceive.CreateTime = nowtime
        if paiming is not False:
            c = {'ToUserName': msgReceive.FromUserName, 'FromUserName': msgReceive.ToUserName, 'CreateTime': nowtime, 'Content': paiming}
            return HttpResponse(XmlForm.format(rep=msgReceive.__dict__))
        else:
            return HttpResponse('')
