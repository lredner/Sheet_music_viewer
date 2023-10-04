import PySimpleGUI as sg
from screeninfo import get_monitors
from pdf_conversion_gui import are_new_pdfs_available, PdfWindowGui
import os
import PIL.Image
import io

def convToBytes(image, resize=None):
   img = image.copy()	
   cur_width, cur_height = img.size
   if resize:
      new_width, new_height = resize
      scale = min(new_height/cur_height, new_width/cur_width)
      img = img.resize((int(cur_width*scale), int(cur_height*scale)))	
   ImgBytes = io.BytesIO()
   img.save(ImgBytes, format="PNG")
   del img
   return ImgBytes.getvalue()

def search(sheet_music_list, input_text):
   return sorted([entry for entry in sheet_music_list if input_text in entry.lower()])


def main():
   sg.theme('BlueMono')

   # convert pixels to characters
   PIXELS_PER_CHARACTER_WIDTH = 8
   PIXELS_PER_CHARACTER_HEIGHT = 8

   # get size of screen in pixels and characters
   screen_height_pixels = get_monitors()[0].height
   screen_width_pixels = get_monitors()[0].width
   screen_height_char = int(screen_height_pixels/PIXELS_PER_CHARACTER_HEIGHT)
   screen_width_char = int(screen_width_pixels/PIXELS_PER_CHARACTER_WIDTH)

   # convert new pdfs to images
   target_path = os.path.join(os.path.expanduser('~'), 'Sheet_music')
   source_pdf_path = os.path.join(target_path, 'pdf')
   new_pdfs = []
   if are_new_pdfs_available(source_pdf_path, target_path, new_pdfs):
      PdfWindowGui(source_pdf_path, target_path, new_pdfs, (int(0.4*screen_width_pixels), int(0.3*screen_height_pixels)))

   # get the list of sheet music
   sheet_music_list = [piece for piece in os.listdir(target_path) if len(os.listdir(os.path.join(target_path, piece)))>0 and piece != 'pdf']

   # format it e.g. Moonlight_Sonata__Beethoven -> Moonlight Sonata Beethoven
   sheet_music_list = sorted([name.replace('__', ' - ').replace('_', ' ') for name in sheet_music_list])
   longest_entry = len(max(sheet_music_list, key=len))

   listbox_size = (min(int(0.3*screen_width_char), longest_entry), screen_height_char)
   final_font = ('Arial Bold', 15)

   file_list_column = [
      [
         sg.Input('', size=(listbox_size[0], 1), key='-SEARCH-', font = final_font, enable_events = True)
      ],
      [
         sg.Listbox(values=sheet_music_list, enable_events=True, size=(listbox_size[0], listbox_size[1]-1), 
                     key="-MUSIC_LIST-", font=final_font, select_mode = "LISTBOX_SELECT_MODE_SINGLE")
      ]
   ]

   sheet_music_viewer_column = [
      [
         sg.Image(key="-SHEET_MUSIC-")
      ]
   ]

   browse_layout = [
      [
         sg.Column(file_list_column),
         sg.VSeperator(),
         sg.Column(sheet_music_viewer_column)
      ]
   ]

   fullscreen_layout = [
       [
           sg.Image(key="-FULLSCREEN1-"),
           sg.Image(key='-FULLSCREEN2-')
       ]
   ]

   layout = [[sg.Column(browse_layout, key = '-BROWSE-'), sg.Column(fullscreen_layout, key = '-FULLSCREEN-', visible = False)]]

   window = sg.Window("Sheet Music Viewer", layout, resizable=True, size = (screen_width_pixels, screen_height_pixels), finalize = True)

   window['-MUSIC_LIST-'].bind('<Double-Button-1>' , "+-double click-")
   window.bind("<Escape>", "-ESCAPE-")
   window['-FULLSCREEN-'].bind('<Button-1>', "-LEFT_CLICK-")
   window['-FULLSCREEN-'].bind('<Button-3>', "-RIGHT_CLICK-")
   window['-FULLSCREEN1-'].bind('<Button-1>', "-LEFT_CLICK-")
   window['-FULLSCREEN1-'].bind('<Button-3>', "-RIGHT_CLICK-")
   window['-FULLSCREEN2-'].bind('<Button-1>', "-LEFT_CLICK-")
   window['-FULLSCREEN2-'].bind('<Button-3>', "-RIGHT_CLICK-")

   search_content = ""

   # indices for which file to display in fullscreen mode
   lower_page_index = 0
   upper_page_index = 1

   # toggle for which panel to update. Left then right goes to new music
   update_panel = 1

   # Run the Event Loop
   while True:
      event, values = window.read()
      
      if event == "Exit" or event == sg.WIN_CLOSED:
         break
      
      if event == "-MUSIC_LIST-":
         # format back into the image format
         image = values['-MUSIC_LIST-'][0].replace(' ', '_').replace('-','')
         image_path = os.path.join(os.path.expanduser('~'), 'Sheet_music', image)

         # retrieve and resize the image
         filename = os.path.join(image_path, sorted(os.listdir(image_path))[0])
         image_size = list(window['-MUSIC_LIST-'].get_size())
         image_size[0] = screen_width_pixels - image_size[0]
         window["-SHEET_MUSIC-"].update(data = convToBytes(PIL.Image.open(filename), image_size))

      if event == "-MUSIC_LIST-+-double click-":
         window['-BROWSE-'].update(visible=False)
         window['-FULLSCREEN-'].update(visible=True)

         files = sorted(os.listdir(image_path))
         image_size[0] = int(screen_width_pixels/2)
         lower_page_index = 0
         upper_page_index = 1
         if len(files) > 1:
            window['-FULLSCREEN2-'].update(data = convToBytes(PIL.Image.open(os.path.join(image_path,files[upper_page_index])), image_size))
         window['-FULLSCREEN1-'].update(data = convToBytes(PIL.Image.open(os.path.join(image_path,files[lower_page_index])), image_size))
         
      if search_content != values['-SEARCH-']:
         window['-MUSIC_LIST-'].update(values = search(sheet_music_list, values['-SEARCH-']))

      if len(values['-SEARCH-']) == 0:
         window['-MUSIC_LIST-'].update(values = sheet_music_list)

      if window['-FULLSCREEN-'].visible:
         if event == "-ESCAPE-":
            window['-BROWSE-'].update(visible=True)
            window['-FULLSCREEN-'].update(visible=False)
         if event == "-FULLSCREEN1--LEFT_CLICK-" or event == "-FULLSCREEN2--LEFT_CLICK-" or event == "-FULLSCREEN--LEFT_CLICK-":
            if lower_page_index >0:
               upper_page_index -= 1
               lower_page_index -= 1
               window[f'-FULLSCREEN1-'].update(data = convToBytes(PIL.Image.open(os.path.join(image_path,files[lower_page_index])), image_size))
               window[f'-FULLSCREEN2-'].update(data = convToBytes(PIL.Image.open(os.path.join(image_path,files[upper_page_index])), image_size))
               window.refresh()
         if event == "-FULLSCREEN1--RIGHT_CLICK-" or event == "-FULLSCREEN2--RIGHT_CLICK-" or event == "-FULLSCREEN--RIGHT_CLICK-":
            if upper_page_index < len(files)-1:   
               upper_page_index += 1
               lower_page_index += 1
               window[f'-FULLSCREEN{update_panel}-'].update(data = convToBytes(PIL.Image.open(os.path.join(image_path,files[upper_page_index])), image_size))
               # switch update panel. If was 1, become 2. Otherwise, 2 becomes 1
               update_panel = update_panel%2 + 1
               window.refresh()

      
      search_content = values['-SEARCH-']


if __name__ == "__main__":
   main()