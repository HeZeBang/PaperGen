import json

with open('../downloads/test.json') as f:
	src = json.load(f)

try:
	title = src['data']['title']
except:
	title = input('试题名称：') or '试题'

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

otp = otp + '''
<!--button style=".noprint{visibility:hidden}" type="button" onclick="window.print()">
	Print PDF
</button-->
<p align='center' style="font-family: Tahoma, Geneva, sans-serif; font-size: 6px; font-weight: 300;">Github: HeZeBang/PaperGen</h2>
</html>'''

print(otp)
with open('./output/' + title + '.html','w', encoding = 'utf-8') as f:
	f.write(otp)

