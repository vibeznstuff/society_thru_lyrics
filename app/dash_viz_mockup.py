import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd, numpy as np

df = pd.read_csv("../output/scored_songs.csv")

x = list(df.groupby(['year']).mean().index)
categories = ['political','romance','sexual','sad']
series_dict = {}
data = []

for cat in categories:
	#Normalize scores from scale of 0-1
	df[cat+'_score'] = (df[cat+'_score'] - df[cat+'_score'].min())/(df[cat+'_score'].max()-df[cat+'_score'].min())
	
	#Create y-axis output series for plotting
	series_dict[cat]=list(df.groupby(['year']).mean()[cat+'_score'])
	
	#Create inputs by series for dash viz
	data.append({'x':x,'y':series_dict[cat],'type':'line','name':cat + ' Score'})

app = dash.Dash()

app.layout = html.Div(children=[
		html.H1('Dash Tutorial'),
		dcc.Graph(id='example',
				figure={
					'data': data,
					'layout': {
						'title':'Dash Mock Up - Lyrics Scores'
					}
				})
	])

if __name__ == '__main__':
	app.run_server(debug=True)
	pass

