'''
Created on 2019/04/09

@author: matsumura
'''
import copy
import functools
import itertools
import operator
import csv
import openpyxl as excel
import cplex
from cplex.exceptions import CplexError

def make_record_file(result_file_name):

    wb = excel.Workbook()
    wb.save(result_file_name)

    return result_file_name

# get all the data to add as variables and objectives in cplex.
def get_data(n):

    my_ctype = "B" * (pow(2,n)-1)
    my_colnames = ["a{}".format(i) for i in range(pow(2,n)-1)]

    rows = []
    for i in range(n):
        bin = [0.0] * pow(2,i) + [1.0] * pow(2,i)
        constraint = bin * (pow(2,n-i-1))
        constraint.pop(0)
        rows.append([my_colnames, constraint])

    my_rownames = ["c{}".format(i) for i in range(n)]
    my_rhs = [1.0] * n
    my_sense = "E" * n

    return my_ctype, my_colnames, rows, my_rownames, my_rhs, my_sense

# make all the binary lists for n-agents
#    to represent the corresponding coalitions.
# n = 3
# >>> [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1],
#     [1, 0, 1], [0, 1, 1], [1, 1, 1]

def make_binary_list(n):

    number = list(itertools.product(range(0,2), repeat=n))
    number.pop(0)
    binary_list = [list(number[i])[::-1] for i in range(pow(2,n)-1)]

    return binary_list

# calcurate the expected value for the coalition.
# my_obj = [20, 50, 10, 70, 60, 100, 110]
# coalition = [0, 1, 1], my_prob = [0.9, 0.5, 0.3]
# >>> ve = 100 * 0.5 * 0.3

def calc_coalition_ve(k_prob, my_obj, coalition_list, binary_list):

    number = binary_list.index(coalition_list)
    ve = functools.reduce(operator.mul, k_prob) * my_obj[number]

    return ve

# calcurate the expected value considering k-agents might be absent.
def make_k_expected_value(n, k_para, my_prob,
                          coalition_list, binary_list, my_obj):

    k_prob_pre = [1 if coalition_list[i]==0
                    else my_prob[i] for i in range(n)]

    ve_sum = calc_coalition_ve(k_prob_pre,
                               my_obj, coalition_list, binary_list)

    structure = [coalition_list]
    count = coalition_list.count(1)
    while len(structure) != 0:
        k_prob = []
        new_coalition = structure.pop(0)
        for i in range(n):
            if coalition_list[i] == 0:
                k_prob.append(1)
            elif (coalition_list[i] == 1
                    and new_coalition[i] == 0):

                k_prob.append(1.0- my_prob[i])
            else:
                k_prob.append(my_prob[i])

        for i in range(n):
            if (new_coalition.count(1) <= count - k_para
                    or new_coalition.count(1) <= 1):
                break
            elif new_coalition[i] == 1:
                k_prob[i] = 1.0 - k_prob[i]
                new_coalition[i] = 0
                structure_pre = copy.deepcopy(new_coalition)

                if structure_pre not in  structure:
                    structure.append(structure_pre)

                    ve = calc_coalition_ve(
                        k_prob, my_obj,
                        new_coalition, binary_list)

                    ve_sum += ve
                    new_coalition[i] = 1
                    k_prob[i] = 1.0 - k_prob[i]
                else:
                    new_coalition[i] = 1
                    k_prob[i] = 1.0 - k_prob[i]

    return ve_sum

# make the objective function of PCSG.
def make_k_value_list(n, k_para, binary_list,
                      my_prob, my_obj):
    k_values = []
    for i in range(len(binary_list)):
        coalition_list = binary_list[i]

        value = make_k_expected_value(n, k_para, my_prob,
                        coalition_list, binary_list, my_obj)

        k_values.append(value)

    return k_values

# make the following three lists according to p_tilde.
def reduce_list(n, p_tilde, my_prob, rows):

    reduced_list = []
    remaining_prob = []
    reduced_prob = []
    for i in range(n):
        if my_prob[i] <= p_tilde:
            reduced_list.append(rows[i])
            reduced_prob.append((my_prob[i], i))
        else:
            remaining_prob.append(my_prob[i])

    return reduced_list, remaining_prob, reduced_prob

def sum_individual_values(reduced_prob, my_obj):

    individual_values = 0
    for i in range(len(reduced_prob)):
        indi_idx = reduced_prob[i][1]
        indi_value = reduced_prob[i][0] \
                    * my_obj[pow(2, indi_idx)-1]

        individual_values += indi_value

    return individual_values

def calc_error_bound(reduced_list, k_values):

    sigma_r=0
    individual_a=0
    for i in range(len(reduced_list)):
        rmax_list = [x*y for (x,y)
                    in zip(reduced_list[i], k_values)]

        for j in range(len(rmax_list)):
            if rmax_list[j] != 0:
                individual_a += rmax_list[j]
                break

        sigma_r += max(rmax_list)

    error_bound = sigma_r - individual_a

    return error_bound

# the following function is used in the BAAAT.
def reduce_objecticve_values(n, reduced_list, my_obj):

    if not reduced_list:
        return []
    else:
        all_reduce_list = [functools.reduce(operator.add, x)
                           for x in zip(*reduced_list)]

        reduced_obj = [my_obj[i] for i in range(pow(2,n)-1)
                                if all_reduce_list[i] == 0]
        return reduced_obj

def solve_pcsg(n, k_para, my_prob, my_obj):

    my_ctype, my_colnames, rows, my_rownames,\
                            my_rhs, my_sense = get_data(n)

    binary_list = make_binary_list(n)
    k_values = make_k_value_list(n, k_para,
                                 binary_list, my_prob, my_obj)

    # solve the problem
    problem = cplex.Cplex()
    problem.objective.set_sense(problem.objective.sense.maximize)
    problem.variables.add(obj=k_values, types=my_ctype,
                            names=my_colnames)

    problem.linear_constraints.add(lin_expr=rows, senses=my_sense,
                                   rhs=my_rhs, names=my_rownames)
    problem.solve()
    optimal_value = problem.solution.get_objective_value()
    print("Solution value  = ", optimal_value)

    return optimal_value, k_values

def solve_pcsg_by_baaat(n, k_para, p_tilde, my_prob, my_obj):

    rows_baaat = []
    for i in range(n):
        bin = [0.0] * pow(2,i) + [1.0] * pow(2,i)
        constraint = bin * (pow(2,n-i-1))
        constraint.pop(0)
        rows_baaat.append(constraint)

    reduced_list, remaining_prob, reduced_prob\
                            = reduce_list(n, p_tilde, my_prob, rows_baaat)
    reduced_obj = reduce_objecticve_values(n, reduced_list, my_obj)

    m = len(remaining_prob)

    my_ctype, my_colnames, rows, my_rownames,\
                            my_rhs, my_sense = get_data(m)

    indi_values = sum_individual_values(reduced_prob, my_obj)
    binary_list = make_binary_list(m)

    if reduced_prob:
        k_values = make_k_value_list(m, k_para, binary_list,
                                    remaining_prob, reduced_obj)
    else:
        k_values = make_k_value_list(m, k_para, binary_list,
                                    remaining_prob, my_obj)

    # solve the problem
    problem = cplex.Cplex()
    problem.objective.set_sense(problem.objective.sense.maximize)
    problem.variables.add(obj=k_values, types=my_ctype,
                            names=my_colnames)

    problem.linear_constraints.add(lin_expr=rows, senses=my_sense,
                                   rhs=my_rhs, names=my_rownames)
    problem.solve()
    optimal_value = problem.solution.get_objective_value() + indi_values
    print("Solution value  = ", optimal_value)

    return optimal_value, reduced_list
