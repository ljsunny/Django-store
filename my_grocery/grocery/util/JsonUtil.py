import os
import shutil
import json

class JsonUtil:
    def readFile(dir):
        if os.path.exists(dir):
            file = open( dir , "r")
            list = json.loads(file.read())
            file.close()
            return list
        else:
            return []


    def writeFile(dir, content):
        file = open( dir , "w")
        file.write(json.dumps(content))
        file.close()
        return list

    def appendFile(file_path, content):
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write("[]")

        with open(file_path, "r+") as file:
            data = file.read()
            if len(data) > 2:  # 기존 데이터가 있으면, 콤마로 구분해서 추가
                file.seek(file.tell() - 1)  # 마지막 위치로 이동 (닫는 대괄호 `]` 바로 앞)
                file.truncate()  # 마지막 문자(`]`) 제거
                file.write("," + json.dumps(content) + "]")
            else:
                # 파일이 빈 배열 `[]`일 경우, 안에 첫 번째 항목으로 추가
                file.seek(1)  # 대괄호 `[` 뒤로 이동
                file.write(json.dumps(content) + "]")
    

