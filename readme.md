# Setlist Generator
![Screenshot](scr.png)
This project is targeted at musicians, who want to generate the best setlist possible.

Basically; you provide your song pool and set flow in JSON format, and the program automatically generates the best 
sequence of songs. 

## How To Use

- Edit config/constants.py and put your own values here
- Create and put your JSON files into the /data folder. The file should look like the samples provided in /data. The format is very intuitive.
- Run main.py

### Non-Intuitive JSON Tags

reservation: Determines if the song should be placed to an ad-hoc location within the generated setlist. Accepted values: 
- "gig_opener": Songs that should be at the beginning of the gig
- "gig_closer": Songs that should be at the end of the gig
- "gig_closer-1": Song that should be placed before the last song of the gig. You can set values like -2 -3 -4 etc...
- "set_opener": Songs that should be at the beginning of a set
- "set_closer": Songs that should be at the end of a set

## How To Extend

If you want to add new song properties;
- Extend your JSON file(s) with new properties
- Edit gig/song.py to support the new properties
- Edit generator/primal_song_picker.py (or your own generators) to consider the new properties

If you want to modify the default generator, you can edit /generator/primal_song_picker.py with your own logic

If you want to develop a new generator;
- Create a new file + class under /generator, which extends /generator/abstract_generator
- Ensure that /gui/prime.py uses your new generator instead of the default one

If you need a new writer (like a new file format output);
- Create a new file + class under /writer, which extends /writer/abstract_writer
