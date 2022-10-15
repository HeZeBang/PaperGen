import json
import urllib.request
import urllib.parse
import re
import requests

jsonpth = './downloads/test.json'
subid = input('输入学科编号: ')
srcapi='https://zjappserver.xkw.com/app-server/v1/ques/detail/11/{}?browserWidth=800'
apih={'zjapp-check':
'1664877770||android||zj.app||63dd00ea7f9abc3a94ae6b9ebf536a66fadfb6f29023abdacd48f9d21520a765',
'authToken':
'8Iw3ids/wAis8rQrOScGN56xg/89g2c+q24tmPSfOA9CCIGZ2tdjBWgq3zu1+dxvrb4nlGZD9Gujff9xuw+WlN+xztWd4QoVqtaoGF/PxIR1kqpQPDJiUbRJx1wi9tP9rI+LWqdrZOzgTUEQssRC53aimQ4Gzhh16vZhA7+Q24o=',
'User-Agent':'okhttp/3.14.9'
}
print (apih)
txtlist = []
id = input('输入id获取试题')

if(id):
	src = json.loads(requests.get('https://zjappserver.xkw.com/app-server/v1/special/' + id, headers = apih).text)
else:
	with open(jsonpth) as f:
		src = json.load(f)

print(src['msg'])

try:
	title = src['data']['title']
except:
	title = input('试题名称：') or '试题'

print(title)
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
img{{max-width: 100%; }}
</style>
</head>
<h1>{}</h1>
<p onclick="window.print()" style="font-family: Tahoma, Geneva, sans-serif; font-size: 12px; font-weight: 100;">Powered by PaperGen/ZAMBAR</h2>
'''.format(title, title)

if type(src['data']) != list:
	src['data'] = [src['data'].copy()]

for ques in src['data']:
	if 'name' in ques:
		otp = otp + '''
<div style="font-size: 12px; font-weight: 900">{}部分</div><hr>
'''.format(ques['name'])
	for item in ques.get('list', ques.get('quesList')):
		idx = idx + 1
		txtlist.append(item.get('id',0))
		otp = otp + '''
<div class="qml-ques">
<div style="font-size: 10px; font-weight: 700">{}.[{}/{}]</div>
<div style="font-size: 8px"><i>{}|{} 知识点|{}</i></div>
<div clsss="ques-stem">{}</div>{}
</div>
'''.format(idx, item['type']['name'], 
	item['title'], item['diff']['name'], item['diff']['value'], 
	item['knowledgeInfo'], item['body'].replace('【题文】', ''), 
	'' if item['type']['id'] != 2703 else '<p style="margin:150px">&zwnj;</p>')

print(txtlist)
with open('./output/' + title + '.html','w', encoding = 'utf-8') as f:
	f.write(otp)

idx = 0
if (input('是否查找答案 y/n') == 'y'):
	otp = '<h1>{}–答案部分</h1>'.format(title)
	for item in txtlist:
		idx=idx+1
		print ('请求{}题答案'.format(idx))
		result = json.loads(requests.get(url=srcapi.format(item), headers=apih).text)
		print (result['msg'])
		otp = otp + '''<h2>第{}题</h2>
<img style="width: 100%; margin: 0mm" src="{}"/>
<img style="width: 100%; margin: 0mm" src="{}"/>
'''.format(idx, result['data']['answerImg'], result['data']['parseImg'])

otp = otp + '''<!--button style=".noprint{visibility:hidden}" type="button" onclick="window.print()">Print PDF</button--><p align='center' style="font-family: Tahoma, Geneva, sans-serif; font-size: 6px; font-weight: 300;">Github: HeZeBang/PaperGen</h2></html>'''

with open('./output/' + title + ('_xk答案版' if idx else '') +'.html','w', encoding = 'utf-8') as f:
	f.write(otp)
