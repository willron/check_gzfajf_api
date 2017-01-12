#coding=utf-8
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import time
import receive
import reply
from check_gzfajf_api import check_gzfajf_api


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
        print 'i am port', request.body
        msgReceive = receive.parse_xml(request.body)

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
            print 'return msg:', paiming
        if not isinstance(paiming, int):
            msgReceive.Content = paiming
        else:
            msgReceive.Content = '请提供正确的身份证号' if paiming == 3 \
                else '查询不到信息' if paiming == 1 \
                else '请以 ajf,身份证号 或 gzf,身份证号 为输入格式' if paiming == 4 \
                else '输入有误'

        msgReceive.CreateTime = nowtime
        if paiming is not False:
            print XmlForm.format(rep=msgReceive.__dict__)
            return HttpResponse(XmlForm.format(rep=msgReceive.__dict__))
        else:
            return HttpResponse('')
