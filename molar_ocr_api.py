import requests
from io import BytesIO
from docx import Document


def requestDoc(pdf):
    try:
        # url = 'http://relay.molardata.com:42315/smart-tool/pdf2docx/'
        # url = "http://relay.molardata.com:28474/smart-tool/pdf2docx/"
        url = "http://relay.molardata.com:28474/smart-tool/pdf2docx-cn-pt"
        payload = {'file': open(pdf, 'rb')}
        headers = {
            'accept': 'application/json',
        }
        response = requests.post(url, headers=headers, files=payload)
        return response.content
    except Exception as e:
        print(f'请求错误 {pdf}: {str(e)}')


def parsePdf(pdf):
    doc = requestDoc(pdf)
    docx_file = BytesIO(doc)
    document = Document(docx_file)
    textContent = ''
    for p in document.paragraphs:
        textContent = textContent + p.text
    return textContent


def test():
    file_path = r"test_data/pdf_dir/0905_2_ch.pdf"
    text = parsePdf(file_path)
    print(text)


if __name__ == '__main__':
    test()
