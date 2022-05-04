# Setlist Generator
![Screenshot](scr2.png)
This project is targeted at musicians, who want to generate the best setlist possible.

Basically; you provide your song pool and set flow in JSON format, and the program automatically generates the best 
sequence of songs. 

You can watch a live demo [on YouTube](https://youtu.be/SyNAFOwRFCQ) .

## How To Use

- Edit config.json and put your own values here
- Create and put your JSON files into the /data folder. The file should look like the samples provided in /data. The format is very intuitive.
- Run main.py

## Igigi integration

Igigi is a mobile gig helper app, available at https://github.com/keremkoseoglu/igigi . 

When you generate an HTML output, it will also generate an output for Igigi which can later be downloaded to Igigi (iPad) over Dropbox.

## FlukeBox integration

FlukeBox is a cross-streaming-service audio player, available at https://github.com/keremkoseoglu/flukebox .

When you generate an HTML output, it will also trigger FlukeBox to generate an output for rehearsal / studying.

To enable that functionality;

- Install FlukeBox
- Edit config.json so that **FLUKEBOX_DIR** points to your FlukeBox installation directory

To disable that functionality; simply edit config.json and leave **FLUKEBOX_DIR** empty.

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
