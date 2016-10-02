# -*- coding: utf-8 -*-
import vkapi, os

DIR = os.path.abspath(os.curdir) + '/'

#generate your own access_token: https://habrahabr.ru/post/213163/
token = ''#token here

if __name__ == "__main__":

	#change groupid
	#vkapi.get_users_list_by_groupid('piter')

	#add your key words and parameters like this: https://vk.com/dev/groups.search
	#standard parameters: substrings, access_token, filename='', grouptype='', countryid='', cityid='', future='', market='', sort=0, count=10
	vkapi.get_groups_list('Moscow, Krasnodar, Piter', access_token=token, count=1000)

	