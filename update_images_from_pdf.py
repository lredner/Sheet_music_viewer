try:
    import pdf2image
    import os
    from PIL import Image
    import numpy as np
    import copy
except ImportError:
   print('Missing required module. Install requirements.txt')
   quit()

def convert_new_pdf_to_image(source_path, target_path, pdf):

    piece_name = pdf.split('.')[0]

    target_image_folder = os.path.join(target_path, piece_name)
    os.mkdir(target_image_folder)

    source_pdf = os.path.join(source_path, pdf)
    pdf2image.convert_from_path(source_pdf, output_folder = target_image_folder, output_file = piece_name, fmt = 'png', thread_count = 4)
        

def change_colour_background(target_image_folder):
    for image in os.listdir(target_image_folder):
        im = Image.open(os.path.join(target_image_folder, image))
        im_matrix = np.array(im, dtype = np.int32)
        updated_matrix = copy.deepcopy(im_matrix)
        updated_matrix[:,:,0] = (0.0393*im_matrix[:,:,0] + 0.0769*im_matrix[:,:,1] + 0.0189*im_matrix[:,:,2])*7.5
        updated_matrix[:,:,1] = (0.0349*im_matrix[:,:,0] + 0.0686*im_matrix[:,:,1] + 0.0168*im_matrix[:,:,2])*7.5
        updated_matrix[:,:,2] = (0.0272*im_matrix[:,:,0] + 0.0534*im_matrix[:,:,1] + 0.0131*im_matrix[:,:,2])*7.5
        updated_matrix[updated_matrix>255] = 255
        updated_image = Image.fromarray(updated_matrix.astype(np.uint8))
        updated_image.save(os.path.join(target_image_folder, image))
        # tr = 0.393R + 0.769G + 0.189B
        # tg = 0.349R + 0.686G + 0.168B
        # tb = 0.272R + 0.534G + 0.131B

if __name__ == "__main__":
   quit()