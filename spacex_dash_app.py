#!/usr/bin/env python3

# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("data/spacex_launch_dash.csv")

# Get min and max payload for the range slider
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Create a dash application
app = dash.Dash(__name__)

# Application layout
app.layout = html.Div(children=[
	html.H1('SpaceX Launch Records Dashboard',
			style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
	
	# TASK 1: Dropdown
	dcc.Dropdown(
		id='site-dropdown',
		options=[
			{'label': 'All Sites', 'value': 'ALL'},
			*[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
		],
		value='ALL',
		placeholder="Select a Launch Site here",
		searchable=True
	),
	html.Br(),
	
	# TASK 2: Pie Chart
	html.Div(dcc.Graph(id='success-pie-chart')),
	html.Br(),
	
	html.P("Payload range (Kg):"),
	
	# TASK 3: Range Slider
	dcc.RangeSlider(
		id='payload-slider',
		min=0, max=10000, step=1000,
		marks={i: str(i) for i in range(0, 10001, 2500)},
		value=[min_payload, max_payload]
	),
	
	# TASK 4: Scatter Plot
	html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Pie chart callback
@app.callback(
	Output('success-pie-chart', 'figure'),
	Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
	if selected_site == 'ALL':
		fig = px.pie(spacex_df, names='Launch Site', values='class',
					title='Total Success Launches by Site')
	else:
		filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
		fig = px.pie(filtered_df, names='class',
					title=f'Success vs. Failure for site {selected_site}')
	return fig

# TASK 4: Scatter plot callback
@app.callback(
	Output('success-payload-scatter-chart', 'figure'),
	[Input('site-dropdown', 'value'),
	Input('payload-slider', 'value')]
)
def update_scatter_plot(selected_site, payload_range):
	low, high = payload_range
	df = spacex_df[
		(spacex_df['Payload Mass (kg)'] >= low) &
		(spacex_df['Payload Mass (kg)'] <= high)
	]
	if selected_site != 'ALL':
		df = df[df['Launch Site'] == selected_site]
		
	fig = px.scatter(
		df, x='Payload Mass (kg)', y='class',
		color='Booster Version Category',
		title='Correlation between Payload and Success'
	)
	return fig

# Run the app
if __name__ == '__main__':
	app.run(debug=True)
	
	