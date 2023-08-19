import json, requests
import base64

# PNG 파일 경로
png_file_path = "example.png"

# PNG 파일 읽기


def trans_img_to_base64(src):
    with open(src, "rb") as img_file:
        base64_encoded = base64.b64encode(img_file.read()).decode("utf-8")
        return base64_encoded

company_code = "JC10"
station_code = "1111"

def get_token():
    url="https://stage00.common.solumesl.com/common/api/v2/token"
    api_headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "username": "ymk051128@gmail.com",
        "password": "Blackwind1!"
    }
    
    res = requests.post(url, data=json.dumps(data), headers=api_headers)
    info = res.text
    parse = json.loads(info)
    
    print(parse)
        
    res_message = parse["responseMessage"]
    return res_message
    
def turn_on_LED( ESL_token_type, ESL_token, label_code, duration):
    url=f"https://stage00.common.solumesl.com/common/api/v1/labels/contents/led?company={company_code}"
    api_headers = {
        "accept": "application/json",
        "Authorization": f"{ESL_token_type} {ESL_token}",
        "Content-Type": "application/json"
    }
    data = {
        "labelCode": label_code,
        "color": "RED",
        "duration": duration,
        "patternId": "0",
        "multiLed": "false",
    }

    res = requests.put(url, data=json.dumps([data]), headers=api_headers)

    info = res.text
    parse = json.loads(info)
    print(parse)

def push_img_on_ESL():
    pass

def broadcast_img(img_base64, ESL_token_type, ESL_token, label_code, front_page, page_index):
    url=f"https://stage00.common.solumesl.com/common/api/v1/labels/contents/image?company={company_code}&stationCode={station_code}"

    api_headers = {
        "accept": "application/json",
        "Authorization": f"{ESL_token_type} {ESL_token}",
        "Content-Type": "application/json",
    }
    data = {
        "labels": [ {
                "labelCode": label_code,
                "frontPage": front_page,
                
                "contents": [
                    {
                    "contentType": "image",
                    "imgBase64": img_base64,
                    "pageIndex": page_index,
                    "skipChecksumValidation": "true"
                    }
                ]
            }
        ]
    }

    res = requests.post(url, data=json.dumps(data), headers=api_headers)

    info = res.text
    parse = json.loads(info)

res = get_token()
turn_on_LED(
    ESL_token_type=res["token_type"],
    ESL_token=res["access_token"],
    label_code="0848A6EEE1DA",
    duration="10s"
    )

broadcast_img(
    img_base64=trans_img_to_base64("./page1.png"),
    ESL_token_type=res["token_type"],
    ESL_token=res["access_token"],
    label_code="0848A6EEE1DA",
    front_page=3,
    page_index=3,
    )