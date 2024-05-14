import os
from PIL import Image
import pickle
from manga_ocr import MangaOcr
import paddleocr
import warnings
warnings.filterwarnings("ignore")

def crop_image(image, coordinates):
    cropped_img = image.crop(coordinates)
    return cropped_img

def get_OCR_model(ocr_language):
    '''
    Get OCR model according to the language the user want to translate from

    Args:
    ocr_language(str) : user define specific language to ocr from

    Return:
    model: OCR model
    '''

    # support languages
    support_language_short = ['jp', 'cn', 'kr', 'en']
    support_language_long = ['japan', 'china', 'korea', 'english']

    # Get model according to the language
    if ocr_language.lower() in support_language_short or support_language_long:
        if ocr_language == 'jp' or ocr_language == 'japan':
            model = MangaOcr()
        elif ocr_language == 'cn' or ocr_language == 'china':
            # model = PaddleOCR(with china in mind)
            raise NotImplementedError 
        elif ocr_language == 'kr' or ocr_language == 'korea':
            # model = PaddleOCR(with korea in mind)
            raise NotImplementedError
        elif ocr_language == 'en' or ocr_language == 'english':
            # model = PaddleOCR(with english in mind)
            raise NotImplementedError
    else:
        print("The language you want have NOT been implemented yet, stay tune for future update")
        raise NotImplementedError
    
    return model

def get_text_from_bubble(ocr_language, the_bubble_pkl_output): 
    '''
    OCR to get the text from the input bubble

    Args:
    ocr_language(str) : user define specific language to ocr from
    the_bubble_output(nested_dict): the output from bubble_text_detector.py

    Return:
    idk nested dict that append the text in? COCO JSON file? txt file?? 
    '''
    # Load from output.pkl (which is a nested dict by itself)
    if the_bubble_pkl_output.endswith('.pkl'):
        with open(the_bubble_pkl_output, 'rb') as file:
            nested_data = pickle.load(file)
    
    #TODO: implement if it load directly
    # # Load directly from the output (which is a nested dict by itself)
    # nested_data = the_bubble_output

    # Get ocr model based on the ocr_language user choose
    ocr_model = get_OCR_model(ocr_language)

    # Get info from the nested_data
    for k, value in nested_data.items():
        image_path = value['img']         # relative image path (images should be in a folder and that image folder should be put in the dataset folder [just create the dataset folder in the transflow folder by yourself cuz idk why Khanh not do it])
        full_image = Image.open(image_path)
        for bk, bubb_value in value['bubbles'].items():
            bubble_coordinate = bubb_value['coord'] # tuple vd: (1458, 313, 1598, 589)
            bubble_image = crop_image(image=full_image,
                                      coordinates=bubble_coordinate)
            text = ocr_model(bubble_image)
            bubb_value['text'] = text

    # dump to .pkl
    pkl_path = os.path.join('/home/doki/Code_workspace/EXE_project/', 'output_with_jap_text.pkl')
    with open(pkl_path, 'wb') as file:
        pickle.dump(nested_data, file)
    return nested_data

x = get_text_from_bubble('jp', '/home/doki/Code_workspace/EXE_project/transflow/TEST/output.pkl')
print(x)         



            

