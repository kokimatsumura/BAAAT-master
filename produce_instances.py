'''
Created on 2019/04/14

@author: matsumura
'''
import random
import csv
import function as fc

def make_coalition_size(n):
    
    binary_list = fc.make_binary_list(n)

    coalition_size = [binary_list[i].count(1) 
                        for i in range(len(binary_list))]
    return coalition_size

def produce_uniform(n, ins_num, prob_list, coalition_size):
    
    f=open('n=%d_uniform.csv' %n,'w')
    for i in range(ins_num):
        for i in range(pow(2,n)-1):
            f.write(str(random.uniform(0,coalition_size[i]))+',')
        for i in range(n):
            f.write(str(random.choice(prob_list))+',')
        f.write('\n')
    f.close()

def produce_normal(n, ins_num, prob_list, coalition_size):
    
    f=open('n=%d_normal.csv' %n,'w')
    for i in range(ins_num):
        for i in range(pow(2,n)-1):
            f.write(str(random.normalvariate(10*coalition_size[i],0.1))+',')
        for i in range(n):
            f.write(str(random.choice(prob_list))+',')
        f.write('\n')
    f.close()

def produce_modified_uniform(n, ins_num, prob_list, coalition_size):
    
    f=open('n=%d_modified_uniform.csv' %n,'w')
    for i in range(ins_num):
        for i in range(pow(2,n)-1):
            number = random.randint(1, 100)
            if number <= 20:
                modified = random.uniform(0, 50)
            else:
                modified = 0

            f.write(str(random.uniform(0,10*coalition_size[i])\
                                                + modified)+',')
        for i in range(n):
            f.write(str(random.choice(prob_list))+',')
        f.write('\n')
    f.close()

def produce_modified_normal(n, ins_num, prob_list, coalition_size):
    
    f=open('n=%d_modified_normal.csv' %n,'w')
    for i in range(ins_num):
        for i in range(pow(2,n)-1):
            number = random.randint(1, 100)
            if number <= 20:
                modified = random.uniform(0, 50)
            else:
                modified = 0

            f.write(str(random.normalvariate(10*coalition_size[i],0.01)\
                                                        + modified)+',')

        for i in range(n):
            f.write(str(random.choice(prob_list))+',')
        f.write('\n')
    f.close()

def produce_beta(n, ins_num, prob_list, coalition_size):
    
    f=open('n=%d_Beta.csv' %n,'w')
    for i in range(ins_num):
        for i in range(pow(2,n)-1):
            f.write(str(coalition_size[i] * random.betavariate(0.5,0.5))+',')
        for i in range(n):
            f.write(str(random.choice(prob_list))+',')
        f.write('\n')
    f.close()

def produce_gamma(n, ins_num, prob_list, coalition_size):
    
    f=open('n=%d_Gamma.csv' %n,'w')
    for i in range(ins_num):
        for i in range(pow(2,n)-1):
            f.write(str(coalition_size[i] * random.gammavariate(2.0,2.0))+',')
        for i in range(n):
            f.write(str(random.choice(prob_list))+',')
        f.write('\n')
    f.close()

def produce_all_files(n, ins_num, prob_list):

    coalition_size = make_coalition_size(n)

    produce_uniform(n, ins_num, prob_list, coalition_size)
    produce_normal(n, ins_num, prob_list, coalition_size)
    produce_modified_uniform(n, ins_num, prob_list, coalition_size)
    produce_modified_normal(n, ins_num, prob_list, coalition_size)
    produce_gamma(n, ins_num, prob_list, coalition_size)
    produce_beta(n, ins_num, prob_list, coalition_size)


n = 4
ins_num = 100
prob_list = [0.1,0.3,0.5,0.7,0.9]

produce_all_files(n, ins_num, prob_list)