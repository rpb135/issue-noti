import numpy as np
import json
import requests
import time

from collections import Counter
from jira import JIRA
from datetime import datetime, timedelta

options = {'server':'https://jira.주소/'}
jira = JIRA(options, basic_auth=("jhhwang", "password"))
issueNum = []
tmpNum = []
issueDir = {}
# sDate = ""
# eDate = ""
# sDate = now.date()
# eDate = now.date() + timedelta(days=2)

jira_Date_SQL = 'created >= -1m AND reporter in (보고자 ID)'
# print(jira_Date_SQL)

while True:
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    for issue in jira.search_issues(jira_Date_SQL, maxResults=5):
        # print('{} : {}'.format(issue.key, issue.fields.summary))
        if issue.key in issueNum:
            break
        issueDir[issue.key] = issue.fields.summary
        issueNum.append(issue.key)
    
    # print("저장된 이슈번호 : ", tmpNum)
    # print("업데이트 이슈번호 : ", issueNum)
    if(issueNum):
        # issueNum 요소가 존재 함 = 새로운 이슈가 있음

        if(np.array_equal(issueNum, tmpNum)):
            # tmpNum 요소가 존재하지만 issueNum,과 같은 요소라면 둘다 초기화
            del issueNum
            del tmpNum
            issueNum = []
            tmpNum = []
            time.sleep(60)

        else:
            # tmpNum과 issueNum이 다르다면 새로운 이슈가 생성 됨
            print("새로운 이슈가 생성 되었습니다.")

            for key, val in issueDir.items():
                if key not in tmpNum:
                    print(key)

                    jiraStr = "**["+ key +"](https://jira.ktmusic.co.kr/browse/"+ key +")\n**"

                    webhook_url= "https://hooks.glip.com/webhook/029cc970-0192-4fbc-bc42-7b3a9e1757fa"
                    payload= {
                        "icon": "https://image.flaticon.com/icons/png/512/1447/1447436.png",
                        "title": jiraStr + val
                    }

                    requests.post(
                        webhook_url, data=json.dumps(payload),
                        headers={'Content-Type':'application/json'}
                    )
                    
                    tmpNum.append(key)
                # print("tmpNum 배열 값 : ", tmpNum)
                # print("issueNum 배열 값 : ", issueNum)
            del issueDir
            issueDir = {}

    else:
        # 새로운 이슈가 없음
        print("새로 등록된 이슈가 없습니다. 현재 시간 :", now)

        time.sleep(60)
