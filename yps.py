#!/usr/bin/env python3

import argparse
import fnmatch
import os
import json
import subprocess


YOUTUBE_DL_PATH = 'youtube-dl'
CONFIG_FILENAME = 'yps.json'


def print_info(info):
    print('YPS: ' + info)

def run_in_subprocess(args):
    print_info(' '.join(args))
    subprocess.call(args)

def save_config(directory, playlist_url):
    config_loc = os.path.expanduser(os.path.join(directory, CONFIG_FILENAME))
    if os.path.exists(config_loc):
        exit('Configuration at ' + config_loc + ' already exists. Not saving new config.')

    config_data = {'youtube_playlist': playlist_url}

    save_config_data(config_loc, config_data)
    print_info('Saved config to ' + config_loc)

def save_config_data(config_loc, data):
    with open(config_loc, 'w') as config_outfile:
        json.dump(data, config_outfile, sort_keys=True, indent=4, separators=(',', ': '))

def get_config(directory):
    with open(directory, 'r') as config_handler:
        return json.load(config_handler)


def sync_playlist(config_path):
    print_info('Starting to process config file: ' + config_path)
    if not os.path.exists(config_path):
        print_info('Config path does not exist')
        return False

    config_data =get_config(config_path)

    current_dir = os.getcwd()  # save dir to change back to it later
    os.chdir(os.path.dirname(config_path))  # change dir to the one you want to save the videos to

    if 'format' in config_data:
        run_in_subprocess([YOUTUBE_DL_PATH, '-f', config_data['format'], config_data['youtube_playlist']])
    else:
        run_in_subprocess([YOUTUBE_DL_PATH, config_data['youtube_playlist']])

    os.chdir(current_dir)  # change back to original dir

    return True

parser = argparse.ArgumentParser(description='Download and synchronise a directory with a youtube playlist')
parser.add_argument('--sync', required=False, nargs='?', const='.')
parser.add_argument('--init', metavar='playlist_url', help='words', required=False)
parser.add_argument('--dir', metavar='directory', required=False, default='.', help='The directory to act on')
parser.add_argument('--format', required=False)
args = parser.parse_args()

if args.sync:
    dir_to_process = args.sync

    all_found_configs = []
    for root, dirnames, filenames in os.walk(os.path.expanduser(dir_to_process)):
        for filename in fnmatch.filter(filenames, CONFIG_FILENAME):
            all_found_configs.append(os.path.join(root, filename))

    print_info('Found ' + str(len(all_found_configs)) + ' config files, proceeding to sync')

    for config_file in all_found_configs:
        success = sync_playlist(os.path.abspath(config_file))
        if not success:
            print_info('Failed to sync config ' + config_file)
        else:
            print_info('Synced config ' + config_file)

elif args.init:
    new_youtube_playlist = args.init
    save_dir = args.dir

    save_config(save_dir, new_youtube_playlist)

elif args.format:
    yps_config_loc = os.path.join(args.dir, CONFIG_FILENAME)

    config = get_config(yps_config_loc)
    config['format'] = args.format
    save_config_data(yps_config_loc, config)
    print_info('Added format ' + args.format)


else:
    parser.print_help()