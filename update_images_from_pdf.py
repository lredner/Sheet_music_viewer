import pdf2image
import os
import threading

def convert_individual_pdf(source_pdf, target_image_folder, piece_name):
    pdf2image.convert_from_path(source_pdf, output_folder = target_image_folder, output_file = piece_name, fmt = 'png')

def convert_new_pdf_to_image(source_path, target_path):
    threads = []

    # iterate over contents of source for pdfs and convert if not converted
    for pdf in os.listdir(source_path):
        # ignore if not a pdf, or if the images folder exists and has content
        if not pdf.endswith('.pdf'):
            continue
        piece_name = pdf.split('.')[0]

        target_image_folder = os.path.join(target_path, piece_name)
        if os.path.exists(target_image_folder):
            if len(os.listdir(target_image_folder)) > 0:
                continue
        else:
            os.mkdir(target_image_folder)

        source_pdf = os.path.join(source_path, pdf)

        x = threading.Thread(target=convert_individual_pdf, args=(source_pdf,target_image_folder,piece_name,))
        x.start()
        threads.append(x)
    
    for index, thread in enumerate(threads):
        thread.join()
        