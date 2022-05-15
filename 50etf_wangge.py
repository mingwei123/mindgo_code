import datetime

#初始化账户
def init(context):
    g.stock='510050.OF'
    set_benchmark(g.stock)
    # 50etf的基准年份：2022年
    day_str = get_datetime().strftime('%Y') 
    g.start_year = int(day_str)  # 开始年份
    g.check_year = 2022
    g.start_price = 3.2 / (1.08** (g.check_year - g.start_year)) # 获得开始的价格                                                                                      
    g.x1 = 0.03   # 下跌多少买入 
    g.x2 = 0.03   # 上涨多少卖出
    
    g.p = g.start_price #记录上一次交易的价格
    g.p1 = g.p - g.x1 #下次买入价 
    g.p2 = g.p + g.x2 #下次卖出价
    
    g.positions = 0 # 仓位
    log.info("start_price:{}".format(g.start_price))
    
    g.init = 0 # 账户初始化
    
def handle_bar(context,bar_dict):
    date=get_datetime().strftime('%Y%m%d %H%M%S') 
    day_str = get_datetime().strftime('%Y') 
    if int(day_str) - g.start_year > 0:
        log.info("按年增加年化8%:{},{}".format(g.start_price, g.start_price * 1.08))
        g.start_price *= 1.08
        g.p = g.start_price #记录上一次交易的价格
        g.p1 = g.p - g.x1 #下次买入价 
        g.p2 = g.p + g.x2 #下次卖出价
        g.start_year = int(day_str)
    
    end_date = get_datetime() + datetime.timedelta(days=1)
    df = get_price(securities='510050.OF', start_date=get_datetime(),end_date =get_datetime(),  fre_step='1m', fields=['close'])
    
    for p in df["close"]:
        if g.init == 0:
            if p < g.start_price:
                order(g.stock, 17000)
                g.positions += 0.04
                log.info('时间：{}，执行买入操作，价位：{}，数量：{}, 仓位数：{}'.format(date,p, "4%", g.positions))
                log.info(context.portfolio.stock_account)
                g.p=p  
                g.p1 = g.p - g.x1 
                g.p2 = g.p + g.x2
                g.init += 1
                log.info("当前价：{}，下次买入价：{}，下次卖出价：{}".format(g.p, g.p1, g.p2))
        else:
            if p <=g.p1: 
                order(g.stock, 17000)
                g.p=p  
                g.p1 = g.p - g.x1 
                g.p2 = g.p + g.x2
                g.positions += 0.04
                log.info('时间：{}，执行买入操作，价位：{}，数量：{}, 仓位数：{}'.format(date,p, "4%", g.positions))          
                log.info("当前价：{}，下次买入价：{}，下次卖出价：{}".format(g.p, g.p1, g.p2))
            elif p>g.p2 and context.portfolio.stock_account.positions["510050.OF"].available_amount >= 17000: 
                if g.positions <=0.00001:
                    g.p = g.start_price #记录上一次交易的价格
                    g.p1 = g.p - g.x1 #下次买入价 
                    g.p2 = g.p + g.x2 #下次卖出价
                    continue
                order(g.stock, -17000)
                g.p=p  
                g.p1 = g.p - g.x1 
                g.p2 = g.p + g.x2
                g.positions -= 0.04
                log.info('时间：{}，执行卖出操作，价位：{}，数量：{}, 仓位数：{}'.format(date,p, "4%", g.positions))
                log.info("当前价：{}，下次买入价：{}，下次卖出价：{}".format(g.p, g.p1, g.p2))
                log.info(context.portfolio.stock_account)

        