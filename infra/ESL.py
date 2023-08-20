import base64
import json, requests
import base64

from infra.img_proc import create_ESL_locker_img

COMPANY_CODE = 'JC10'
STORE_CODE = 1111

def trans_img_to_base64(src):
    with open(src, "rb") as img_file:
        base64_encoded = base64.b64encode(img_file.read()).decode("utf-8")
        return base64_encoded

def request_token():
    url="https://stage00.common.solumesl.com/common/api/v2/token"
    api_headers = {
        "accept":       "application/json",
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

    url=f"https://stage00.common.solumesl.com/common/api/v1/labels/contents/led?company={COMPANY_CODE}"
    api_headers = {
        "accept":        "application/json",
        "Authorization": f"{ESL_token_type} {ESL_token}",
        "Content-Type":  "application/json"
    }
    data = {
        "labelCode": label_code,
        "color":     "RED",
        "duration":  duration,
        "patternId": "0",
        "multiLed":  "false",
    }

    res = requests.put(url, data=json.dumps([data]), headers=api_headers)

    info = res.text
    parse = json.loads(info)
    print(parse)

def push_img_on_ESL():
    pass

def set_display_page(ESL_token_type, ESL_token, label_codes, page_index):
    url=f'https://stage00.common.solumesl.com/common/api/v1/labels/contents/page?company={COMPANY_CODE}'
    api_headers = {
        "accept":        "application/json",
        "Authorization": f"{ESL_token_type} {ESL_token}",
        "Content-Type":  "application/json",
    }
    data = {
        "labels": [ {
                "labelCode":    label_codes[i],
                "displayPage":  page_index,
            } for i in range(len(label_codes))
        ]
    }
    res = requests.post(url, data=json.dumps(data), headers=api_headers)
    info = res.text
    parse = json.loads(info)
    print(parse)
def broadcast_img(img_base64, ESL_token_type, ESL_token, label_codes, front_page, page_index):
<<<<<<< HEAD
    url=f"https://stage00.common.solumesl.com/common/api/v1/labels/contents/image?company={COMPANY_CODE}&stationCode={STORE_CODE}"
=======
    url=f"https://stage00.common.solumesl.com/common/api/v1/labels/contents/image?company={COMPANY_CODE}&stationCode={station_code}"
>>>>>>> 530e8d9487cfb097c1a8395aab5f55789c93d0d4

    api_headers = {
        "accept":        "application/json",
        "Authorization": f"{ESL_token_type} {ESL_token}",
        "Content-Type":  "application/json",
    }
    data = {
        "labels": [ {
                "labelCode": label_codes[i],
                "frontPage": front_page,
                
                "contents": [
                    {
                    "contentType": "image",
                    "imgBase64":    img_base64,
                    "pageIndex":    page_index,
                    "skipChecksumValidation": "true"
                    }
                ]
            } for i in range(len(label_codes))
        ]
    }   
    res = requests.post(url, data=json.dumps(data), headers=api_headers)

def trans_img_to_base64(src):
    with open(src, "rb") as img_file:
        base64_encoded = base64.b64encode(img_file.read()).decode("utf-8")
        return base64_encoded
    
token = None 

def get_token():
    global token
    if token is None:
        token = request_token()

    return token

def match_display(res_token, label_code, locker_num):
    create_ESL_locker_img(
        origin_img_src="./resource/ESL-locker.png",
        save_src="./resource",
        num=locker_num
    )
    
    broadcast_img(
        img_base64=trans_img_to_base64(f"./resource/ESL-locker-{locker_num}.png"),
        ESL_token_type=res_token["token_type"],
        ESL_token=res_token["access_token"],
        label_codes=[label_code],
        front_page=1,
        page_index=1,
        )
    set_display_page(
        ESL_token_type=res_token["token_type"],
        ESL_token=res_token["access_token"],
        label_codes=[label_code],
        page_index=1,
    )

#res = get_token()
# turn_on_LED(
#     ESL_token_type=res["token_type"],
#     ESL_token=res["access_token"],
#     label_code="0848A6EEE1DA",
#     duration="10s"
#     )
'''
broadcast_img(
    img_base64=trans_img_to_base64("./page1.png"),
    ESL_token_type=res["token_type"],
    ESL_token=res["access_token"],
    label_code="0848A6EEE1DA",
    front_page=2,
    page_index=2,
    )
'''