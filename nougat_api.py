import requests
import os


def predict(file_path):
    if not file_path.endswith(".pdf"):
        raise ValueError("File must be a PDF")
    # url = "http://143.89.126.16:8503/predict/"
    url = "http://127.0.0.1:8503/predict/"
    file_name = os.path.basename(file_path)
    files = {'file': (file_name, open(file_path, 'rb'))}
    data = {
        "start": 1,  # Optional
        "stop": 5   # Optional
    }

    response = requests.post(url, files=files)
    print(response.text)
    return response.text


def main():
    test_file = "../test_pdf/test_pdf_ch.pdf"
    predict(test_file)


if __name__ == "__main__":
    main()












