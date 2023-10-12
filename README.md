# Install #
Install normally through git. Add the required packages in the requirements.txt via `pip install -r requirements.txt`

Windows users need to install poppler (https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows)

# First Run #
Execute `main_gui.py` from terminal, i.e. `python main_gui.py`
On first run, the script will create the necessary target folder, `Sheet_music` in the home directory.
Within this, there will be a `pdf` folder which must be populated with sheet music.

The required naming schema for these pdfs is score__composer. 
e.g. Moonlight Sonata by Beethoven would become `Moonlight_Sonata__Beethoven`

# Usage #
If new pdfs are detected, a popup will appear to convert them to the supported format. 
Conversion can be slow, especially if there are many new files. There is the option to convert to a sepia tinted tone to be easy on the eyes.

After conversion, or if conversion is skipped, pieces can be searched for and viewed.
To view a full piece, double click it. Navigate forward by right clicking on either displayed page, backward by left clicking.
Exit the "playing" view by hitting the Escape key.
