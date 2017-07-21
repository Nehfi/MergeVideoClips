#!/usr/bin/env python

import subprocess
import urllib.request
import os
import sys
import tempfile

FFMPEG = "/usr/bin/ffmpeg"
OUTPUT = "out.mp4"

os.makedirs("tmpdir")

#URLs for the files in question. Probably change to read in an array from file
URLrender1 = 'http://recoordio-zoo.s3-eu-west-1.amazonaws.com/KimsChallenge/0c2bad4c9873680a784c29ca3aa7f4b7-9000-render.mp4'
URLraw1 = 'http://recoordio-zoo.s3-eu-west-1.amazonaws.com/KimsChallenge/0c2bad4c9873680a784c29ca3aa7f4b7-9000.mp4'
URLrender2 = 'http://recoordio-zoo.s3-eu-west-1.amazonaws.com/KimsChallenge/1248fd1e3b056eda99c1723e11f3f838-118000-render.mp4'
URLraw2 = 'http://recoordio-zoo.s3-eu-west-1.amazonaws.com/KimsChallenge/1248fd1e3b056eda99c1723e11f3f838-118000.mp4'
URLrender3 = 'http://recoordio-zoo.s3-eu-west-1.amazonaws.com/KimsChallenge/69dbf8532876199b29e372f2d296db89-68000-render.mp4'
URLraw3 = 'http://recoordio-zoo.s3-eu-west-1.amazonaws.com/KimsChallenge/69dbf8532876199b29e372f2d296db89-68000.mp4'

#Download specified files
urllib.request.urlretrieve(URLrender1, "tmpdir/render1.mp4")
urllib.request.urlretrieve(URLraw1, "tmpdir/raw1.mp4")
urllib.request.urlretrieve(URLrender2, "tmpdir/render2.mp4")
urllib.request.urlretrieve(URLraw2, "tmpdir/raw2.mp4")
urllib.request.urlretrieve(URLrender3, "tmpdir/render3.mp4")
urllib.request.urlretrieve(URLraw3, "tmpdir/raw3.mp4")

print("Downloading the specified files...")

#Make files containing filenames to be concatenated
fileRender = open('tmpdir/render','w')
fileRender.write("file 'render1.mp4'" '\n')
fileRender.write("file 'render2.mp4'" '\n')
fileRender.write("file 'render3.mp4'")
fileRender.close()
fileRaw = open('tmpdir/raw','w')
fileRaw.write("file 'raw1.mp4'" '\n')
fileRaw.write("file 'raw2.mp4'" '\n')
fileRaw.write("file 'raw3.mp4'")
fileRaw.close()

print("Concatenating clips...")

#Concatenate the rendered clips and the raw raw into two distinct clips
cmd = ['ffmpeg', '-y', '-f', 'concat', '-i', 'tmpdir/render', '-c', 'copy', 'tmpdir/outRender.mp4']
subprocess.call(cmd)
cmd = ['ffmpeg', '-y', '-f', 'concat', '-i', 'tmpdir/raw', '-c', 'copy', 'tmpdir/outputRaw.mp4']
subprocess.call(cmd)

print("Mergin clips...")

#Stack clips vertically, by way of reasizing the smaller clip, then stacking them.
#Writes to the final output file
cmd = ['ffmpeg', '-i', 'tmpdir/outRender.mp4', '-i', 'tmpdir/outputRaw.mp4', '-y',
    '-filter_complex', '[1][0]scale2ref[2nd][ref];[ref][2nd]vstack',
    '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast',
    'out.mp4']

subprocess.call(cmd)

#Delete any intermediary files?

print("Job done. Will now exit.")










#
