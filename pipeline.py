from detector import *
from ocr import *
from utils import *

def main(args):
    # Get model
    dt_model, ocr_model = get_model(args)
    dt_output = detect_bubble_text(args, dt_model)
    ocr_output = get_text_from_bubble(args, ocr_model, dt_output)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)