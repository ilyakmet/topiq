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
		return get_request(url)
	except:
		print('vkapi_method error')
		return None

#get part of users in group
def groups_getMembers(groupid, offset):
	try:
		print(offset)
		f = open(DIR + groupid + '_usersdata.txt', 'a')
		for i in vkapi_method('groups.getMembers', {'group_id':groupid, 'offset': offset, 'count':1000})['response']['users']:
			f.write(str(i) + '\n')
		f.close()
		return 'susccess'
	except:
		print('groups_getMembers error')
		return None

#get full users list by group_id
def get_users_list_by_groupid(groupid):
	try:
		f = open(DIR + groupid + '_usersdata.txt', 'w')
		res = vkapi_method('groups.getMembers', {'group_id':groupid, 'offset': 0, 'count':1000})['response']
		for i in res['users']:
			f.write(str(i) + '\n')
		f.close()
		border  = res['count']
		print('Group count:' + str(border))

		#ThreadPool model
		offsets = [(groupid, x) for x in range(1000, border + 1, 1000)]
		def groups_getMembers_local(groupid_offset):
			return groups_getMembers(*groupid_offset)
			
		pool = ThreadPool(pool_number)
		pool.map(groups_getMembers_local, offsets)
		return 'susccess'
	except:
		print('get_users_list_by_groupid error')
		return None






