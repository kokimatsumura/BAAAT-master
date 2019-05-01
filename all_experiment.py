'''
Created on 2019/04/24

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
from function import *
from experiment1 import *
from experiment2 import *
from experiment3 import *

six_list = ['n=6_normal.csv', 'n=6_modified-normal.csv', 'n=6_uniform.csv',
            'n=6_modified-uniform.csv', 'n=6_Gamma.csv', 'n=6_Beta.csv']

eight_list = ['n=8_normal.csv', 'n=8_modified-normal.csv', 'n=8_uniform.csv',
              'n=8_modified-uniform.csv', 'n=8_Gamma.csv', 'n=8_Beta.csv']

ten_list = ['n=10_normal.csv', 'n=10_modified-normal.csv', 'n=10_uniform.csv',
            'n=10_modified-uniform.csv', 'n=10_Gamma.csv', 'n=10_Beta.csv']

twelve_list = ['n=12_normal.csv', 'n=12_modified-normal.csv', 'n=12_uniform.csv',
               'n=12_modified-uniform.csv', 'n=12_Gamma.csv', 'n=12_Beta.csv']

fourteen_list = ['n=14_normal.csv', 'n=14_modified-normal.csv', 'n=14_uniform.csv',
                 'n=14_modified-uniform.csv', 'n=14_Gamma.csv', 'n=14_Beta.csv']

sixteen_list = ['n=16_normal.csv', 'n=16_modified-normal.csv', 'n=16_uniform.csv',
                'n=16_modified-uniform.csv', 'n=16_Gamma.csv', 'n=16_Beta.csv']

eighteen_list = ['n=18_normal.csv', 'n=18_modified-normal.csv', 'n=18_uniform.csv',
                 'n=18_modified-uniform.csv', 'n=18_Gamma.csv', 'n=18_Beta.csv']

twenty_list = ['n=20_normal.csv', 'n=20_modified-normal.csv', 'n=20_uniform.csv',
               'n=20_modified-uniform.csv', 'n=20_Gamma.csv', 'n=20_Beta.csv']

result_file_name1 = make_record_file('BAAAT-experiment1.xlsx')

create_result_file1(six_list, result_file_name1, k_para=1, p_tilde=0.3)
create_result_file1(eight_list, result_file_name1, k_para=1, p_tilde=0.3)
create_result_file1(ten_list, result_file_name1, k_para=1, p_tilde=0.3)
create_result_file1(twelve_list, result_file_name1, k_para=1, p_tilde=0.3)
create_result_file1(fourteen_list, result_file_name1, k_para=1, p_tilde=0.3)
create_result_file1(sixteen_list, result_file_name1, k_para=1, p_tilde=0.3)

result_file_name2 = make_record_file('BAAAT-experiment2.xlsx')

create_result_file2(six_list, result_file_name2, k_para_list=[2,3,4,5])
create_result_file2(eight_list, result_file_name2, k_para_list=[2,3,4,5])
create_result_file2(ten_list, result_file_name2, k_para_list=[2,3,4,5])
create_result_file2(twelve_list, result_file_name2, k_para_list=[2,3,4,5])
create_result_file2(fourteen_list, result_file_name2, k_para_list=[2,3,4,5])

result_file_name3 = make_record_file('BAAAT-experiment3.xlsx')

create_result_file3(six_list, result_file_name3, p_tilde_list=[0.1,0.5,0.7,0.9], k_para=1)
create_result_file3(eight_list, result_file_name3, p_tilde_list=[0.1,0.5,0.7,0.9], k_para=1)
create_result_file3(ten_list, result_file_name3, p_tilde_list=[0.1,0.5,0.7,0.9], k_para=1)
create_result_file3(twelve_list, result_file_name3, p_tilde_list=[0.1,0.5,0.7,0.9], k_para=1)
create_result_file3(fourteen_list, result_file_name3, p_tilde_list=[0.1,0.5,0.7,0.9], k_para=1)
create_result_file3(sixteen_list, result_file_name3, p_tilde_list=[0.1,0.5,0.7,0.9], k_para=1)
create_result_file3(eighteen_list, result_file_name4, p_tilde_list=[0.1,0.3,0.5,0.7,0.9], k_para=1)
create_result_file3(twenty_list, result_file_name5, p_tilde_list=[0.3,0.5,0.7,0.9], k_para=1)
