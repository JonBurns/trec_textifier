#!/usr/bin/env python

import subprocess
import os
import sys

def decrypt_decompress(fname, old_folder_path, new_folder_path):

    # this will contain the type of file (classified/linking/etc) plus a ton of numbers
    pure_fname = fname.split('.')[0]

    full_fname = old_folder_path + fname

    # Decryption
    # IMPORTANT: Keys must have been imported for this to work: See http://www.debuntu.org/how-to-importexport-gpg-key-pair/
    # print 'gpg --output ' + old_folder_path + pure_fname + '.sc.xz' + ' --decrypt ' + full_fname + '\n'
    subprocess.call('gpg --output ' + old_folder_path + pure_fname + '.sc.xz' + ' --decrypt ' + full_fname, shell = True)

    # Decompression 
    # print 'xz --decompress ' + old_folder_path + pure_fname + '.sc.xz' + '\n'
    subprocess.call('xz --decompress ' + old_folder_path + pure_fname + '.sc.xz', shell = True)

    # Change to a textfile 
    # print 'mv ' + old_folder_path + pure_fname + '.sc ' + new_folder_path + pure_fname + '.txt' + '\n'
    subprocess.call('mv ' + old_folder_path + pure_fname + '.sc ' + old_folder_path + pure_fname + '.txt' , shell = True)

    # Call the correct parse script on the file
    # parse_me(old_folder_path + pure_fname, new_folder_path)

def parse_me(filename, new_file_location):

    if 'meme' in filename:
        print 'MEME call on: ' + filename
        subprocess.call('python file_splitter_MEME.py ' + filename + '.txt ' + new_file_location, shell = True)

    elif 'social' in filename:
        print 'SOCIAL call on: ' + filename
        subprocess.call('python file_splitter_SOCIAL.py ' + filename + '.txt ' + new_file_location, shell = True)

    else:
        print 'HTML call on: ' + filename
        subprocess.call('python file_splitter_HTML.py ' + filename + '.txt ' + new_file_location, shell = True)
    


# file_containing_filepaths = 'streamcorpus-2014-v0_3_0-ts-filtered.s3-paths.txt'

#subprocess.call("wget http://s3.amazonaws.com/aws-publicdatasets/trec/ts/streamcorpus-2014-v0_3_0-ts-filtered.s3-paths.txt.xz;", shell = True)

#subprocess.call("xz --decompress streamcorpus-2014-v0_3_0-ts-filtered.s3-paths.txt.xz;", shell = True)

# # subprocess.call("xz --decompress test.txt.xz;", shell = True)

#subprocess.call("cat streamcorpus-2014-v0_3_0-ts-filtered.s3-paths.txt | cut -d ':' -f3 | sed 's/\/\//:\/\/s3.amazonaws.com\//g' | parallel -j 10 'wget --recursive --continue --no-host-directories --no-parent --reject \"index.html*\" http{}';", shell = True)

subprocess.call("cat test.txt | cut -d ':' -f3 | sed 's/\/\//:\/\/s3.amazonaws.com\//g' | parallel -j 10 'wget --recursive --continue --no-host-directories --no-parent --reject \"index.html*\" http{}';", shell = True)

# The above calls download the Trec data to the follow file tree:
# Working Directory
# -> aws-publicdatasets
#    -> trec
#        -> ts
#            -> streamcorpus-2014-v0_3_0-ts-filtered
#                -> first date
#                ...
#                -> last date

# Directory that will contain all the different date folders
path = 'aws-publicdatasets/trec/ts/streamcorpus-2014-v0_3_0-ts-filtered/'

# This will give us all the folders (Which will be times)
folders = os.listdir(path)

## Stuff if running on Mac (get rid of .ds_store)
#folders = folders[1:]    
    
##

# We want to deal with each folder individually 
for folder in folders:
    path_to_folder = path + folder
    new_folder = 'new_stuff/' + folder + '/'

    subprocess.call('mkdir ' + new_folder, shell = True)

    # We need to get a list of the files
    files = os.listdir(path_to_folder)

    ## .ds_store again
    #files = files[1:]

    # For each file we need to decrypt it, decompress it and then move it to a new folder
    # As each parser will cause each file to result in 1 to n different we have to move the entire folder after instead of each
    # file (As we don't know how many there will be)
    for f in files:
        decrypt_decompress(f, path_to_folder + '/', new_folder)

    # # We should now be able to remove the old files
    subprocess.call('rm -rf ' + path_to_folder, shell = True)

    # # Now we want to upload the finished files into S3
    subprocess.call('aws s3 cp --recursive ' + new_folder + ' s3://trec2014test/' + folder + ' &', shell = True)


