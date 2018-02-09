# galleryRate
An app for collecting gallery rating data

Modify app behavior with config.conf. One command per line, with the format <parameter>: <value>
  Example:
  title: This is my title
  
You can use # to comment out a line. Parameters specified with no value will default to an empty string. Parameters omitted will use reasonable values.

Available parameters:

path: set the name and path of the csv file to record the rating data
title: The large header at the top of the screen
label_[1/2/3/4/5]: The label underneath button
subtitle: The large footer below the labels
date_string: If False, returns the time in seconds from the UNIX epoch. Defautls True, which gives an ISO string
font_[title/subtitle/label/button]: specifies a font to be used, either from the local directory or the system catalog. Defaults to Roboto.
