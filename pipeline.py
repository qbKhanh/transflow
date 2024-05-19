from detector import *
from ocr import *
from translate import *
from text_segment import *
from utils import *

def main(args):
    # Get model
    ocr_model, sg_model = get_model(args)
    sg_output = segment_text(args, sg_model)
    ocr_output = get_text_from_bubble(args, ocr_model, sg_output)
    trs_output = translate(ocr_output)
    
    trs_path = args.output + '/output_trs.pkl'
    with open(trs_path, 'wb') as file:
        pickle.dump(trs_output, file)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)