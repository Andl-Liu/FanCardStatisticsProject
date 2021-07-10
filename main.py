# Author: Andl
# Time: 2021/7/10
#
# url解析：
#   本体：https://api.bilibili.com/x/v2/reply/main
#   参数:
#       callback: 可不需要
#       jsonp: 可不需要
#       next: 当mode=1时，按时间从晚到早排序，当为第一批被加载出来的评论时，该参数为0，否则该参数为上一批被加载出来的评论的最后一个评论的楼层号；
#             当mode=3时，按热度从高到低排序，当为第一批被加载出来的评论时，该参数为0，除此之外，当为第n批被加载出来的评论时，该参数为n
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

import requests

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

reps = requests.get(url=url, params=params, headers=headers)

print(reps.json())
