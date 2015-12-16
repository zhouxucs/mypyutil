#!/usr/bin/python

import os
import sys

def convert_dvd_to_mp4(dvd_path, save_to):


	dvd_video_path = os.path.join(dvd_path, "VIDEO_TS")
	print dvd_video_path

	vedio_list = ""
	for root, dirs, files in os.walk(dvd_video_path):
		for f in files:
			if f.endswith(".VOB"):
				file_path = os.path.join(dvd_video_path, f)
				if len(vedio_list) == 0:
					vedio_list += file_path
				else:
					vedio_list += ("|" + file_path)


	vedio_list = "\"" + vedio_list + "\""

	if len(vedio_list) == 0:
		return

	#cmdline = "ffmpeg -i concat:%s -acodec libfaac -aq 100 -ac 2 -vcodec libx264 -vpre slow -crf 24 -threads 0 %s" % (vedio_list, save_to)
	cmdline = "ffmpeg -i concat:%s -acodec libfaac -vcodec mpeg4 -mbd 2 -flags +mv4+aic -trellis 2 -cmp 2 -subcmp 2 -metadata title=my_dvd %s" % (vedio_list, save_to)

	os.system(cmdline)

if __name__ == "__main__":
	dvd_path = sys.argv[1]
	save_to = sys.argv[2]
	convert_dvd_to_mp4(dvd_path, save_to)
