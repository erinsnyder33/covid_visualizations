import numpy as np
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.patches as mpatches
import matplotlib.lines as mlines


def countrygraph():

    allcolors=['r','#ff8900','#ffe600','g']


    colordict={"Alabama":24.5,"Alaska":29,"Arizona":28.4,"Arkansas":22,"California":32.6,"Colorado":39.4,"Connecticut":38.4,"Delaware":31,"Florida":28.5,"Georgia":29.9,
    "Hawaii":32,"Idaho":26.8,"Illinois":33.4,"Indiana":25.3,"Iowa":27.7,"Kansas":32.2,"Kentucky":23.2,"Louisiana":23.4,"Maine":30.3,"Maryland":39,"Massachusetts":42.1,
    "Michigan":28.1,"Minnesota":34.8,"Mississippi":21.3,"Missouri":28.2,"Montana":30.7,"Nebraska":30.6,"Nevada":23.7,"New Hampshire":36,"New Jersey":38.1,"New Mexico":26.9,
    "New York":35.3,"North Carolina":29.9,"North Dakota":28.9,"Ohio":27.2,"Oklahoma":24.8,"Oregon":32.3,"Pennsylvania":30.1,"Rhode Island":33.0,"South Carolina":27.0,"South Dakota":27.8,
    "Tennessee":26.1,"Texas":28.7,"Utah":32.5,"Vermont":36.8,"Virginia":37.6,"Washington":34.5,"West Virginia":19.9,"Wisconsin":29,"Wyoming":26.7}


   
    
    finalstatelist=["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho",
    "Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri",
    "Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon",
    "Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    

    dict_of_df = {}

    for i in range(len(finalstatelist)):
        dict_of_df["df_{}".format(i)]=(pd.read_csv(open('us-counties.csv'),delimiter = ",", skiprows=0))

    timeorder=[]
    indexorder=[]
    for i in range(len(dict_of_df)):
        #dict_of_df[df]=((dict_of_df[df][dict_of_df[df]['state']==finalstatelist[i]]))
        dict_of_df[f'df_{i}']=((dict_of_df[f'df_{i}'][dict_of_df[f'df_{i}']['state']==finalstatelist[i]]))
        dict_of_df[f'df_{i}']=dict_of_df[f'df_{i}'][dict_of_df[f'df_{i}']['state']==finalstatelist[i]]
        dict_of_df[f'df_{i}']=(dict_of_df[f'df_{i}'].groupby('date').sum())
        dict_of_df[f'df_{i}']=dict_of_df[f'df_{i}'].drop(['fips','deaths'], axis=1)
        dict_of_df[f'df_{i}']['diff']=dict_of_df[f'df_{i}']['cases'].diff(periods=7)
        dict_of_df[f'df_{i}']=dict_of_df[f'df_{i}'].drop('cases', axis=1)

        dict_of_df[f'df_{i}'].name=finalstatelist[i]

        timeorder.append(dict_of_df[f'df_{i}'].index[0])
        indexorder.append(i)


    timedict=({i:j for (i,j) in list(zip(indexorder,timeorder))})   

    timelist=(sorted(timedict.items(), key = lambda kv:(kv[1])))

    #print(timelist[0][1])

    
    start=dict_of_df[f'df_{timelist[0][0]}'].index.min()
    end=dict_of_df[f'df_{timelist[0][0]}'].index.max()


    
    a=([timelist[i][0] for i in range(len(timelist))])
    #fig.legend([dict_of_df[f'df_{i}'].name for i in a])

    
    colorlist=[]
    statelist=[]
    for state in [dict_of_df[f'df_{i}'].name for i in a]:
        statelist.append(state)
        if colordict[state]<=25:
            colorlist.append(allcolors[0])
        elif colordict[state]<=30:
            colorlist.append(allcolors[1])
        elif colordict[state]<=35:
            colorlist.append(allcolors[2])
        else:
            colorlist.append(allcolors[3])
        
    fig, axs = plt.subplots(1,1, figsize=(15, 8),squeeze=False)
    for i in range(len(timelist)):
        axs[0, 0].plot(dict_of_df[f'df_{timelist[i][0]}'].index, (dict_of_df[f'df_{timelist[i][0]}']['diff'])/7, lw=.6, c=colorlist[i], label=statelist[i])

    timelable=[dict_of_df[f'df_{timelist[0][0]}'].index[i] for i in range(len(dict_of_df[f'df_{timelist[0][0]}'].index)) if i%25==0]
    
    

    axs[0,0].set_xticks(timelable)
    axs[0,0].set_xticklabels(timelable)
    #orients date nicely
    fig.autofmt_xdate()

    axs[0,0].set_title('Percent of College Educated Citizens vs Daily Corona Cases')

    maxcase=(max([dict_of_df[f'df_{i}']['diff'].max()/7 for i in range(len(timelist))]))
    hline=[i for i in range(int(maxcase)) if i%1000==0]

    axs[0,0].hlines(hline,start,end,colors='#e2e2df',lw=.9)


    mplcursors.cursor(hover=True)
    mplcursors.cursor().connect(
        "add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))


    red = mlines.Line2D([], [], color=allcolors[0], marker='o', markersize=15, label='20-25%') #baseline filename
    orange = mlines.Line2D([], [], color=allcolors[1], marker='o', markersize=15, label='25-30%')
    yellow = mlines.Line2D([], [], color=allcolors[2], marker='o', markersize=15, label='30-35%')
    green = mlines.Line2D([], [], color=allcolors[3], marker='o', markersize=15, label='35%+')

    fig.legend(loc='lower center',handles=[red, orange, yellow, green],mode='expand', ncol=4)


    plt.show()
    


countrygraph()
