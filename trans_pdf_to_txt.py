import fitz  # PyMuPDF
import json
import re
import logging
import nougat_api
import molar_ocr_api
import os
import time
from wenxin_gpt_api import wenxin_correct
from postprocess import post_process_api
logging.basicConfig(level=logging.INFO)  # 设置日志级别为DEBUG
non_english_pattern = re.compile(r'[^a-zA-Z\s\d.,!?;]')


def postprocess(ori_result):
    if ori_result.get("gpt_correct_result", None):
        curr_result = ori_result["gpt_correct_result"]
    elif ori_result.get("ocr_result", None):
        curr_result = ori_result["ocr_result"]
    elif ori_result.get("fitz_extract_text", None):
        curr_result = ori_result["fitz_extract_text"]
    else:
        return ori_result
    post_res = post_process_api.process(curr_result)
    ori_result["post_processed_text"] = post_res
    return ori_result


def gpt_correct_text(text):
    # use wenxin api to correct text
    instructions_path = r"instructions/wenxin_ocr_correction_ins.txt"
    with open(instructions_path, "r", encoding="utf-8") as fi:
        prompt = fi.read()
    result = wenxin_correct(prompt, text)
    return result


def count_non_english_chars(text):
    # 匹配非英文字符，包括非拉丁字母、数字、标点符号和空白
    non_english_chars = non_english_pattern.findall(text)
    return len(non_english_chars)


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    doc.close()
    return text


def single_process(pdf_path, output_path, selected_ocr="nougat"):
    global ocr_time_costing, gpt_time_costing, ocr_count, gpt_count
    if os.path.exists(output_path):
        logging.info("already exists, skip it")
        return
    text_valid = False
    result = {"file_path": pdf_path,
              "file_name": pdf_path.split("/")[-1],
              "fitz_extract_text": None,
              "post_processed_text": None,
              "need_ocr": False,
              # "need_ocr": True,
              "ocr_result": None,
              "need_gpt": True,
              # "need_gpt": False,
              "gpt_correct_result": None,
              # "language": "English",
              }
    # directly extract text from pdf
    try:
        text = extract_text_from_pdf(pdf_path)
        # todo: 判断是否是一份既包含"图片文字"又包含"文本元素"的PDF
        if not text or len(text) < 10:
            result["need_ocr"] = True
        else:
            text_valid = True
            result["fitz_extract_text"] = text
    except Exception as e:
        result["need_ocr"] = True
        logging.info(str(e) + "cannot directly extract text from this pdf " + pdf_path.split("/")[-1])

    # call ocr
    ocr_text = None
    if result["need_ocr"]:
        try:
            start = time.time()
            if selected_ocr == "nougat":
                ocr_text = nougat_api.predict(pdf_path)
            else:
                ocr_text = molar_ocr_api.parsePdf(pdf_path)
            # todo: 判断是否是一份非英文且"图片形式"的PDF
            if ocr_text and len(ocr_text) > 10:
                result["ocr_result"] = ocr_text
                text_valid = True
                logging.info("ocr recognized this file " + pdf_path.split("/")[-1])
            logging.info("ocr costing time " + str(time.time() - start) + "s")
            ocr_time_costing += time.time() - start
            ocr_count += 1
            logging.info("total ocr_count is " + str(ocr_count) +
                         "\ntotal ocr time is " + str(ocr_time_costing))
        except Exception as e:
            logging.info(str(e) + "nougat cannot recognize this file " + pdf_path.split("/")[-1])

    # use gpt to correct the result of ocr
    if result["need_ocr"] and text_valid:
        result["need_gpt"] = True

    if result["need_gpt"]:
        start = time.time()
        if result["need_ocr"]:
            text = ocr_text
        else:
            text = result["fitz_extract_text"]
        result["gpt_correct_result"] = gpt_correct_text(text)
        logging.info("gpt costing time " + str(time.time() - start) + "s")
        gpt_count += 1
        gpt_time_costing += time.time() - start
        logging.info("total gpt_count is " + str(gpt_count) +
                     "\ntotal gpt_time_costing is " + str(gpt_time_costing))

    # save result to file
    if not text_valid:
        logging.info("text is not valid, " + pdf_path)
    else:
        result = postprocess(result)
        with open(output_path, "w", encoding="utf-8") as fo:
            fo.write(json.dumps(result, ensure_ascii=False))


def pipeline(input_dir, output_dir, selected_ocr="nougat"):
    global count
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".pdf"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
                single_process(input_path, output_path, selected_ocr)
                count += 1
                if count % 1 == 0:
                    logging.info(str(count) + " files processed")


def test_fitz():
    # pdf_path = "../test_pdf/test_pdf_1.pdf"
    pdf_path = "../test_pdf/test_pdf_ch.pdf"
    output_path = "../test_pdf/res_ch_1.json"
    # pdf_path = "../test_pdf/test_pdf_ch.pdf"
    result = extract_text_from_pdf(pdf_path)
    with open(output_path, "w", encoding="utf-8") as fo:
        fo.write(json.dumps(result, ensure_ascii=False))


def test_pipeline():
    input_dir = r"test_data/ch_pdf_dir/"
    output_dir = r"test_data/ch_result_dir/"
    # input_dir = r"/ML-A100/data/CHpaper"
    # output_dir = r"/ML-A100/data/CHpaper_0907_sample/"
    selected_ocr = "molar"
    pipeline(input_dir, output_dir, selected_ocr=selected_ocr)


if __name__ == '__main__':
    count = 0
    ocr_count = 0
    gpt_count = 0
    ocr_time_costing = 0
    gpt_time_costing = 0
    test_pipeline()

