import os
import json


def select():
    input_dir = r"../../CHpaper_sample_200/"
    output_dir = r"../../CHpaper_OCR_samples/"
    for file in os.listdir(input_dir):
        with open(input_dir + file, 'r') as fi:
            data = json.load(fi)
            if data["need_ocr"]:
                with open(output_dir + file, 'w') as fo:
                    fo.write(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    select()

