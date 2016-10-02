# -*- coding: utf-8 -*-
import urllib, os, requests, random#, logging
from multiprocessing.dummy import Pool as ThreadPool
#logging.basicConfig(level=logging.DEBUG)

DIR = os.path.abspath(os.curdir) + '/'
pool_number = 10



#get random proxy from proxy.txt
def get_random_proxy():
	try:
		return random.choice(open('proxy.txt', 'r').readlines())
	except:
		print('get_random_proxy error')
		return None

#generate url by parameters
def create_api_url(method, parameters={}):
	try:
		return 'https://api.vk.com/method/' + method + '?' + urllib.urlencode(parameters)
	except:
		print('create_api_url error')
		return None

#create request by url
def get_request(url):
	try:
		random_proxy = get_random_proxy()
		#print(random_proxy)
		return requests.get(url, proxies={'http':random_proxy}).json()
	except:
		print('get_request error')
		return None

#create vkapi request by method_name and parameters
def vkapi_method(method, parameters={}):
	try:
		url = create_api_url(method, parameters)
		#print(url)
		return get_request(url)['response']
	except:
		print('vkapi_method error')
		return None

#get part of users in group
def groups_getMembers(groupid, offset):
	try:
		print(offset)
		f = open(DIR + groupid + '_usersdata.txt', 'a')
		for i in vkapi_method('groups.getMembers', {'group_id':groupid, 'offset': offset, 'count':1000})['users']:
			f.write(str(i) + '\n')
		f.close()
		return 'susccess'
	except:
		print('groups_getMembers error')
		return None

#get list of groups by substring
def groups_search(substring, access_token, filename='', grouptype='', countryid='', cityid='', future='', market='', sort=0, count=10):
	try:
		if filename == '':
			fname = substring
		else:
			fname = filename
		f = open(DIR + fname + '.txt', 'a')
		for i in vkapi_method('groups.search', {'access_token':access_token, 'q':substring, 'type':grouptype, 'country_id':countryid, 'ciy_id':cityid, 'future':future, 'market':market, 'sort':sort, 'count':count})[1:]:
			#print(i['gid'])
			f.write(str(i['gid']) + '\n')
		f.close()
		return 'susccess'
	except:
		print('groups_search error')
		return None



#===========================================================================================================MAIN FUNCTIONS
#get full users list by group_id
def get_users_list_by_groupid(groupid):
	try:
		#in first step get 1000 users id and count of group (border)
		f = open(DIR + groupid + '_usersdata.txt', 'w')
		res = vkapi_method('groups.getMembers', {'group_id':groupid, 'offset': 0, 'count':1000})
		for i in res['users']:
			f.write(str(i) + '\n')
		f.close()
		border  = res['count']
		print('Group count:' + str(border))

		#ThreadPool model
		offsets = [(groupid, x) for x in range(1000, border+1, 1000)]
		def groups_getMembers_local(groupid_offset):
			return groups_getMembers(*groupid_offset)
			
		pool = ThreadPool(pool_number)
		pool.map(groups_getMembers_local, offsets)
		return 'susccess'
	except:
		print('get_users_list_by_groupid error')
		return None
		
#get group list by substrings and parameters
def get_groups_list(substrings, access_token, filename='', grouptype='', countryid='', cityid='', future='', market='', sort=0, count=10):
	try:
		fname = substrings[:50]
		open(DIR + fname + '.txt', 'w')
		substrings_list = substrings.split(',')
		for string in substrings_list:
			print(string)
			groups_search(string, access_token, fname, grouptype, countryid, cityid, future, market, sort, count)
		return 'susccess'
	except:
		print('get_groups_list error')
		return None








