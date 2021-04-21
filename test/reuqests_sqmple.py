# Rest API 파라미터
import json
# Rest API 호출
import requests


# JSON 파라미터 정의
in_params_dict = {
    "Session": {
        "usrId": "upload_opt_value",
        "sysDttm": current_dtm,
        "pgmNm": "upload_opt_value",
        "jobId": 0,
        "jobGrpId": 0,
        "osPrcsId": 0,
        "url": "",
        "step": ""
    },
    "InParm": [
        "A_COL": "first",
        "C_COL": "Second",
    ]
}
# JSON 파라미터 생성
param_json_data = json.dumps(opt_validation_dict, ensure_ascii=False, indent="\t")
# REST API 서버 호출을 위한 주소 설정
url_rest_api = rest_api_ip_addr_port + "/de/excel"
print(url_rest_api)
# JSON 파라미터로 서버 호출
response = requests.get(url_rest_api, headers=headers, data=param_json_data)
# 결과를 JSON 형태로 변환
result_json = response.json()
# 결과코드 확인. 던져주는 쪽에서 어떻게 던지느냐에 따라 다름. JSON 형태, 딕셔너리로 받는게 일반적임.
result_code = result_json["OutResult"]["rtnCd"]
# rest api 오류인 경우
if result_code != 1:
    print(response)