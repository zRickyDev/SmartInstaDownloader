#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os.path
import urllib, json
import time, sys
from pprint import pprint

log_file = "log.txt"
last_media_ids = []
download_counter = 0

base_url = "https://www.instagram.com/"
json_url_enabler = "/?__a=1"
profile_username = raw_input("Please enter Instagram username: ")
full_url = base_url + profile_username + json_url_enabler

while True:
	try:
		# Get json data
		response = urllib.urlopen(full_url)
		data = json.loads(response.read())
		print ("Downloading user data...")

		# Check if file exists
		if not os.path.exists(log_file):
			open(log_file, 'a').close()
		
		# Get media nodes from json data
		image_nodes = data["user"]["media"]["nodes"]
		
		# Download new images and save on storage
		for node in image_nodes:
			display_src = node["display_src"]
			id = node["id"]
			with open(log_file) as myfile:
				if not id in myfile.read():
					urllib.urlretrieve(display_src, id + ".jpg")
					last_media_ids.append(id)
					download_counter += 1
					print("Downloaded image: " + id + ".jpg")
		print("Download has been finished for now...")		

		# Writing new media id on file...
		out_file = open("log.txt", "a")
		for id in last_media_ids:
			out_file.write(id)
		out_file.close()
		last_media_ids = []

		# Wait 600s before doing another parse
		print("Now waiting 10 minutes before check if other pictures has been uploaded!")
		time.sleep(600)
		
	except KeyboardInterrupt:
		print("Downloads in this session: " + str(download_counter))
		sys.exit()
