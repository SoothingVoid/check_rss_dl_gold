import requests
from bs4 import BeautifulSoup
import urllib.request
import wget
#from xmldiff import main, formatting
import hashlib
import datetime;
import os

import my_params #import all private values

my_script_dir = os.path.dirname(__file__)

# Input parameters // Here you fill the secret values
my_login = my_params.my_login
my_passw = my_params.my_passw
my_passkey = my_params.my_passkey
f_torrent_dl = my_params.f_torrent_dl
url_base = my_params.url_base

# Script parameters
url_login = url_base+'/takelogin.php'
url_rss = url_base + '/rssdl.php?passkey=' + my_passkey

f_rss_prev_hex = my_script_dir +'/'+'rss_prev_ver.txt'
f_torrent_url_history = my_script_dir +'/'+'used_url_history.txt'
f_rss_last_check = my_script_dir +'/'+'rss_last_check.'
#check RSS that there are any changes
rss_resp = requests.get(url_rss)

# Fill in your details here to be posted to the login form.
url_login_payload = {
    'username': my_login,
    'password': my_passw,
    'returnto': '/browse_old.php?search=&incldead=0&sgold=on'
}

def is_rss_updated():
    # Function to check to detect if rss page has been changed
	ret_val = bool(False)
	with open(f_rss_prev_hex, 'r') as file:
		rss_old_hex = file.read()

	rss_new_hex = hashlib.sha224(rss_resp.text.encode("utf-8")).hexdigest()
	#print (rss_old_hex)
	#print (rss_new_hex)
	if rss_old_hex != rss_new_hex:
		print('RSS Update detected.')
		ret_val = bool(True)
		with open(f_rss_prev_hex, 'w') as file:
            		file.write(rss_new_hex)
	return ret_val

def get_fano_gold_torrents():
	# Use 'with' to ensure the session context is closed after use.
	with requests.Session() as s:
		p = s.post(url_login, data=url_login_payload, verify=False)
		# print the html returned or something more intelligent to see if it's a successful login page.
		#print (p.text.encode("utf-8"))
		bs = BeautifulSoup(p.text.encode("utf-8"))
		#htmltable = bs.find('table', { 'class' : 'torrenttable' })
		#htmltablerows = htmltable.find_all('tr', {'class': ''})

	find_all_id = bs.find_all(id='a_down')
	with open(f_torrent_url_history) as f:
		dl_lines = [line.rstrip('\n') for line in f]
	dl_lines.reverse()
	#print(*dl_lines, sep = '\n')

	#getting value
	for i in find_all_id:
		if i.get('href') not in dl_lines:
			print('DOWNLOADING: '+i.get('href'))
			#print('URL: '+ url_base + '/' + i.get('href') +'&passkey=' + my_passkey)
			wget_response = wget.download(url_base + '/' + i.get('href') +'&passkey=' + my_passkey, out = f_torrent_dl)
			#print('wget')
			with open(f_torrent_url_history, 'a') as file:
				file.write(i.get('href')+'\n')

print("RSS checked: ", datetime.datetime.now())
with open(f_rss_last_check, 'w') as file:
	file.write('RSS checked: '+ str(ct) + '\n')

if is_rss_updated():
	print('is_rss_updated() = True')
	get_fano_gold_torrents()
else:
	print('is_rss_updated() = False')
