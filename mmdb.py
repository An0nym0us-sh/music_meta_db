#!/usr/bin/env python3

from sys import argv
from tinytag import TinyTag
import os

from rich.console import Console
from rich.table import Table
from rich import box

root_dir = os.environ["HOMEPATH"] + "\\Music"

padding = 3
SUPPORTED_FILETYPES = [
        ".mp4",
        ".m4a",
        ".mp3"
        ]


class Track():
    def __init__(self, artist , album , title , duration):
        self.artist = artist
        self.album = album
        self.title = title
        self.duration = duration

    def get_values(self):
        return [self.artist , self.album , self.title, self.duration]


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    if hour == 0:
        return "%dm %ds" % (minutes, seconds)

    else:
        return "%d:%02d:%02d" % (hour, minutes, seconds)


def main(args):
    artist_db = {} # List of Tracks for each artist

    track_counter = 0

    console = Console()

    file_list = []

    for root , dirs , files in os.walk(root_dir):
        for i in files:
            for filetype in SUPPORTED_FILETYPES:
                if i.endswith(filetype):
                    file_list.append(os.path.join(root,i))

    for track in file_list:
        data = TinyTag.get(track)
        if data.artist not in artist_db.keys():
            artist_db.update({data.artist : []})
            artist_db[data.artist].append(Track(data.artist , data.album , data.title , round(data.duration)))
        else:
            artist_db[data.artist].append(Track(data.artist , data.album , data.title , round(data.duration)))

    for artist in artist_db.keys():
        table = Table(title=artist , expand=True , box=box.SIMPLE , style="yellow" , title_style="color(14)")

        table.add_column("Album" , width=10 , style="magenta" , justify="right")
        table.add_column("Title", width=30 , style="magenta" , justify="left")
        table.add_column("Duration" , width=10 , style="magenta" ,justify="center")

        for value in artist_db[artist]:
            info = value.get_values()
            table.add_row(info[1] , info[2] , convert(info[3]))
            track_counter += 1
        
        console.print(table)
        print("\n" * padding)
   
    console.print(f"{track_counter} Songs across {len(artist_db.keys())} artists")
    print("\n")
    artist_table = Table(title="Artist Summary" , style="blue")
    artist_table.add_column("Artist")
    artist_table.add_column("Songs")

    for artist in artist_db.keys():
       artist_table.add_row(artist , str(len(artist_db[artist])))

    console.print(artist_table)



main(argv)
