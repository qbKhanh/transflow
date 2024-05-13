import argparse
import time
import os
import pickle
from pathlib import Path

from ultralytics import YOLO
from ultralytics import YOLO
from PIL import Image
import cv2


def get_parser():
    parser = argparse.ArgumentParser(description='Detect bubble text')
    # input/output
    parser.add_argument('--image', type=str, help='path to image or image folder')
    parser.add_argument('--output', type=str, default='', help='path to save the output')

    # YOLO options
    parser.add_argument('--weight', type=str, default='checkpoints/comic-speech-bubble-detector-640.onnx', help='path to pretrained weight')
    parser.add_argument('--device', type=str, default='cpu', help='device to use (cpu, cuda:0, cuda:1, ...)')
    parser.add_argument('--conf', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou', type=float, default=0.7, help='IoU threshold')
    parser.add_argument('--save-crop', action='store_true', help='save crop bubble text')
    parser.add_argument('--save-output', action='store_true', help='save output of detection')
    return parser

def get_model(args):
    '''
    Load the YOLO model
    Args:
        weight: path to the pretrained weight
    Returns:
        model: YOLO model    
    '''
    model = YOLO(args.weight, task='detect')
    return model

def main(args):
    '''
    Detect bubble text in image
    Args:
        image|str: path to the image or image folder
        output|str: path to save the output (pkl file)
        weight|str: path to the pretrained weight (YOLO)
        device|str: device to use (cpu, cuda:0, cuda:1, ...)
        conf|float: confidence threshold
        iou|float: IoU threshold
    Returns:
        result_info|nested_dict: detection information
            {
            'img_0': {
                'img': original image,
                'bubbles': {
                    'bubble_0': {
                        'coord': (x1, y1, x2, y2),
                        },
                    ...
                    },
                },
            ...
            }
    
    '''
    start_time = time.time()
    # Load the YOLO model
    model = get_model(args)
    # Detect bubble text
    results = model.predict(source=args.image, device=args.device)
    output_dict = dict() # Save the detection information
    
    # Loop through each image
    for i, result in enumerate(results):
        bubble_dict = dict() # save bubble text information
        coords = result.boxes.xyxy
        # Save the crop bubble text
        if args.save_crop:
            os.makedirs(args.output, exist_ok=True)
            result.save_crop(f'{args.output}', file_name=Path('im'))
        # Loop through each bubble text of an image
        for j, coord in enumerate(coords):
            # Get coordinates of the bubble text
            bubble_dict[j] = {'coord':(int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3]))}
            
        # Get all information
        output_dict[i] = {
            'img': result.orig_img,
            'bubbles': bubble_dict
        }

    if args.save_output:
        os.makedirs(args.output, exist_ok=True)
        pickle_path = args.output + '/output.pkl'
        # Save detection infor to a pickle file
        with open(pickle_path, 'wb') as file:
            pickle.dump(output_dict, file)

    end_time = time.time()
    print(f"Time taken: {round(end_time - start_time, 2)} seconds")

    return output_dict

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)
