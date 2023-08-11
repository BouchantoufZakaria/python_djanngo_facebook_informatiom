

from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup as bs
import re
import json

url='https://n.facebook.com'
xurl=url+'/login.php'
ua="Mozilla/5.0 (Linux; Android 4.1.2; GT-I8552 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
#ua="Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36'"
def login(userE,pas):
	try:
		user=userE
		pswd=pas
		req=requests.Session()
		req.headers.update({
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,ima`ge/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-language': 'en_US','cache-control': 'max-age=0',
		'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
		'sec-ch-ua-mobile': '?0','sec-ch-ua-platform': "Windows",
		'sec-fetch-dest': 'document','sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1',
		'user-agent': ua})
		with req.get(url) as response_body:
			inspect=bs(response_body.text,'html.parser')
			lsd_key=inspect.find('input',{'name':'lsd'})['value']
			jazoest_key=inspect.find('input',{'name':'jazoest'})['value']
			m_ts_key=inspect.find('input',{'name':'m_ts'})['value']
			li_key=inspect.find('input',{'name':'li'})['value']
			try_number_key=inspect.find('input',{'name':'try_number'})['value']
			unrecognized_tries_key=inspect.find('input',{'name':'unrecognized_tries'})['value']
			bi_xrwh_key=inspect.find('input',{'name':'bi_xrwh'})['value']
			data={
			'lsd':lsd_key,'jazoest':jazoest_key,
			'm_ts':m_ts_key,'li':li_key,
			'try_number':try_number_key,
			'unrecognized_tries':unrecognized_tries_key,
			'bi_xrwh':bi_xrwh_key,'email':user,
			'pass':pswd,'login':"submit"}
			response_body2=req.post(xurl,data=data,allow_redirects=True,timeout=300)
			cookie=str(req.cookies.get_dict())[1:-1].replace("'","").replace(",",";").replace(":","=")
			if 'checkpoint' in cookie :
				return 'Account terminat ed by Facebook! '
			
			elif 'c_user' in cookie :
				pattern = r'(\w+)\s*=\s*([^;]+)'
				matches = re.findall(pattern, cookie)
				# Create a dictionary from the extracted key-value pairs
				data_dict = {key: value for key, value in matches}           
				cookies = json.dumps(data_dict, indent=2)
				return cookies
			else:
				return "wrong detail"
	except:
	    pass
	

def Acc(acc):
    try :
        cookies = json.loads(acc)
        data = requests.get('https://business.facebook.com/business_locations', headers = {
                    'user-agent'                : 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36', # don't change this user agent.
                    'referer'                   : 'https://www.facebook.com/',
                    'host'                      : 'business.facebook.com',
                    'origin'                    : 'https://business.facebook.com',
                    'upgrade-insecure-requests' : '1',
                    'accept-language'           : 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                    'cache-control'             : 'max-age=0',
                    'accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'content-type'              : 'text/html; charset=utf-8'
                }, cookies=cookies)
        
        my_string = data.text
        
        start_index = my_string.find("EAAG")  # find the index of "EAAG" in the string
        
        for i in range(start_index, len(my_string)):
            substring = my_string[start_index:i+1]  # extract the substring from the start index to the current loop index
            
            if '"' in substring:
                substring = substring.replace('"', '')  # remove the double quote from the substring
                break  # if the double quote is found, break out of the loop
            
        return substring# print
    except:
        pass

def index(request):
    username = request.GET.get('user', None)
    password = request.GET.get('pass',None )
    
    if username  is not None and password is not None  :
	    cookie = login(username,password)
	    AccessToken = Acc(cookie)
	    info = {
		    	'cookie':cookie,
	     		'access':AccessToken
				}
	    
	    acount = json.dumps(info,indent=4)
	    return HttpResponse(acount)
    else:
        return HttpResponse('you do not provide any information of the facebook account !')

