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
                'bubble_0': {
                    'coord': (x1, y1, x2, y2),
                    },
                ...
                },
            ...
            }
    
    '''
    start_time = time.time()
    # Load the YOLO model
    model = get_model(args)
    # Detect bubble text
    results = model.predict(source=args.image, device=args.device)
    result_info = dict() # Save the detection information
    
    # Loop through each image
    for i, result in enumerate(results):
        sub_dict = dict()
        coords = result.boxes.xyxy
        # Save the crop bubble text
        if args.save_crop:
            result.save_crop(f'{args.output}', file_name=Path('im'))
        # Loop through each bubble text of an image
        for j, coord in enumerate(coords):
            
            info_dict = dict()
            # Get coordinates of the bubble text
            info_dict['coord'] = (int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3]))
            # Get the bubble text image
            # info_dict['img'] = result.orig_img[int(coord[1]):int(coord[3]), int(coord[0]):int(coord[2])]

            sub_dict[j] = info_dict
        # Get the original image
        result_info['img'] = result.orig_img
        # Get the bubble text information
        result_info[i] = sub_dict

        if args.save_output:
            pickle_path = args.output + '/output.pkl'
            # Save detection infor to a pickle file
            with open(pickle_path, 'wb') as file:
                pickle.dump(result_info, file)

    end_time = time.time()
    print(f"Time taken: {round(end_time - start_time, 2)} seconds")

    return result_info

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)
