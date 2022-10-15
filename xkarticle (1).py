import requests
import re

#url = input('url')
url = 'https://zujuan.xkw.com/thematiclist/11pt3201ct8113.html'
src = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}).text
# pat = re.compile(r'<article class="exam-cnt">[.|^.]*')
#result = pat.search(src)

print (src.find('<article class="exam-cnt">'))
print (src.find('</article>'))
result = (src[src.find('<article class="exam-cnt">'):src.find('</article>')+10])
#print (result)
with open('./output/test.html', 'w') as f:
	f.write(result)
