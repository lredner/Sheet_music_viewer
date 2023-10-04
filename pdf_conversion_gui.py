import PySimpleGUI as sg
import os
from update_images_from_pdf import convert_new_pdf_to_image, change_colour_background

def are_new_pdfs_available(source_path, target_path, new_pdfs):
   # strip extension for comparison
   pdfs = [pdf.split('.')[0] for pdf in os.listdir(source_path) if pdf.endswith('.pdf')]
   target_contents = os.listdir(target_path)
   for pdf in pdfs:
      if pdf not in target_contents:
         new_pdfs.append(pdf + '.pdf')
   
   return len(new_pdfs)>0

class PdfWindowGui:
   def __init__(self, source_path, target_path, new_pdfs, size):
      # display progress bar at top, bottom left 'convert pdfs', centre bottom sepia tone? ,bottom right continue to sheet music viewer
      layout = [[sg.ProgressBar(max_value=len(new_pdfs), orientation='h', size_px=(500, 20), key='-CONVERSION_PROGRESS-')],
                           [sg.Button(button_text=f'Convert {len(new_pdfs)} new pdf(s)', key = '-CONVERT_BUTTON-', auto_size_button=True, enable_events=True),
                           sg.Checkbox(text='Eye Friendly Sheet Music (Sepia Toned)', key = '-SEPIA-', enable_events=True, default = True),
                           # sg.Checkbox(text='Create MIDI', key = '-MIDI-', enable_events=True, default = False),
                           sg.Button(button_text='Skip to Viewer', key = '-SKIP_BUTTON-', auto_size_button=True, enable_events=True)]
                           ]
      window = sg.Window("PDF Conversion", layout, resizable=True, finalize = True, element_justification='c')

      while True:
         event, values = window.read()
         if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            break
         if event == '-SKIP_BUTTON-':
            window.close()
            break
         if event == '-CONVERT_BUTTON-':
            for ii, pdf in enumerate(new_pdfs):
               convert_new_pdf_to_image(source_path, target_path, pdf)
               if values['-SEPIA-']:
                  change_colour_background(os.path.join(target_path, pdf.split('.')[0]))
               window['-CONVERSION_PROGRESS-'].update(current_count = ii+1)
               window.refresh()
            window.close()
            break

if __name__ == "__main__":
   quit()