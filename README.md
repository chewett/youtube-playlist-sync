# Youtube Playlist Sync

A small script used to download videos from a number of playlists using youtube-dl.

You initialise a folder to hold a specific playlist, which then stores a config file in that directory that holds the
 playlist details.

Once this has been done, sync can be run on a directory, and all directories under that holding a config file will
 have their videos downloaded and updated.
 
This allows to keep an updated local copy of a large number of playlists easily.

## Usage

Clone the repository

Set up a folder to store your playlist details with

    yps.py --init <playlist url> --dir <folder>

Then sync it and download all the videos with

    yps.py --sync <folder>
    
youtube-dl handles if you need to download a video or not and supports download resuming.

## License

MIT all the way!