# Youtube Playlist Sync

A small script used to download videos from a number of playlists using youtube-dl

## Usage

Clone the repository

Set up a folder to store your playlist details with

    yps.py --init <playlist url> --dir <folder>

Then sync it and download all the videos with

    yps.py --sync <folder>
    
youtube-dl handles if you need to download a video or not and supports download resuming.

## License

MIT all the way!