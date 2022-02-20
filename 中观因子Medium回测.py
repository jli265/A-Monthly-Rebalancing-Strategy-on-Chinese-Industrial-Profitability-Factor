import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import datetime
import os
import numpy as np
import time
import matplotlib
from scipy.stats import ttest_1samp
from scipy import stats

# 在 PyCharm 里，中文正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号,避免负号显示成方框
plt.rcParams['axes.unicode_minus']=False
# 使图不要在程序运行时弹出来，避免plt.show()
plt.switch_backend('agg')
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------数据读取-------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#导入数据
WIND行业指数行情表 =  pd.read_excel('./WIND行业指数行情序列.xlsx')
print('WIND行业指数行情表\n'  , WIND行业指数行情表)
WIND行业利润总额累计值表 =  pd.read_excel('./WIND行业利润总额累计值.xlsx')
print('WIND行业利润总额累计值表\n'  , WIND行业利润总额累计值表)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------数据预处理与特征工程-----------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#计算每个月月底的中观月频景气度指标
中观月频景气度_列表 = [] #初始化保存中观月频景气度数据的列表
中观月频景气度由左小到右大排名的板块编号_列表 = [ ] # 初始化板块1-8（按论文顺序）的排名后板块编号（由左小到右大）
is_backtest = 0 #月底的日期是否在回测期内 1是 0不是
for i in range(len(WIND行业利润总额累计值表)):
    if str(WIND行业利润总额累计值表.loc[i,'指标名称'])[:10] == '2012-12-31':
        is_backtest = 1 #日期进入回测期
    if str(WIND行业利润总额累计值表.loc[i,'指标名称'])[:10] == '2021-07-31':
        is_backtest = 0 #日期超出回测期
    if is_backtest == 1 and str(WIND行业利润总额累计值表.loc[i,'指标名称'])[5:10] != '01-31': #回测期内有充足的数据构造景气度
       #计算中观月频景气度
       temp_list = [str(WIND行业利润总额累计值表.loc[i,'指标名称'])[:10]]
       temp_list.append( (WIND行业利润总额累计值表.loc[i,'采矿业:利润总额:累计值'] -  WIND行业利润总额累计值表.loc[i-12,'采矿业:利润总额:累计值']) / abs(WIND行业利润总额累计值表.loc[i,'采矿业:利润总额:累计值'] + WIND行业利润总额累计值表.loc[i-12,'采矿业:利润总额:累计值'])  )
       temp_list.append((WIND行业利润总额累计值表.loc[i, '化学原料及化学制品制造业:利润总额:累计值'] - WIND行业利润总额累计值表.loc[i - 12, '化学原料及化学制品制造业:利润总额:累计值']) / abs(
           WIND行业利润总额累计值表.loc[i, '化学原料及化学制品制造业:利润总额:累计值'] + WIND行业利润总额累计值表.loc[i - 12, '化学原料及化学制品制造业:利润总额:累计值']))
       temp_list.append((WIND行业利润总额累计值表.loc[i, '通用设备制造业:利润总额:累计值'] - WIND行业利润总额累计值表.loc[i - 12, '通用设备制造业:利润总额:累计值']) / abs(
           WIND行业利润总额累计值表.loc[i, '通用设备制造业:利润总额:累计值'] + WIND行业利润总额累计值表.loc[i - 12, '通用设备制造业:利润总额:累计值']))
       temp_list.append((WIND行业利润总额累计值表.loc[i, '纺织业:利润总额:累计值'] - WIND行业利润总额累计值表.loc[i - 12, '纺织业:利润总额:累计值']) / abs(
           WIND行业利润总额累计值表.loc[i, '纺织业:利润总额:累计值'] + WIND行业利润总额累计值表.loc[i - 12, '纺织业:利润总额:累计值']))
       temp_list.append((WIND行业利润总额累计值表.loc[i, '酒、饮料和精制茶制造业:利润总额:累计值'] - WIND行业利润总额累计值表.loc[i - 12, '酒、饮料和精制茶制造业:利润总额:累计值']) / abs(
           WIND行业利润总额累计值表.loc[i, '酒、饮料和精制茶制造业:利润总额:累计值'] + WIND行业利润总额累计值表.loc[i - 12, '酒、饮料和精制茶制造业:利润总额:累计值']))
       temp_list.append((WIND行业利润总额累计值表.loc[i, '医药制造业:利润总额:累计值'] - WIND行业利润总额累计值表.loc[i - 12, '医药制造业:利润总额:累计值']) / abs(
           WIND行业利润总额累计值表.loc[i, '医药制造业:利润总额:累计值'] + WIND行业利润总额累计值表.loc[i - 12, '医药制造业:利润总额:累计值']))
       temp_list.append( 0 )
       temp_list.append((WIND行业利润总额累计值表.loc[i, '计算机、通信和其他电子设备制造业:利润总额:累计值'] - WIND行业利润总额累计值表.loc[i - 12, '计算机、通信和其他电子设备制造业:利润总额:累计值']) / abs(
           WIND行业利润总额累计值表.loc[i, '计算机、通信和其他电子设备制造业:利润总额:累计值'] + WIND行业利润总额累计值表.loc[i - 12, '计算机、通信和其他电子设备制造业:利润总额:累计值']))
       print('当前月频景气度： ', temp_list)
       中观月频景气度_列表.append(temp_list[:])
中观月频景气度_列表[0][1] = 0 #将唯一一个异常缺失值填补为0
print('中观月频景气度_列表: ',中观月频景气度_列表)
# 排序中观月频景气度,使用由左小到右大的选择排序算法
月频日期列表, 月频日期列表_节选年月 = [], []
for i in range(len(中观月频景气度_列表)):
  月频日期列表.append(中观月频景气度_列表[i][0])
  月频日期列表_节选年月.append(中观月频景气度_列表[i][0][:7])
  temp_list2 = [[中观月频景气度_列表[i][j + 1], j + 1] for j in range(8)]
  j = 6
  while j >= 0:
    for k in range(j, 7):
        if temp_list2[k][0] > temp_list2[k + 1][0]:
            temp_list2[k], temp_list2[k + 1] = temp_list2[k + 1], temp_list2[k]
    j -= 1
  temp_list3 = [x[1] for x in temp_list2]
  中观月频景气度由左小到右大排名的板块编号_列表.append([中观月频景气度_列表[i][0], temp_list3[:]])
print('中观月频景气度由左小到右大排名的板块编号_列表: ',中观月频景气度由左小到右大排名的板块编号_列表)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------策略回测----------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------
中观月频景气度_top组_净值列表,  中观月频景气度_基准组_净值列表 ,  中观月频景气度_down组_净值列表  = [1], [1], [1] #初始化top、基准、down组净值列表
中观月频景气度_top组_投资组合指数列表, 中观月频景气度_down组_投资组合指数列表 = [], []  # 初始化top、down组的投资组合指数列表
全部期限_中观月频景气度_基准组_二维收益率列表 = []
Top组是否战胜市场_列表 = []
Top组超额收益率_列表 = []
is_backtest = 0 #日期是否在回测期内 1是 0不是
上次遍历到的年和月 = '2012-12' #初始化上次遍历到的年和月为2012年12月 日期格式： yyyy-mm
for i in range(len(WIND行业指数行情表)):
    当前遍历到的年和月 = str(WIND行业指数行情表.loc[i, '时间'])[:7]
    下次遍历到的年和月 = str(WIND行业指数行情表.loc[i+1, '时间'])[:7]
    if str(WIND行业指数行情表.loc[i,'时间'])[:10] == '2012-12-31':
        is_backtest = 1 #日期进入回测期, 准备开始回测...
        print('日期进入回测期, 准备开始回测...')
    if 当前遍历到的年和月  == '2021-07':
        is_backtest = 0 #日期超出回测期, 准备结束回测...
        print('日期超出回测期, 准备结束回测...')
        break
    if is_backtest == 1:
       # 开仓条件:当前遍历到新的一个月的第一个交易日 和 上一个月月底有月频景气度数据
       # 开仓条件之一:当前遍历到新的一个月的第一个交易日
       if 当前遍历到的年和月 != 上次遍历到的年和月:
          中观月频景气度_top组_投资组合指数列表, 中观月频景气度_down组_投资组合指数列表 = [], []  # 初始化top、down组的投资组合指数列表
          # 如果上一个月月底有月频景气度数据，找到该月的中观月频景气度由左小到右大排名的板块编号
          当前排名后板块编号列表 = None
          for x in 中观月频景气度由左小到右大排名的板块编号_列表:
              if x[0][:7] == 上次遍历到的年和月:
                  当前排名后板块编号列表 = x[1]
                  break
          print('当前排名后板块编号列表: ',当前排名后板块编号列表)
          # 开仓条件之二： 上一个月月底有月频景气度数据
          if 当前排名后板块编号列表:
             print('开仓成功！')
             for j in range(4,8):
                 中观月频景气度_top组_投资组合指数列表.append(WIND行业指数行情表.iloc[i, 当前排名后板块编号列表[j]])
             for j in range(4):
                 中观月频景气度_down组_投资组合指数列表.append(WIND行业指数行情表.iloc[i, 当前排名后板块编号列表[j]])
             print('中观月频景气度_top组_投资组合指数列表: ',中观月频景气度_top组_投资组合指数列表)
             print('中观月频景气度_down组_投资组合指数列表: ', 中观月频景气度_down组_投资组合指数列表)
       #平仓条件：有开仓 和 当月最后一个交易日临近收盘
       if len(中观月频景气度_top组_投资组合指数列表) > 0 and 下次遍历到的年和月 != 当前遍历到的年和月:
          中观月频景气度_top组_收益率列表 = [WIND行业指数行情表.iloc[i, 当前排名后板块编号列表[k+4]]/中观月频景气度_top组_投资组合指数列表[k] - 1 for k in range(4)]
          中观月频景气度_top组_平均收益率 = sum(中观月频景气度_top组_收益率列表) / 4
          中观月频景气度_top组_净值 = 中观月频景气度_top组_净值列表[-1]*(1+中观月频景气度_top组_平均收益率)
          中观月频景气度_top组_净值列表.append(中观月频景气度_top组_净值)
          print('中观月频景气度_top组_收益率列表: ',中观月频景气度_top组_收益率列表, '中观月频景气度_top组_平均收益率: ',中观月频景气度_top组_平均收益率)
          print('中观月频景气度_top组_净值列表: ', 中观月频景气度_top组_净值列表)

          中观月频景气度_down组_收益率列表 = [WIND行业指数行情表.iloc[i, 当前排名后板块编号列表[k]]/中观月频景气度_down组_投资组合指数列表[k] - 1 for k in range(4)]
          中观月频景气度_down组_平均收益率 = sum(中观月频景气度_down组_收益率列表) / 4
          中观月频景气度_down组_净值 = 中观月频景气度_down组_净值列表[-1]*(1+中观月频景气度_down组_平均收益率)
          中观月频景气度_down组_净值列表.append(中观月频景气度_down组_净值)
          print('中观月频景气度_down组_收益率列表: ',中观月频景气度_down组_收益率列表, '中观月频景气度_down组_平均收益率: ',中观月频景气度_down组_平均收益率)
          print('中观月频景气度_down组_净值列表: ', 中观月频景气度_down组_净值列表)

          中观月频景气度_down组_收益率列表.extend(中观月频景气度_top组_收益率列表)
          全部期限_中观月频景气度_基准组_二维收益率列表.append(中观月频景气度_down组_收益率列表[:])
          中观月频景气度_基准组_平均收益率 =  (中观月频景气度_top组_平均收益率+中观月频景气度_down组_平均收益率)/2
          中观月频景气度_基准组_净值 = 中观月频景气度_基准组_净值列表[-1]*(1+中观月频景气度_基准组_平均收益率)
          中观月频景气度_基准组_净值列表.append(中观月频景气度_基准组_净值)
          print('中观月频景气度_基准组_平均收益率: ',中观月频景气度_基准组_平均收益率)
          print('中观月频景气度_基准组_净值列表: ', 中观月频景气度_基准组_净值列表)
          print('全部期限_中观月频景气度_基准组_二维收益率列表: ', 全部期限_中观月频景气度_基准组_二维收益率列表)

          if 中观月频景气度_top组_平均收益率 > 中观月频景气度_基准组_平均收益率:
              Top组是否战胜市场_列表.append(1)
          Top组超额收益率_列表.append(中观月频景气度_top组_平均收益率-中观月频景气度_基准组_平均收益率)

          中观月频景气度_top组_投资组合指数列表, 中观月频景气度_down组_投资组合指数列表 = [], [] #标志已平仓
          print('平仓成功！')

    上次遍历到的年和月 = 当前遍历到的年和月
print('收益率回测成功！')
print('中观月频景气度_top组_净值列表: ', 中观月频景气度_top组_净值列表)
print('中观月频景气度_基准组_净值列表: ', 中观月频景气度_基准组_净值列表)
print('中观月频景气度_down组_净值列表: ', 中观月频景气度_down组_净值列表)
print('全部期限_中观月频景气度_基准组_二维收益率列表的长度： ', len(全部期限_中观月频景气度_基准组_二维收益率列表))
print('全部期限_中观月频景气度_列表的长度： ', len(中观月频景气度_列表))
print('月频日期列表的长度： ', len(月频日期列表))
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------回测结果深度分析--------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------
是否画净值曲线 = 1 # 1画 0不画
if 是否画净值曲线:
    fig = plt.figure(figsize=(16, 16))
    plt.plot(月频日期列表,  中观月频景气度_top组_净值列表 , color='orange', label='Top组合')
    plt.legend(loc='upper left', prop = {'size':20})
    plt.plot(月频日期列表,  中观月频景气度_基准组_净值列表 , color='silver', label='等权基准组合')
    plt.legend(loc='upper left', prop={'size': 20})
    plt.plot(月频日期列表,  中观月频景气度_down组_净值列表 , color='blue', label='Down组合')
    plt.legend(loc='upper left', prop={'size': 20})
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
    fig.autofmt_xdate()
    plt.tick_params(labelsize=20)   # 更改x,y轴刻度字体大小
    #plt.show()
    plt.savefig('./图2 净值曲线.png')
    plt.close()
    print('图2 净值曲线做好了！')
是否画IC曲线 = 1 # 1画 0不画
if 是否画IC曲线:
   IC列表 = []
   for i in range(len(全部期限_中观月频景气度_基准组_二维收益率列表)):
       单日_中观月频景气度_序列 = pd.Series(中观月频景气度_列表[i][1:])
       单日_中观月频景气度_基准组_收益率_序列 = pd.Series(全部期限_中观月频景气度_基准组_二维收益率列表[i])
       IC = round(单日_中观月频景气度_序列.corr(单日_中观月频景气度_基准组_收益率_序列), 4)
       IC列表.append(IC)
   print('\n以下是关于IC的一些回测统计指标： ↓ \n')
   print('IC列表: ',IC列表)
   print('Top组合战胜市场基准组合的频率: ', len(Top组是否战胜市场_列表)/len(IC列表) )
   print('IC均值: ',  np.mean(IC列表))
   print('IC期数: ',len(IC列表))
   print('ICIR(因子IR): ', np.mean(IC列表)/np.std(IC列表))
   print('ICIR(策略IR): ', np.mean(Top组超额收益率_列表) / np.std(Top组超额收益率_列表))
   t, p = ttest_1samp(IC列表, 0)
   print('IC的T值(判断是否显著不为0): ', t)

   #画IC曲线图
   fig = plt.figure(figsize=(16, 16))
   plt.plot(月频日期列表[1:], [sum(IC列表[:i+1]) for i in range(len(IC列表))], color='orange', label='多期IC累积值')
   plt.legend(loc='upper left', prop={'size': 20})
   ax = plt.gca()
   ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
   fig.autofmt_xdate()
   plt.tick_params(labelsize=20)  # 更改x,y轴刻度字体大小
   # plt.show()
   plt.savefig('./图3 多期IC累积值.png')
   plt.close()
   print('图3 多期IC累积值 制作完毕！')