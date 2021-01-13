import numpy as np
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt


def countrygraph(statelist):

	statedict = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia",
	"HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts",
	"MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico",
	"NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota",
	"TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
	#print(statedict['NJ'])


	finalstatelist=[]
	for state in statelist:
		if len(state)==2:
			if state.upper() in statedict.keys():
				state=statedict[state.upper()]
			else:
				return('Not a valid state')

		state=' '.join(x.capitalize() for x in state.split())

		if state not in ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho",
		"Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri",
		"Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon",
		"Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]:
			return('Not a valid state')

		finalstatelist.append(state)

	print(finalstatelist)
	

	#state1=finalstatelist[0]
	#state2=finalstatelist[1]
	dict_of_df = {}

	for i in range(len(finalstatelist)):
		print(finalstatelist[i])
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


	timedict=({i:j for (i,j) in list(zip(timeorder,indexorder))})
	timelist=(sorted(timedict.items(), key = lambda kv:(kv[0])))


	#print(timelist[0][1])


	fig, axs = plt.subplots(1,1, figsize=(15, 8),squeeze=False, constrained_layout=True)
	for i in range(len(timelist)):
		axs[0, 0].plot(dict_of_df[f'df_{timelist[i][1]}'].index, (dict_of_df[f'df_{timelist[i][1]}']['diff'])/7)

	timelable=[dict_of_df[f'df_{timelist[0][1]}'].index[i] for i in range(len(dict_of_df[f'df_{timelist[0][1]}'].index)) if i%25==0]
	
	

	start=dict_of_df[f'df_{timelist[0][1]}'].index.min()
	end=dict_of_df[f'df_{timelist[0][1]}'].index.max()

	a=([timelist[i][1] for i in range(len(timelist))])
	fig.legend([dict_of_df[f'df_{i}'].name for i in a])

	#print([i for i in indexorder])

	axs[0,0].set_xticks(timelable)
	axs[0,0].set_xticklabels(timelable)
	#orients date nicely
	fig.autofmt_xdate()

	axs[0,0].set_title('Corona Comparison')

	maxcase=(max([dict_of_df[f'df_{i}']['diff'].max()/7 for i in range(len(timelist))]))
	hline=[i for i in range(int(maxcase)) if i%1000==0]

	axs[0,0].hlines(hline,start,end,colors='#e2e2df',lw=.9)

	plt.show()





print(countrygraph(['NJ','Ga','Ny']))
