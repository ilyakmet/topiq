# -*- coding: utf-8 -*-
import vkapi, os

DIR = os.path.abspath(os.curdir) + '/'

#generate your own access_token: https://habrahabr.ru/post/213163/
token = '0b857507f6fe8a67c01ef4f51c9b4085077eb225e4bb6cda064705ecfa1d97a7d6d38c347222e1887d6d3'#token here

if __name__ == "__main__":

	#call help(function_name) for more information

	#change groupid
	vkapi.get_users_list_by_groupid('piter')

	#add your key words and parameters like this: https://vk.com/dev/groups.search
	#vkapi.get_groups_list_by_substrings('Stepic, Python, HSE, Privet', access_token=token, count=1000)

	#change group and parameters
	#vkapi.get_page_posts(domain='team', filter_='owner')

	#vkapi.groups_getMembers(groupid='typical_krd', count=1000)
	

	