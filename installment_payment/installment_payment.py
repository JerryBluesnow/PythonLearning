# -*- coding: utf-8 -*-
<<<<<<< HEAD
=======

>>>>>>> ac3014a8a4f467669fd247ac4793405b9525b0fa
import math
 
# 定义函数
def installment_payment( monthly_interest_rate, payment_periods, repayment_month_index ):
    "计算中信银行新快现公式："
    "monthly_interest_rate - 官方月利率"
    "payment_periods       - 分期期数 3/6/9/12/15/24/36"
    "repayment_month_index - 第几个月提前还款"
   
    #分母  (1+2+3+...+n-1), n>=2,等差数列求和公式 ( (repayment_month_index * (repayment_month_index - 1)) / 2 )
<<<<<<< HEAD
    denominator = 2 * repayment_month_index * (payment_periods - repayment_month_index) + repayment_month_index * (repayment_month_index + 1)

    #分子 numerator： 
    numerator = 24 * (payment_periods * repayment_month_index * monthly_interest_rate + ((payment_periods - repayment_month_index) * 3 /(float)(100)) )
=======
    denominator = 25 * ((repayment_month_index * repayment_month_index) + (2 * payment_periods) - repayment_month_index)

    #分子 numerator： 
    numerator = 6 * ((100 * payment_periods * repayment_month_index * monthly_interest_rate) + (3 * (payment_periods - repayment_month_index)))
>>>>>>> ac3014a8a4f467669fd247ac4793405b9525b0fa

    yearly_interest_rate = numerator/(float)(denominator)

    print "++++++++++++++++++++++++++++++++++++++++++"
    print "中信新快现月利率(百分之...)：", monthly_interest_rate * 100, "%"
    print "分期期数：                  ", payment_periods
    print "第几个月提前还款：           ", repayment_month_index
    print "分期年化利率(百分之...)：    ", yearly_interest_rate * 100, "%"
    print "++++++++++++++++++++++++++++++++++++++++++"
    return
 
# 调用函数
for repayment_month_index in range(1, 36 + 1):
    installment_payment(0.76/100, 36, repayment_month_index)
<<<<<<< HEAD

sequence = [3, 6, 12, 18, 24, 36]
for index, payment_periods in enumerate(sequence):
    installment_payment(0.76/100, payment_periods, payment_periods)
=======
>>>>>>> ac3014a8a4f467669fd247ac4793405b9525b0fa
