import os
import cv2
from PIL import Image
import pickle

import numpy as np

from ultralytics import YOLO
from remove_text import *

def segment_text(args, sg_model=None, trs_output=None):
    '''
    Segment the text from the bubble and remove it
    Args:
        args: arguments
        sg_model: YOLO model for segmenting text
        trs_output: translated output
    Returns:
        nested_data: nested dictionary containing the segmented text
            additional key: 'removed_image': path to the image with removed text
    '''
    if trs_output:
        nested_data = trs_output
    else:
        bubble_pkl_output = os.path.join(args.output, 'output_dt.pkl') 
        if bubble_pkl_output.endswith('.pkl'):
            with open(bubble_pkl_output, 'rb') as file:
                nested_data = pickle.load(file)

    # Load the model
    if sg_model:
        model = sg_model
    else:
        model = YOLO(args.sg_weight, task='segment')
    
    images_list = [nested_data[i]['img'] for i in range(len(nested_data))]

    # Perform prediction
    results = model.predict(source=images_list, device=args.device) 

    # Visualize the segmentation masks
    for idx, result in enumerate(results):
        # Load the image using OpenCV
        image_path = result.path
        original_image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        # Loop through each segmentation result
        # print(result.path.split('/')[-1])
        for mask in result.masks:
            # Convert the mask to a binary mask
            binary_mask = mask.data.cpu().numpy().astype(np.uint8)
            
            # Ensure the binary_mask is 2D
            if binary_mask.ndim == 3:
                binary_mask = binary_mask.squeeze(0)
            
            # Resize the binary mask to match the original image size
            binary_mask = cv2.resize(binary_mask, (original_image.shape[1], original_image.shape[0]), interpolation=cv2.INTER_NEAREST)
            
            # Replace the segment area with white color
            removed_image = simple_remove(image_rgb, binary_mask)

        # Convert the image back to BGR format for OpenCV
        removed_image = cv2.cvtColor(removed_image, cv2.COLOR_RGB2BGR)

        # Save the result
        if 1:
            os.makedirs(f"{args.output}/remove", exist_ok=True)
            cv2.imwrite(f"{args.output}/remove/{result.path.split('/')[-1]}", removed_image)
        nested_data[idx]['removed_image'] = f"{args.output}/remove/{result.path.split('/')[-1]}"

    return nested_data

