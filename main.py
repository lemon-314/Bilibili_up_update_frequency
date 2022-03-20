import requests
from plotly import graph_objects as go
import json
from datetime import datetime

def main(mid):
    # 爬页数
    heads = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}

    response = requests.get(f"https://api.bilibili.com/x/space/arc/search?mid={mid}&pn=999", headers=heads)
    json_dict = json.loads(response.text)

    count = json_dict["data"]["page"]["count"]
    pns = count//30+1 if count%30 else count//30 # 视频数->页数(30一页)

    dates = []
    cha = []

    # 爬日期
    print(f"开始爬数据, 共{pns:02}面")
    for pn in range(1, pns+1):
        print(f"第{pn:02}面, 共{pns:02}面")
        response = requests.get(f"https://api.bilibili.com/x/space/arc/search?mid={mid}&pn={pn}", headers=heads)
        json_dict = json.loads(response.text)
        for i in json_dict["data"]["list"]["vlist"]:
            date = datetime.fromtimestamp(i["created"])
            dates.append(str(date)[:10])

    #求差
    for i, d in enumerate(dates[:-1]):
        d1 = datetime.strptime(d, "%Y-%m-%d")
        d2 = datetime.strptime(dates[i+1], "%Y-%m-%d")
        cha.append((d1 - d2).days)
    cha = [0] + cha


    # print(dates)
    # print(cha)


    # 划分等级
    print("数据以爬完, 正在整理, 请稍后······")
    level = []
    for i in cha:
        if i<=3: level.append("Turquoise")
        elif i<=7: level.append("SpringGreen")
        elif i<=10: level.append("Gold")
        elif i<=20: level.append("Red")
        else: level.append("DarkRed")

    line = go.Scatter(x=dates, y=cha, line={"color":"grey"}, mode="lines", name="")
    scatter = go.Scatter(x=dates, y=cha, marker={"color":level}, mode="markers", name="等级")
    fig  = go.Figure((line, scatter))
    fig.show()


if __name__ =="__main__":
    mid = input("UID: ")
    main(mid)
    
