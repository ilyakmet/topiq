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

#https://vk.com/dev/groups.getMembers
def groups_getMembers(groupid='', offset=0, sort='', count=1000, fields='', filter_=''):
	try:
		print(offset)
		f = open(DIR + groupid + '_usersdata.txt', 'a')
		res = vkapi_method('groups.getMembers', {'group_id':groupid, 'offset': offset, 'count':count, 'sort':sort, 'fields':fields, 'filter':filter_})
		for i in res['users']:
			f.write(str(i) + '\n')
		f.close()
		return res['count']
	except:
		print('groups_getMembers error')
		return None

#https://vk.com/dev/groups.search
def groups_search(q, access_token, filename='', type_='', country_id='', city_id='', future='', market='', offset=0, sort=0, count=1000):
	try:
		if filename == '':
			fname = q
		else:
			fname = filename
		f = open(DIR + fname + '.txt', 'a')
		for i in vkapi_method('groups.search', {'access_token':access_token, 'q':q, 'type':type_, 'country_id':country_id, 'ciy_id':city_id, 'future':future, 'market':market, 'sort':sort, 'count':count, 'offset':offset})[1:]:
			#print(i['gid'])
			f.write(str(i['gid']) + '\n')
		f.close()
		return 'susccess'
	except:
		print('groups_search error')
		return None
		
#https://vk.com/dev/wall.get
def wall_get(access_token='', owner_id='', domain='', count=1000, extended='', fields='', offset=0, filter_='owner', likes=None, reposts=None, comments=None):
	try:
		print(offset)
		filename = max(owner_id, domain)
		f = open(DIR + filename + '_posts.txt', 'a')
		res = vkapi_method('wall.get', {'owner_id':owner_id, 'domain':domain, 'count':count, 'extended':extended, 'fields':fields, 'offset':offset, 'filter':filter_, 'access_token':access_token})
		for i in res[1:]:
			if i['likes']['count'] >= likes and i['reposts']['count'] >= reposts and i['comments']['count'] >= comments:
				f.write(str(i['likes']['count']) + ',' + str(i['id']) + ',' + str(i['date']) + '\n')
		f.close()
		return res[0]
	except:
		print('wall_get error')
		return None




#===========================================================================================================MAIN FUNCTIONS
#get full users list by group_id
def get_users_list_by_groupid(groupid):
	try:
		#in first step get 1000 users id and count of group (border)
		open(DIR + groupid + '_usersdata.txt', 'w')
		border = groups_getMembers(groupid)
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
		
#get groups list by substrings and parameters
def get_groups_list_by_substrings(q, access_token, filename='', type_='', country_id='', city_id='', future='', market='', offset=0, sort=0, count=''):
	try:
		fname = q[:50]
		open(DIR + fname + '.txt', 'w')
		substrings_list = q.split(',')
		for string in substrings_list:
			print(string)
			groups_search(string, access_token, fname, type_, country_id, city_id, future, market, offset, sort, count)
		return 'susccess'
	except:
		print('get_groups_list error')
		return None

#get posts list by group and parameters
def get_page_posts(access_token='', owner_id='', domain='', count='', extended='', fields='', offset=0, filter_='owner', likes=None, reposts=None, comments=None):
	try:
		filename = max(owner_id, domain)
		open(DIR + filename + '_posts.txt', 'w')
		border = wall_get(access_token, owner_id, domain, count, extended, fields, offset, filter_, likes, reposts, comments)
		print(border)
		#ThreadPool model
		offsets = [(access_token, owner_id, domain, count, extended, fields, offset, filter_, likes, reposts, comments) for offset in range(100, border+1, 100)]
		def wall_get_local(parameters):
				return wall_get(*parameters)
		pool = ThreadPool(pool_number)
		pool.map(wall_get_local, offsets)
		return 'susccess', border
	except:
		print('get_page_posts error')
		return None




		








