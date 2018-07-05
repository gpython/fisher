#encoding:utf-8

#处理礼物清单 或 心愿清单 的用户列表
#处理一组数据 先处理单个数据
#用户昵称 创建时间 id
class TradeInfo:
  def __init__(self, goods):
    self.total = 0
    self.trades = []
    self.__parse(goods)

  def __parse(self, goods):
    self.total = len(goods)
    self.trades = [self.__map_to_trade(single) for single in goods]

  def __map_to_trade(self, single):
    if single.create_datetime:
      time = single.create_datetime.strftime("%Y-%m-%d")
    else:
      time = "None"
    return dict(
      user_name = single.user.nickname,
      time=time,
      id=single.id
    )
