import numpy as np
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import mplcursors


def countrygraph():



	colordict={"Alabama":"r","Alaska":"r","Arizona":"r","Arkansas":"r","California":"b","Colorado":"b","Connecticut":"b","Delaware":"b","Florida":"r","Georgia":"r",
	"Hawaii":"b","Idaho":"r","Illinois":"b","Indiana":"r","Iowa":"r","Kansas":"r","Kentucky":"r","Louisiana":"r","Maine":"b","Maryland":"b","Massachusetts":"b",
	"Michigan":"r","Minnesota":"b","Mississippi":"r","Missouri":"r","Montana":"r","Nebraska":"r","Nevada":"b","New Hampshire":"b","New Jersey":"b","New Mexico":"b",
	"New York":"b","North Carolina":"r","North Dakota":"r","Ohio":"r","Oklahoma":"r","Oregon":"b","Pennsylvania":"r","Rhode Island":"b","South Carolina":"r","South Dakota":"r",
	"Tennessee":"r","Texas":"r","Utah":"r","Vermont":"b","Virginia":"b","Washington":"b","West Virginia":"r","Wisconsin":"r","Wyoming":"r"}


	
	
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
		colorlist.append(colordict[state])
		statelist.append(state)

	fig, axs = plt.subplots(1,1, figsize=(15, 8),squeeze=False)
	for i in range(len(timelist)):
		axs[0, 0].plot(dict_of_df[f'df_{timelist[i][0]}'].index, (dict_of_df[f'df_{timelist[i][0]}']['diff'])/7, lw=.6, c=colorlist[i], label=statelist[i])

	timelable=[dict_of_df[f'df_{timelist[0][0]}'].index[i] for i in range(len(dict_of_df[f'df_{timelist[0][0]}'].index)) if i%25==0]
	
	

	axs[0,0].set_xticks(timelable)
	axs[0,0].set_xticklabels(timelable)
	#orients date nicely
	fig.autofmt_xdate()

	axs[0,0].set_title('Corona Comparison')

	maxcase=(max([dict_of_df[f'df_{i}']['diff'].max()/7 for i in range(len(timelist))]))
	hline=[i for i in range(int(maxcase)) if i%1000==0]

	axs[0,0].hlines(hline,start,end,colors='#e2e2df',lw=.9)


	mplcursors.cursor(hover=True)
	mplcursors.cursor().connect(
    	"add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))


	plt.show()
	





countrygraph()
