import PySimpleGUI as sg
from screeninfo import get_monitors
from update_images_from_pdf import convert_new_pdf_to_image
import os
import PIL.Image
import io

def convToBytes(image, resize=None):
	img = image.copy()	
	cur_width, cur_height = img.size
	if resize:
		new_width, new_height = resize
		scale = min(new_height/cur_height, new_width/cur_width)
		img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)	
	ImgBytes = io.BytesIO()
	img.save(ImgBytes, format="PNG")
	del img
	return ImgBytes.getvalue()


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
    print('Converting new pdfs to images')
    convert_new_pdf_to_image(source_pdf_path, target_path)

    # get the list of sheet music
    sheet_music_list = [pdf.split('.')[0] for pdf in os.listdir(source_pdf_path) if pdf.endswith('.pdf')]

    # format it e.g. Moonlight_Sonata__Beethoven -> Moonlight Sonata\nBeethoven
    sheet_music_list = [name.replace('__', ' - ').replace('_', ' ') for name in sheet_music_list]
    longest_entry = len(max(sheet_music_list, key=len))

    file_list_column = [
        [
            sg.Listbox(values=sheet_music_list, enable_events=True, size=(min(int(0.3*screen_width_char), longest_entry), screen_height_char), 
                       key="-MUSIC_LIST-", font=('Arial Bold', 15), select_mode = "LISTBOX_SELECT_MODE_SINGLE")
        ]
    ]

    sheet_music_viewer_column = [
        [
            sg.Image(key="-SHEET_MUSIC-")
        ]
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(sheet_music_viewer_column)
        ]
    ]

    window = sg.Window("Sheet Music Viewer", layout, resizable=True, size = (screen_width_pixels, screen_height_pixels))

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
            filename = os.path.join(image_path, os.listdir(image_path)[0])
            window["-SHEET_MUSIC-"].update(data = convToBytes(PIL.Image.open(filename), window['-SHEET_MUSIC-'].get_size()))

if __name__ == "__main__":
    main()