import dash, re
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd, numpy as np

df = pd.read_csv("../output/scored_songs.csv")
categories = ['political','romance','sexual','sad']

for cat in categories:
	#Normalize scores from scale of 0-1
	df[cat+'_score'] = (df[cat+'_score'] - df[cat+'_score'].min())/(df[cat+'_score'].max()-df[cat+'_score'].min())

artists = df['artist'].unique()

def create_line_chart(df):
	series_dict = {}
	data = []
	x = list(df.groupby(['year']).mean().index)
	for cat in categories:
		#Create y-axis output series for plotting
		series_dict[cat]=list(df.groupby(['year']).mean()[cat+'_score'])

		#Create inputs by series for dash viz
		data.append({'x':x,'y':series_dict[cat],'type':'line','name':cat + ' Score'})
	return data
	
app = dash.Dash()

app.layout = html.Div(children=[
		html.Div(children='''
			Enter Artist Name
			'''),
		dcc.Input(id='input', value='', type='text'),
		html.Div(id='output-graph')
	])
	
@app.callback(
	Output(component_id='output-graph',component_property='children'),
	[Input(component_id='input', component_property='value')]
	)
	
def update_graph(input_data):
	clean_input = re.sub('[^A-Za-z0-9]+', "", input_data.lower())
	if clean_input.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
		clean_input = clean_input[3:]
	print(clean_input)
	df_new = df[df['artist'] == clean_input]
	if len(df_new) == 0:
		df_new = df
	
	if input_data=='':
		input_data = 'All Artists'
	graph = dcc.Graph(id='results',
				figure={
					'data': create_line_chart(df_new),
					'layout': {
						'title':'Scores for ' + input_data
					}
				})
	return graph

if __name__ == '__main__':
	app.run_server(debug=True)
	pass

