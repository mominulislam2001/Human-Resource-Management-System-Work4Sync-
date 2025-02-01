import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
from app.models import get_dashboard_data,get_dashboard_data_2 # Assuming this function fetches data from your database





def create_dash_app(flask_app):
    
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dashapp/')

    avg_salary = 50000
    avg_performance_score = 75
    total_employees = 70

    dash_app.layout = html.Div(style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f4f4f4",
        "padding": "5px",
        "boxSizing": "border-box"
        
    }, children=[

        html.Div([
            
       
            html.Div([
                dcc.Dropdown(
                    id='department-dropdown',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'People & Organization', 'value': 'HR'},
                        {'label': 'Marketing', 'value': 'Marketing'},
                        {'label': 'Software Development', 'value': 'Software Development'},
                        {'label': 'Accounting', 'value': 'Accounting'},
                        {'label': 'Finance', 'value': 'Finance'},
                    
                    ],
                    value='All',  
                    clearable=False,
                    style={'width': '100%', 'marginBottom': '10px'}
                )
            ], style={'width': '30%', 'marginRight': '10px', 'display': 'inline-block'}) # Dropdown in a div

      
        ], style={'display': 'flex', 'justifyContent': 'center',  'alignItems': 'center'}),

      
        html.Div([
            html.Div([
                html.Div(id='avg-salary-card', className='card-value', style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#333'}),
                html.Div("Average Salary", className='card-label', style={'marginTop': '5px', 'fontSize': '12px', 'color': '#777'})
            ], className='card', style={
                'width': '20%', 'height': '40px', 'padding': '15px', 'textAlign': 'center', 'backgroundColor': '#fff', 
                'margin': '10px', 'borderRadius': '8px', 'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'
            }),

            html.Div([
                html.Div(id='total-employee-card', className='card-value', style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#333'}),
                html.Div("Total Employees", className='card-label', style={'marginTop': '5px', 'fontSize': '12px', 'color': '#777'})
            ], className='card', style={
                'width': '20%', 'height': '40px', 'padding': '15px', 'textAlign': 'center', 'backgroundColor': '#fff', 
                'margin': '10px', 'borderRadius': '8px', 'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'
            }),

            html.Div([
                html.Div(id='total-salary-employees', className='card-value', style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#333'}),
                html.Div("Total Monthly Salary of Employee", className='card-label', style={'marginTop': '5px', 'fontSize': '12px', 'color': '#777'})
            ], className='card', style={
                'width': '20%', 'height': '40px', 'padding': '15px', 'textAlign': 'center', 'backgroundColor': '#fff', 
                'margin': '10px', 'borderRadius': '8px', 'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'
            }),

          
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '20px'}),
        
         html.Div(style={'display': 'flex', 'justifyContent': 'space-around'}, children=[
            dcc.Graph(id='avg-salary-bar'),
            dcc.Graph(id='total-employees-bar'),
        ])

      
    ])


    @dash_app.callback(
        [Output('avg-salary-card', 'children'),
         Output('total-employee-card', 'children'),
         Output('total-salary-employees','children'),
         Output('avg-salary-bar', 'figure'),
         Output('total-employees-bar', 'figure'),
       ],
        [Input('department-dropdown', 'value')]
    )
    def update_price_cards(department):
     
        data = get_dashboard_data(department) 
        bardata = get_dashboard_data_2(department) 
        
    
        
        
        avg_salary_fig = go.Figure(
            data=[
                go.Bar(
                    x=bardata['Department'],
                    y=bardata['Average Salary'],
                    name='Average Salary',
                    marker=dict(color='#007bff')
                )
            ],
            layout=go.Layout(
                title='Average Salary by Department',
                xaxis={'title': 'Department'},
                yaxis={'title': 'Average Salary'},
                plot_bgcolor='#f4f4f4',
                paper_bgcolor='#f4f4f4',
                font=dict(color='#555'),
                margin=dict(l=60, r=20, t=50, b=40)
            )
        )

        total_employees_fig = go.Figure(
            data=[
                go.Bar(
                    x=bardata['Department'],
                    y=bardata['Total Employees'],
                    name='Total Employees',
                    marker=dict(color='#28a745')
                )
            ],
            layout=go.Layout(
                title='Total Employees by Department',
                xaxis={'title': 'Department'},
                yaxis={'title': 'Total Employees'},
                plot_bgcolor='#f4f4f4',
                paper_bgcolor='#f4f4f4',
                font=dict(color='#555'),
                margin=dict(l=60, r=20, t=50, b=40)
            )
        )
        
        average_salary = data['average_salary']
        total_employees = data['total_employees']
        total_salary_employees = data['total_salary_employees']
 
        average_salary_content = f"{average_salary:.2f} Tk"
        total_employees_content = total_employees
        total_salary_employees_content = f"{total_salary_employees:.2f} Tk"
     
            
        return average_salary_content, total_employees_content,total_salary_employees_content,avg_salary_fig,total_employees_fig

    return dash_app