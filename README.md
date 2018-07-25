# galleryRate
An app for collecting audience feedback

This app requires a Python 3 installation.

At launch, the app will create one button for every file `xxx.conf` in the buttons directory, in alphabetical order by filename from left to right. The following parameters can placed in each conf file:
* `text`: A text string to appear in the button
* `label`: A text string to appear below the button
* `[text/label]_font_size`: The font size for that piece of text. Eg., `text_font_size`
* `[text/label]_font_name`: specifies a font to be used, either from the local directory or the system catalog. Defaults to Roboto. Eg., `label_font`
* `background_normal`: An image file corresponding to what the button (without text) looks like in an unpressed state. This is required and each button should have a border to distinguish it from the others.
* `background_pressed`: An image file corresponding to what the button (without text) looks like in a pressed state. This is required and each button should have a border to distinguish it from the others.

Modify app behavior with config.conf. One command per line, with the format `<parameter>: <value>`
  Example:
  `title: This is my title`
  
You can use `#` to comment out a line. Parameters specified with no value will default to an empty string. Parameters omitted will use reasonable values.

Available parameters:
* `path`: set the name and path of the csv file to record the rating data
* `title`: The large header at the top of the screen
* `subtitle`: The large footer below the labels
* `font_[title/subtitle]`: specifies a font to be used, either from the local directory or the system catalog. Defaults to Roboto. Eg., `font_title`

Text markup:
All text fields can be transformed using the BBCode markup. For information on supported tags, see: https://kivy.org/docs/api-kivy.uix.label.html
