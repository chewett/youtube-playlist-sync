#!/usr/bin/env python

import argparse
import fnmatch
import os
import json
import subprocess


YOUTUBE_DL_PATH = 'youtube-dl'
CONFIG_FILENAME = 'yps.json'


def print_info(info):
    print 'YPS: ' + info


def save_config(directory, playlist_url):
    config_loc = os.path.expanduser(os.path.join(directory, CONFIG_FILENAME))
    if os.path.exists(config_loc):
        exit('Configuration at ' + config_loc + ' already exists. Not saving new config.')

    config_data = {'youtube_playlist': playlist_url}

    with open(config_loc, 'w') as config_outfile:
        json.dump(config_data, config_outfile, sort_keys=True, indent=4, separators=(',', ': '))

    print "Saved config to " + config_loc


def sync_playlist(config_path):
    if not os.path.exists(config_path):
        return False

    with open(config_path, 'r') as config_handler:
        config_data = json.load(config_handler)

    current_dir = os.curdir  # save dir to change back to it later
    os.chdir(os.path.dirname(config_path))  # change dir to the one you want to save the videos to
    subprocess.call([YOUTUBE_DL_PATH, config_data['youtube_playlist']])

    os.chdir(current_dir)  # change back to original dir

    return True

parser = argparse.ArgumentParser(description='Download and synchronise a directory with a youtube playlist')
parser.add_argument('--sync', required=False)
parser.add_argument('--init', required=False)
parser.add_argument('--dir', required=False)
args = parser.parse_args()

if args.sync:
    dir_to_process = args.sync

    all_found_configs = []
    for root, dirnames, filenames in os.walk(os.path.expanduser(dir_to_process)):
        for filename in fnmatch.filter(filenames, CONFIG_FILENAME):
            all_found_configs.append(os.path.join(root, filename))

    print_info('Found ' + str(len(all_found_configs)) + ' config files, proceeding to sync')

    for config_file in all_found_configs:
        success = sync_playlist(config_file)
        if not success:
            print_info('Failed to sync config ' + config_file)
        else:
            print_info('Synced config ' + config_file)

elif args.init:
    new_youtube_playlist = args.init
    save_dir = args.dir

    save_config(save_dir, new_youtube_playlist)

else:
    parser.print_help()