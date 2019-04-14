'''
Created on 2019/04/13

@author: matsumura
'''
import copy
import functools
import operator
import csv
import timeit
import openpyxl as excel
import cplex
from cplex.exceptions import CplexError
import function as fc

def preliminary_experiment(file_path, n, k_para):
    time_pcsg = []
    value_pcsg = []
    with open(file_path,'r') as f:
        reader=csv.reader(f)
        for row in reader:
            row.pop(-1)
            my_obj = [float(i) for i in row[:-n]]
            my_prob = [float(i) for i in row[-n:]]

            #Start solving the PCSG problems.
            start_pcsg  = timeit.default_timer()

            optimal_value, k_values = fc.solve_pcsg(n, k_para,
                                                    my_prob, my_obj)

            stop_pcsg = timeit.default_timer()
            t_pcsg = stop_pcsg - start_pcsg

            time_pcsg.append(t_pcsg)
            value_pcsg.append(optimal_value)

    return time_pcsg, value_pcsg

def create_result_file_pre(file_path, result_file_name, k_para_list):

    n = int(''.join(c for c in file_path if c.isdigit()))

    wb = excel.Workbook()
    wb.create_sheet('result' ,0)
    ws = wb.active

    for i in range(len(k_para_list)):
        k_para = k_para_list[i]
        time_pcsg, value_pcsg = preliminary_experiment(file_path, n, k_para)

        #make a average runtime table
        ws.cell(column=k_para+1, row=2, value='k=%d' % k_para)
        ws.cell(column=1, row=n/2, value='n=%d' % n)
        ws.cell(column=k_para+1, row=n/2, value=sum(time_pcsg)/len(time_pcsg))
        ws.cell(column=7+k_para, row=1, value='n=%dk=%d' % (n, k_para))
        #plot runtime in a column
        for j in range(len(time_pcsg)):
            ws.cell(column=9+i, row=2+j, value=time_pcsg[j])

    wb.save(result_file_name)

    return


k_para_list = [2, 3, 4, 5]

six_list = ['n=6_normal.csv', 'n=6_modified_normal.csv', 'n=6_uniform.csv',
            'n=6_modified_uniform.csv', 'n=6_Gamma.csv', 'n=6_Beta.csv']
            
six_pre = ['n=6n_pre.xlsx', 'n=6mn_pre.xlsx', 'n=6u_pre.xlsx',
            'n=6mu_pre.xlsx', 'n=6g_pre.xlsx', 'n=6b_pre.xlsx']

eight_list = ['n=8_normal.csv', 'n=8_modified_normal.csv', 'n=8_uniform.csv',
                'n=8_modified_uniform.csv', 'n=8_Gamma.csv', 'n=8_Beta.csv']

eight_pre = ['n=8n_pre.xlsx', 'n=8mn_pre.xlsx', 'n=8u_pre.xlsx',
                'n=8mu_pre.xlsx', 'n=8g_pre.xlsx', 'n=8b_pre.xlsx']

ten_list = ['n=10_normal.csv', 'n=10_modified_normal.csv', 'n=10_uniform.csv',
            'n=10_modified_uniform.csv', 'n=10_Gamma.csv', 'n=10_Beta.csv']

ten_pre = ['n=10n_pre.xlsx', 'n=10mn_pre.xlsx', 'n=10u_pre.xlsx',
            'n=10mu_pre.xlsx', 'n=10g_pre.xlsx', 'n=10b_pre.xlsx']

twelve_list = [
    'n=12_normal.csv', 'n=12_modified_normal.csv', 'n=12_uniform.csv',
    'n=12_modified_uniform.csv', 'n=12_Gamma.csv', 'n=12_Beta.csv'
    ]

twelve_pre = ['n=12n_pre.xlsx', 'n=12mn_pre.xlsx', 'n=12u_pre.xlsx',
                'n=12mu_pre.xlsx', 'n=12g_pre.xlsx', 'n=12b_pre.xlsx']

fourteen_list = [
    'n=14_normal.csv', 'n=14_modified_normal.csv', 'n=14_uniform.csv',
    'n=14_modified_uniform.csv', 'n=14_Gamma.csv', 'n=14_Beta.csv']

fourteen_pre = ['n=14n_pre.xlsx', 'n=14mn_pre.xlsx', 'n=14u_pre.xlsx',
                'n=14mu_pre.xlsx', 'n=14g_pre.xlsx', 'n=14b_pre.xlsx']

for i in range(len(six_list)):
    create_result_file_pre(six_list[i], six_pre[i], k_para_list)

for i in range(len(eight_list)):
    create_result_file_pre(eight_list[i], eight_pre[i], k_para_list)

for i in range(len(ten_list)):
    create_result_file_pre(ten_list[i], ten_pre[i], k_para_list)

for i in range(len(twelve_list)):
    create_result_file_pre(twelve_list[i], twelve_pre[i], k_para_list)

for i in range(len(fourteen_list)):
    create_result_file_pre(fourteen_list[i], fourteen_pre[i], k_para_list)
