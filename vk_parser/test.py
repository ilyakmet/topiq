# -*- coding: utf-8 -*-
import vkapi, os

DIR = os.path.abspath(os.curdir) + '/'

#generate your own access_token: https://habrahabr.ru/post/213163/
token = ''#token here

if __name__ == "__main__":

	#call help(function) for more information

	#change groupid
	#vkapi.get_users_list_by_groupid('piter')

	#add your key words and parameters like this: https://vk.com/dev/groups.search
	#vkapi.get_groups_list_by_substrings('Stepic, Python, HSE, Privet', access_token=token, count=1000)

	#change group and parameters
	#vkapi.get_page_posts(domain='typical_krd', filter_='owner')
	

	