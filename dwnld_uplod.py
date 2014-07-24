#!/usr/bin/env python

import subprocess
import os
import sys

files = "streamcorpus-2014-v0_3_0-ts-filtered.s3-paths.txt"

#subprocess.call("wget http://s3.amazonaws.com/aws-publicdatasets/trec/ts/streamcorpus-2014-v0_3_0-ts-filtered.s3-paths.txt.xz;", shell = True)

#subprocess.call("xz --decompress streamcorpus-2014-v0_3_0-ts-filtered.s3-paths.txt.xz;", shell = True)

subprocess.call("xz --decompress test.txt.xz;", shell = True)

#subprocess.call("cat streamcorpus-2014-v0_3_0-ts-filtered.s3-paths.txt | cut -d ':' -f3 | sed 's/\/\//:\/\/s3.amazonaws.com\//g' | parallel -j 10 'wget --recursive --continue --no-host-directories --no-parent --reject \"index.html*\" http{}';", shell = True)

subprocess.call("cat test.txt | cut -d ':' -f3 | sed 's/\/\//:\/\/s3.amazonaws.com\//g' | parallel -j 10 'wget --recursive --continue --no-host-directories --no-parent --reject \"index.html*\" http{}';", shell = True)
