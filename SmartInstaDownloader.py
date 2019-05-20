#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import requests
import time
import csv

download_path = "./InstagramPhotos"

last_media_ids = []
download_counter = 0

base_url = "https://www.instagram.com/"
json_url_enabler = "/?__a=1"
profile_username = raw_input("Please enter Instagram username: ")
full_url = base_url + profile_username + json_url_enabler

while True:
	try:
		# Get json data
		r = requests.get(full_url)
		if r.status_code != 200:
			print 'Something went wrong :('
			exit()

		# Check if log file & download path exists
		if not os.path.exists('log.csv'):
			os.system('touch log.csv')
		if not os.path.exists(download_path):
			os.makedirs(download_path)
		
		# Get media nodes from json data
		edges_nodes = r.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
		
		# Download new images and save on storage
		for edge in edges_nodes:
			image_url = edge["node"]["display_url"]
			id = edge["node"]["id"]
			with open('log.csv') as ids_file:
				reader = csv.reader(ids_file, delimiter=',')
				if not id in reader:
					full_path = os.path.join(download_path, id + ".jpg")
					r = requests.get(image_url, stream=True)
					if r.status_code == 200:
						with open(full_path, 'wb') as f:
							for chunk in r:
								f.write(chunk)
					last_media_ids.append(id)
					download_counter += 1
					print("Downloaded image: " + id + ".jpg")
		print("Download has been finished for now...")		

		# Writing new media id on file...
		with open("log.csv", "a") as out_file:
			writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for id in last_media_ids:
				writer.writerow([id])
			last_media_ids = []

		# Wait 600s before doing another parse
		print("Now waiting 10 minutes before check if other pictures has been uploaded!")
		time.sleep(600)
		
	except KeyboardInterrupt:
		print("Downloads in this session: " + str(download_counter))
		exit()
