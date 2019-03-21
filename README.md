# rfu
Radarr Import Assistant

Import a library with IMDB IDs in the filenames.

`python rfu.py -d <root folder path>`

### Setting up rfu.conf

- **server** [str] - Please use the same address as you use for accessing the web interface in your browser. Default for running on the same machine is `localhost:7878`.
- **api_key** [str] - Can be found under Settings > General.
- **ssl** [`True`|`False`] - Changes to `https://` in Radarr URL instead of `http://`.
- **quality** [int] - ID number assigned to the Radarr profile you want to use.

`http://localhost:7878/api/movie?apikey=XXX` and search for "qualityProfileId", if you use more than one profile you will need to find a movie you know and match Profile name to ID number.

### Installation and Running

- Download and extract the zip or clone with git to a location of your choice.
- Make a copy of `rfu.default.conf` and rename it `rfu.conf` and edit it for your values.
- In Command Prompt or Terminal, navigate into the downloaded folder and run `python rfu.py -d <root folder path>` to begin importing.
