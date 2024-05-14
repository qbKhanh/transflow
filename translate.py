import pandas as pd
import translators as ts
import pickle

def translate(data):
    for key, value in data.items():
        temp_list = []
        for key, small_value in value['bubbles'].items():
            temp_list.append(small_value['text'])
        if len(temp_list) == 0:
            continue #don't need to translate an empty list
        temp_text = "\n".join(temp_list)
        trans_text = ts.translate_text(temp_text, translator = "bing", from_language = 'ja', to_language='vi')
        temp_text = ""
        trans_list = trans_text.split('\n')
        if len(trans_list) != len(temp_list):
            print('translate wrong', len(trans_list), len(temp_list))
            continue
        counter = 0
        for key, small_value in value['bubbles'].items():
            small_value['trs_text'] = trans_list[counter]
            counter += 1
    return data