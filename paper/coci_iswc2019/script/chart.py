import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import colors as mcolors
import os
from datetime import datetime
import bisect
import re
import numpy as np
import operator

#CONSTANTS
COLORS = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)


# data:  {'[[ENTITY]]':{'x':[[ARR_OF_VALS]], 'y':[[ARR_OF_VALS]] }}
#OPTIONAL# opt: {'color': [[HEX_VAL]], 'width': [[NUMBER]]}
#OPTIONAL# logit: False, True
def plotLines(data,opt = {}, logit= False):

    for d in data:

        #def color
        my_color = None
        if 'color' in opt:
            if d in opt['color']:
                my_color = opt['color'][d]

        #def width
        my_width = None
        if 'width' in opt:
            if d in opt['width']:
                my_width = opt['width'][d]

        plt.plot(data[d]['x'],data[d]['y'], label=d, color=my_color, linewidth=my_width)
        if logit:
            plt.yscale('log')
        plt.xticks(data[d]['x'],[item.strftime('%Y-%m') for item in data[d]['x']])

    return plt


# data:  {'[[ENTITY]]':{'x':[[ARR_OF_VALS]], 'y':[[ARR_OF_VALS]] }}
#OPTIONAL# opt: {'color': [[HEX_VAL]], 'multi': [[False, True]], 'width': [[NUMBER]]}
#OPTIONAL# logit: False, True
def plotBars(data,opt = {}, sortit= False, logit= False):

    x_groups = {}
    bars_legend = []

    for d_bar in data:
            bars_legend.append(d_bar)
            d = data[d_bar]

            #the x axis
            for index_x in range(0,len(d['x'])):
                x_val = d['x'][index_x]
                if x_val not in x_groups:
                    x_groups[x_val] = []

                x_groups[x_val].append(d['y'][index_x])

    print(x_groups)
    #sort x_groups
    sorted_x_groups = {}
    if sortit:
        x_groups = sorted(x_groups.items(), key=operator.itemgetter(0))
        for elem in x_groups:
            sorted_x_groups[elem[0]] = elem[1]
    else:
        sorted_x_groups = x_groups


    ind = np.arange(len(sorted_x_groups))    # the x locations for the groups
    width = 0.3     # the width of the bars: can also be len(x) sequence
    if 'width' in opt:
        width = opt['width']
    fig, ax = plt.subplots()


    #for each x tick set all the bars
    loop_width = width/len(bars_legend)
    starting_from = ind - loop_width
    for bl_index in range(0,len(bars_legend)):

        y_vals = []
        for g in sorted_x_groups:
            y_vals.append(sorted_x_groups[g][bl_index])

        my_color = None
        if 'color' in opt:
            if bars_legend[bl_index] in opt['color']:
                my_color = opt['color'][bars_legend[bl_index]]

        xticks_fontsize = 10
        if 'xticks_fontsize' in opt:
            xticks_fontsize = opt['xticks_fontsize']

        yticks_fontsize = 10
        if 'yticks_fontsize' in opt:
            yticks_fontsize = opt['yticks_fontsize']

        ylabel_fontsize = 10
        if 'ylabel_fontsize' in opt:
            ylabel_fontsize = opt['ylabel_fontsize']

        xlabel_fontsize = 10
        if 'xlabel_fontsize' in opt:
            xlabel_fontsize = opt['xlabel_fontsize']

        rects1 = ax.bar(starting_from, tuple(y_vals), width, color=my_color, label= bars_legend[bl_index])
        if 'bar_val' in opt:
            for rect in rects1:
                height = rect.get_height()

                coef = 1
                if 'bar_coi' in opt:
                    coef = opt['bar_coi']

                round_val = 1
                if 'bar_round' in opt:
                    round_val = opt['bar_round']

                suf = ''
                if 'bar_suf' in opt:
                    suf = opt['bar_suf']

                pre = ''
                if 'bar_pre' in opt:
                    pre = opt['bar_pre']

                rotation = 0
                if 'bar_rotation' in opt:
                    rotation = opt['bar_rotation']

                custom_height = 0
                if 'bar_custom_h' in opt:
                    custom_height = opt['bar_custom_h']

                val = height/coef
                if val > 1:
                    #round_val = int(round_val)
                    val = round(val,round_val)
                    suf = 'M'
                else:
                    val = val * 1000
                    val = round(val,round_val)
                    suf = 'K'

                val_on_top = '%s%s%s' % (pre,str(val),suf)

                size_of_space = len(val_on_top) // 2
                str_space = ""
                for val in range(0,size_of_space):
                    str_space = str_space + " "

                after_space = ""
                before_space = str_space
                if bl_index % 2 == 0:
                    after_space = str_space
                    before_space = ""

                val_on_top = before_space+val_on_top+after_space

                plt.text(rect.get_x() + rect.get_width()/2.0, height - custom_height, val_on_top , rotation= rotation, fontsize=yticks_fontsize, ha='center', va='bottom')

        if 'multi' in opt:
            if opt['multi'] == True:
                if ((bl_index & 1) == 1):
                        starting_from = starting_from + 2*loop_width
        else:
            starting_from = starting_from + 2*loop_width



    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xticks(ind)
    #x_groups = [item.strftime('%Y-%m') for item in x_groups]
    ax.set_xticklabels(tuple(sorted_x_groups.keys()))
    ax.legend()

    if logit:
        plt.yscale('log')

    if 'ylabel' in opt:
        plt.ylabel(opt['ylabel'],{'fontsize': ylabel_fontsize})

    if 'xlabel' in opt:
        plt.xlabel(opt['xlabel'],{'fontsize': xlabel_fontsize})

    ax.tick_params(axis = 'x', which = 'major', labelsize = xticks_fontsize)
    ax.tick_params(axis = 'y', which = 'major', labelsize = yticks_fontsize)

    plt.rcParams['figure.figsize'] = (14,8)


    return plt


#Run a demo
def demo_ex():
    ex_data = {
         'A': {'x': ['1','2','3','4'], 'y': [10,20,30,40] },
         'B': {'x': ['1','2','3','4'], 'y': [15,25,35,45] }
    }
    ex_opt = {
         'multi': True
    }

    my_plt = plotBars(ex_data)
    my_plt.legend(loc='upper left', shadow=True, fontsize='large', title='Ex Chart')
    my_plt.ylabel('y-val')
    my_plt.xlabel('x-val')
    my_plt.rcParams['figure.figsize'] = (14,8)
    return my_plt

#REAL TIME PROBLEM DEMO
def real_demo():
    GROUP1 = 'references'
    GROUP2 = 'citations'
    GROUP3 = 'citation'
    GROUP4 = 'metadata'
    analysis2data = {GROUP1:{'x':[],'y':[]}, GROUP2:{'x':[],'y':[]}, GROUP3:{'x':[],'y':[]}, GROUP4:{'x':[],'y':[]}}
    ready_csv_path = '../data/restapi.csv'

    ########################
    #Process from csv
    ########################
    with open(ready_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            analysis2data[row['key']]['x'].append(row['date'])
            analysis2data[row['key']]['y'].append(int(row['accesses']))

    #Now plot the data
    allplotdata = analysis2data;
    if 'value' in allplotdata[GROUP1]:
        allplotdata[GROUP1].pop('value')
    if 'value' in allplotdata[GROUP2]:
        allplotdata[GROUP2].pop('value')
    if 'value' in allplotdata[GROUP3]:
        allplotdata[GROUP3].pop('value')
    if 'value' in allplotdata[GROUP4]:
        allplotdata[GROUP4].pop('value')

    #allplotdata.pop(GROUP1);
    #Call the chart builder and draw it
    my_plt = plotBars(allplotdata,opt = {'width':0.25,'xticks_fontsize':13, 'bar_rotation': 10 , 'bar_custom_h': 20, 'bar_round': 2,'ylabel_fontsize':14,'yticks_fontsize':11,'ylabel': 'Number of accesses', 'bar_val':True,'bar_coi':1000000,'bar_suf':'M','bar_pre':''}, sortit= False, logit= True)
    my_plt.legend(loc='upper left', shadow=True, fontsize='x-large')
    return my_plt

real_demo().show()
