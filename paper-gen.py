import json
import time
import requests
import uuid
import urllib.parse
import re
import hashlib

__version__ = '1.0'
__author__  = 'ZAMBAR'
__debugMode__ = True
jsonpth = './test.json'

id = 11
apih={}
txtlist = []
idlist = []
otp = ''
title = ''

def debug(text):
	if(debug):
		print(text)

def authInit():
	try:
		apih=json.load(open('auth.ini'))
		res = requests.get('https://zjappserver.xkw.com/app-server/gateway/v1/basic/refreshToken', headers = apih, params = json.dumps({'refreshToken':apih.get('refreshToken')}).replace(' ', '')).json()
		print (res)
		print(json.dumps({'refreshToken':apih.get('refreshToken')}))
		apih['authToken'] = res.get('authToken') or apih['authToken']
	except:
		apih={'zjapp-check':
	'1663476130||android||zj.app||c7501df5a8e48b3e09cd733be97cce8e02728c2128f43e16b508ccd069db0a7f',
	'authToken':
	'8Iw3ids/wAis8rQrOScGN56xg/89g2c+q24tmPSfOA9CCIGZ2tdjBWgq3zu1+dxvrb4nlGZD9Gujff9xuw+WlN+xztWd4QoVqtaoGF/PxIR1kqpQPDJiUbRJx1wi9tP9rI+LWqdrZOzgTUEQssRC53aimQ4Gzhh16vZhA7+Q24o=',
	'User-Agent':'okhttp/3.14.9'
	}
	debug(apih)
	print ('当前登录用户：{}'.format((requests.get('https://zjappserver.xkw.com/app-server/v1/user/info', headers = apih).json().get('data') or {}).get('username')))
	return apih
	

def anlyRes(arg, subid):
	if(arg):
		pattern = re.compile(r'[0-9]+')
		res = pattern.findall(arg)
		debug(res)
		subid = int(res[0])
		if len(res) >= 4:
			src = requests.get('https://zjappserver.xkw.com/app-server/v1/special/{}/{}'.format(res[1], res[3]), headers = apih).json()
		elif len(res)>=2:
			src = requests.get('https://zjappserver.xkw.com/app-server/v1/paper/detail/{}/{}'.format(res[0], res[1]), headers = apih).json()
		else:
			src = requests.get('https://zjappserver.xkw.com/app-server/v1/ques/detail/11/{}?browserWidth=800'.format(res[0])).json()
	else:
		src = json.loads(requests.get('https://zjappserver.xkw.com/app-server/v1/basket/' + subid, headers = apih).text)
	print(src['msg'])
	print('共{}题'.format(json.dumps(src).count('body')))
	return src



def fetchList(src):
	try:
		title = src['data']['title']
		partitle = src['data'].get('parentTitle', 'PaperGen - {}'.format(time.strftime("%Y-%m-%d", time.localtime())))
		explain = src['data'].get('explain', '')
		print (title)
	except:
		partitle = 'PaperGen - {}'.format(time.strftime("%Y-%m-%d", time.localtime()))
		title = (input('试题名称：') if __name__ == "__main__" else None) or '试题'
		explain = ''

	idx = 0
	otp = '''
	<!DOCTYPE html>
	<html>
	<head>
	<title>{}</title>
	<meta charset="UTF-8" />
	<link rel="stylesheet" href="https://open.xkw.com/html-render-resource/preview.css" type="text/css" />
	<style>
	@ page {{
		margin: 4mm 10mm 10mm;
		size: 100mm 297mm
	\}}
	</style>
	</head>
	<h3>{}</h3>
	<h1>{}</h1>
	<p onclick="window.print()" style="font-family: Tahoma, Geneva, sans-serif; font-size: 12px; font-weight: 100;">Powered by PaperGen/ZAMBAR</h2>
	'''.format(title, partitle, title)
	otp = otp + explain
	if type(src['data']) != list:
		src['data'] = [src['data'].copy()]
	for ques in src['data']:
		if 'name' in ques:
			otp = otp + '''
<div style="font-size: 12px; font-weight: 900">{}部分</div><hr>
'''.format(ques['name'])
		for item in ques.get('list', ques.get('quesList', [ques])):
			idx = idx + 1
			idlist.append(item.get('id',0))
			txtlist.append(re.sub(r'<.*?>', '', 
				item['body']
				.replace('【题文】','')
				.replace('&nbsp','')))
			otp = otp + '''{}
	<div style="font-size: 10px; font-weight: 700">{}.[{}/{}]</div>
	<div style="font-size: 8px"><i>{}|{} 知识点|{}</i></div>
	<div class="qml-ques">
	<div clsss="ques-stem">{}</div>{}
	</div>
	'''.format(item.get('frontExplain', ''), idx, item['type']['name'], 
		item['title'], item['diff']['name'], item['diff']['value'], 
		item['knowledgeInfo'], item['body'].replace('【题文】', ''), 
	'' if item['type']['id'] != 2703 else '<p style="margin:150px">&zwnj;</p>')
	otp = otp + '''<p align='center' style="font-family: Tahoma, Geneva, sans-serif; font-size: 6px; font-weight: 300;">Github: HeZeBang/PaperGen</h2>
</html>'''
	if __name__ == "__main__":
		with open(r'./output/' + title + '.html', 'w', encoding = 'utf-8') as f:
			f.write(otp)
	return {"title":title,
			"idlist":idlist,
			"txtlist":txtlist,
			"otp":otp}

def output(name, otp):
	with open(r'./output/' + name + '.html', 'w', encoding = 'utf-8') as f:
		f.write(otp)

def ansGen(isId, title, list):
	if not isId:
		srcapi = 'https://graph.baidu.com/s?sign=00000000000000000000000000000000&f=question&more_question=0&extUiData[mode]=text&extUiData[query]='
		idx = 0
		otp = '<h1>{}–答案部分</h1>'.format(title)
		debug(list)
		for item in list:
			idx= idx + 1
			url = srcapi + (urllib.parse.quote(item.replace('_','')))
			otp = otp + "<h2>{}</h2><hr>".format(idx)
			htm = requests.get(url).text
			pat = re.compile('<img.*?/>')
			result = pat.findall(htm)
			print (result)
			for i in result:
				otp = otp + '{}'.format(i.replace('\\',''))
			print ('已找到{}题答案'.format(idx))
		with open('./output/' + title + ('_答案版' if idx else '') + '.html','w', encoding = 'utf-8') as f:
			f.write(otp)
	else:
		srcapi='https://zjappserver.xkw.com/app-server/v1/ques/detail/11/{}?browserWidth=800'
		idx = 0
		otp = '<h1>{}–答案部分</h1>'.format(title)
		for item in list:
			idx=idx+1
			print ('请求{}题答案'.format(idx))
			result = json.loads(requests.get(url=srcapi.format(item), headers=apih).text)
			print (result['msg'] if result.get("data",{}).get("answerImg") else "答案为空")
			otp = otp + '''<h2>第{}题</h2>
	<img style="width: 100%; margin: 0mm" src="{}"/>
	<img style="width: 100%; margin: 0mm" src="{}"/>
	'''.format(idx, result.get("data",{}).get("answerImg"), result.get("data",{}).get("parseImg"))

		with open('./output/' + title + ('_答案版' if idx else '') +'.html','w', encoding = 'utf-8') as f:
			f.write(otp)

def login(phnum, code, isSMS):
	key = str(uuid.uuid1()).replace('-','')
	hds = {
'zjapp-check': str(int(time.time())-1000) + '||android||zj.app||' + key,
'User-Agent': 'okhttp/3.14.9',
'Accept':'application/json',
'Content-Type':'application/json; charset=UTF-8'
}
	debug(hds)
	if(isSMS):
		if(code):#SMS LOGIN
			bdy = '{{"phone":"{}","terminal":"app","validateCode":"{}"}}'.format(str(phnum), str(code))
			ret = requests.post('https://zjappserver.xkw.com/app-server/v1/user/loginByPhone', headers = hds, data = bdy)
			res = ret.headers
			print(ret.json().get('msg'))
			hds['authToken'] = res.get('authToken')
			hds['refreshToken'] = res.get('refreshToken')
			print('Welcome ' + str(ret.json().get('data',{}).get('username')))
			return hds
		else:#SEND CODE
			bdy = '{{"phone":"{}","templateType":"LOGIN"}}'.format(str(phnum))
			print(requests.post('https://zjappserver.xkw.com/app-server/v1/user/sendSmsCode', headers = hds, data = bdy).json().get('msg','错误'))
			return None
	else:#PWD LOGIN
		bdy = '{{"password":"{}","terminal":"app","userName":"{}"}}'.format(str(hashlib.md5(code.encode(encoding='UTF-8')).hexdigest()),str(phnum))
		ret = requests.post('https://zjappserver.xkw.com/app-server/v1/user/loginByUserName', headers = hds, data = bdy)
		print(ret.json().get('msg'))
		res = ret.headers
		hds['authToken'] = res.get('authToken')
		hds['refreshToken'] = res.get('refreshToken')
		print('Welcome ' + str(ret.json().get('data',{}).get('username')))
		return hds


def main():
	sbj = re.compile(r'"id":(.*?),"name":"(.*?),').findall(requests.get('https://zjappserver.xkw.com/app-server/v1/basicData/subjects').text)
	print(sbj)
	if(input("重新登录账户？ y/N")=="y"):
		phnum = input("手机号：")
		if(input("用短信登录吗？ y/N")=="y"):
			login(phnum, None,1)
			hds = login(phnum, input("验证码："),1)
		else:
			hds = login(phnum, input("密码："),0)
		debug(hds)
		with open('auth.ini', 'w') as f:
			f.write(json.dumps(hds))
	authInit()
	ret = fetchList(anlyRes(input('输入链接/试题id获取试题，留空从试题篮获取 '), input('输入学科id ')))
	debug(ret)
	if(input("是否从百度获取答案？ y/N ")=="y"):
		ansGen(0, ret.get("title"), ret.get("txtlist"))
	if(input("是否从主站获取答案？（免费用户30题/日） y/N ")=="y"):
		ansGen(1, ret.get("title"), ret.get("idlist"))


if __name__ == "__main__" :
	main()
