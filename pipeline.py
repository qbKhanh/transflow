from modules.detector.detector import *
from modules.ocr.ocr import *
from modules.translate.translate import *
from modules.detector.text_segment import *
from modules.render.render import *
from modules.utils import *

def main(args):
    # Get model
    # ocr_model, sg_model = get_model(args)
    # sg_output = segment_text(args, sg_model)
    # ocr_output = get_text_from_bubble(args, ocr_model, sg_output)
    # trs_output = translate(args, ocr_output)

    # trs_path = args.output + '/output_trs.pkl'
    # # Save detection infor to a pickle file
    # with open(trs_path, 'wb') as file:
    #     pickle.dump(trs_output, file)

    trs_path = args.output + '/output_trs.pkl'
    with open(trs_path, 'rb') as file:
        trs_output = pickle.load(file)

    render(args, trs_output)


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)