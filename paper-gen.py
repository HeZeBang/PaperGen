import json
import time
import requests
import urllib.request
import urllib.parse
import re

jsonpth = './downloads/test.json'
srcapi = 'https://graph.baidu.com/s?sign=00000000000000000000000000000000&f=question&more_question=0&extUiData[mode]=text&extUiData[query]='
apih={'zjapp-check':
str(time.time())+'||android||zj.app||63dd00ea7f9abc3a94ae6b9ebf536a66fadfb6f29023abdacd48f9d21520a765',
'authToken':
'8Iw3ids/wAis8rQrOScGN52D1l9q2N+8pDRe6jMymLBCCIGZ2tdjBWgq3zu1+dxvzriIvwf+hmWomXJLjl3rgFWV2f6P1J+QMEBDL2KBZMt1kqpQPDJiUbRJx1wi9tP9rI+LWqdrZOzgTUEQssRC53aimQ4Gzhh16vZhA7+Q24o='
}
print (apih)
txtlist = []

if(input('是否从apih获取试题篮? y/n ') == 'y'):
	src = json.loads(requests.get('https://zjappserver.xkw.com/app-server/v1/basket/' + input('输入学科编号:'), headers = apih).text)
else:
	with open(jsonpth) as f:
		src = json.load(f)

print(src['msg'])

try:
	title = src['data']['title']
	partitle = src['data'].get('parentTitle', 'PaperGen - {}'.format(time.strftime("%Y-%m-%d", time.localtime())))
	explain = src['data'].get('explain')
	print (title)
except:
	partitle = 'PaperGen - {}'.format(time.strftime("%Y-%m-%d", time.localtime()))
	title = input('试题名称：') or '试题'
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
	for item in ques.get('list', ques.get('quesList')):
		idx = idx + 1
		txtlist.append(re.sub(r'<.*?>', '', 
			item['body']
			.replace('【题文】','')
			.replace('&nbsp',''))[:15])
		otp = otp + '''{}
<div class="qml-ques">
<div style="font-size: 10px; font-weight: 700">{}.[{}/{}]</div>
<div style="font-size: 8px"><i>{}|{} 知识点|{}</i></div>
<div clsss="ques-stem">{}</div>{}
</div>
'''.format(item.get('frontExplain', ''), idx, item['type']['name'], 
	item['title'], item['diff']['name'], item['diff']['value'], 
	item['knowledgeInfo'], item['body'].replace('【题文】', ''), 
	'' if item['type']['id'] != 2703 else '<p style="margin:150px">&zwnj;</p>')

otp = otp + '''
<!--button style=".noprint{visibility:hidden}" type="button" onclick="window.print()">
	Print PDF
</button-->
<p align='center' style="font-family: Tahoma, Geneva, sans-serif; font-size: 6px; font-weight: 300;">Github: HeZeBang/PaperGen</h2>
</html>'''

print(txtlist)
with open('./output/' + title + '.html','w', encoding = 'utf-8') as f:
	f.write(otp)

idx = 0
if (input('是否查找答案 y/n') == 'y'):
	for item in txtlist:
		idx=idx+1
		url = srcapi+(urllib.parse.quote(item.replace('_','')))
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
