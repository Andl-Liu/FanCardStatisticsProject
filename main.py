# Author: Andl
# Time: 2021/7/10
#
# url解析：
#   本体：https://api.bilibili.com/x/v2/reply/main
#   参数:
#       callback: 可不需要
#       jsonp: 可不需要
#       next: 当mode=1时，按时间从晚到早排序，当为第一批被加载出来的评论时，该参数为0，否则该参数为上一批被加载出来的评论的最后一个评论的楼层号；
#             当mode=3时，按热度从高到低排序，当为第一批被加载出来的评论时，该参数为0，除此之外，当为第n批被加载出来的评论时，该参数为n;
#             next=0时，代表开始；
#             next=1时，代表结束；
# #     type: 不明，但都为1
#       oid: av号
#       mode: 评论显示方式，当mode=2时，按时间从晚到早排序，当mode=3时，按热度从高到低排序
#       plat: 不明，但都为1
#       _: 可不需要
#
# 评论的加载方式:
#   当按热度排序时，每批评论都会加载出20条;
#   当按时间排序时，将要加载的20条评论中，若是有被抽楼的，则不会在被传回来的json文件中，也就是说每次并不都是20条评论
#
# 为了方便统计评论的时间和被抽的楼层数，我决定采用按时间排序的方法获取评论
import time
import requests
import csv


def process_data(reps, csv_writer):
    # json数据
    comments_json = reps.json()
    comments_json = comments_json["data"]["replies"]
    # 用于储存需要的评论数据
    dic = {}

    floor = 1
    for comment in comments_json:
        # 楼层
        dic["floor"] = comment["floor"]
        floor = comment["floor"]
        # 评论时间
        dic["ctime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment["ctime"]))

        member = comment["member"]
        # 用户名称
        dic["user_name"] = member["uname"]
        # 用户性别
        dic["user_sex"] = member["sex"]
        # 用户等级
        dic["user_level"] = member["level_info"]["current_level"]
        # 用户会员等级
        vip = "普通会员"
        if member["vip"]["vipType"] == 1:
            vip = "大会员"
        elif member["vip"]["vipType"] == 2:
            vip = "年度大会员"
        dic["vip_level"] = vip

        # 装扮名称
        dic["fanCard_name"] = "无"
        # 装扮编号
        dic["fanCard_id"] = "000000"
        # 装扮所属up主
        dic["fanCard_up"] = "无"
        if member["user_sailing"].get("cardbg", 0):
            cardbg = member["user_sailing"]["cardbg"]
            dic["fanCard_name"] = cardbg["name"]
            dic["fanCard_id"] = cardbg["fan"]["num_desc"]
            dic["fanCard_up"] = cardbg["fan"]["name"]

        # 评论内容
        dic["content"] = comment["content"]["message"].replace("\n", "\\n")

        # 保存到文件中
        csv_writer.writerow(dic.values())
    print(f"已处理至{floor}")
    return floor


if __name__ == "__main__":
    url = "https://api.bilibili.com/x/v2/reply/main"

    headers = {
        "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }

    params = {
        "next": 0,
        "type": 1,
        "oid": 797915674,
        "mode": 2,
        "plat": 1
    }

    f = open(".\\data.csv", mode="w", newline="", encoding='utf-8')
    csvWriter = csv.writer(f)

    # 表头
    header = ["楼层号", "评论时间", "用户名称", "用户性别", "用户等级", "用户会员等级", "装扮名称", "装扮编号", "装扮所属up主", "评论内容"]
    # 写入表头
    csvWriter.writerow(header)

    page = 0
    while page != 1:
        # 更新参数
        params["next"] = page
        # 获取评论
        response = requests.get(url=url, params=params, headers=headers)
        # 加工数据
        page = process_data(response, csvWriter)
        response.close()

    f.close()

