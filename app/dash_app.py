import dash
from dash import dcc, html
import plotly.graph_objs as go
from flask import Flask

def create_dash_app(flask_app):
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dashapp/')

    # Sample data for the dashboard (Dummy Data)
    avg_salary = 50000
    avg_performance_score = 75
    total_employees = 70

    # Dummy data for Total Employees by Department
    total_employees_df = {
        'department': ['HR', 'Engineering', 'Marketing', 'Sales'],
        'total': [10, 25, 15, 20]
    }

    # Dummy data for Average Salary by Department
    avg_salary_df = {
        'department': ['HR', 'Engineering', 'Marketing', 'Sales'],
        'avg_salary': [60000, 80000, 55000, 70000]
    }

    # Additional data for line plots
    average_salaries = [48000, 50000, 52000, 55000, 54000]
    performance_scores = [70, 75, 80, 85, 90]
    
    # Define x-axis for trends
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']

    # Define color shades based on #8b1df9
    colors = ['#8b1df9', '#a94cfa', '#c37bfb', '#d6a3fc']

    # Layout of the Dash app
    dash_app.layout = html.Div(style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f4f4f4",
        "padding": "20px",
        "boxSizing": "border-box"
    }, children=[
        
        # Container for metrics cards
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'flexWrap': 'wrap',
            'marginBottom': '20px'
        }, children=[
            
            # Average Salary Card
            html.Div(style={
                "width": "30%",
                "padding": "10px",
                "backgroundColor": "#ffffff",
                "borderRadius": "8px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "textAlign": "center"
            }, children=[
                html.Div(f"${avg_salary}", style={
                    "fontSize": "24px",
                    "fontWeight": "bold",
                    "color": "#333"
                }),
                html.Div("Average Salary", style={
                    "fontSize": "14px",
                    "color": "#777"
                })
            ]),

            # Average Employee Performance Score Card
            html.Div(style={
                "width": "30%",
                "padding": "10px",
                "backgroundColor": "#ffffff",
                "borderRadius": "8px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "textAlign": "center"
            }, children=[
                html.Div(f"{avg_performance_score}", style={
                    "fontSize": "24px",
                    "fontWeight": "bold",
                    "color": "#333"
                }),
                html.Div("Avg Employee Performance Score", style={
                    "fontSize": "14px",
                    "color": "#777"
                })
            ]),

            # Total Employees Card
            html.Div(style={
                "width": "30%",
                "padding": "10px",
                "backgroundColor": "#ffffff",
                "borderRadius": "8px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "textAlign": "center"
            }, children=[
                html.Div(f"{total_employees}", style={
                    "fontSize": "24px",
                    "fontWeight": "bold",
                    "color": "#333"
                }),
                html.Div("Total Employees", style={
                    "fontSize": "14px",
                    "color": "#777"
                })
            ]),
            
        ]),

        # Container for horizontal alignment of graphs
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-around',
            'flexWrap': 'wrap',
            'marginBottom': '20px'
        }, children=[
            
            # Total Employees by Department Bar Chart
            dcc.Graph(
                id='total-employees',
                figure={
                    'data': [
                        go.Bar(
                            x=total_employees_df['department'],
                            y=total_employees_df['total'],
                            name='Total Employees',
                            marker=dict(color=colors[0])  
                        )
                    ],
                    'layout': go.Layout(
                        title='Total Employees by Department',
                        titlefont=dict(size=16),
                        xaxis={'title': 'Department'},
                        yaxis={'title': 'Total Employees'},
                        plot_bgcolor='#f4f4f4',  
                        paper_bgcolor='#f4f4f4',  
                        font=dict(color='#555'),
                        margin=dict(l=60, r=20, t=50, b=40)
                    )
                },
                style={"width": "40%", "height": "250px"}
            ),

            # Average Salary by Department Bar Chart
            dcc.Graph(
                id='avg-salary',
                figure={
                    'data': [
                        go.Bar(
                            x=avg_salary_df['department'],
                            y=avg_salary_df['avg_salary'],
                            name='Average Salary',
                            marker=dict(color=colors[1])  
                        )
                    ],
                    'layout': go.Layout(
                        title='Average Salary by Department',
                        titlefont=dict(size=16),
                        xaxis={'title': 'Department'},
                        yaxis={'title': 'Average Salary'},
                        plot_bgcolor='#f4f4f4',  
                        paper_bgcolor='#f4f4f4',  
                        font=dict(color='#555'),
                        margin=dict(l=60, r=20, t=50, b=40)
                    )
                },
                style={"width": "40%", "height": "250px"}
            ),
            
        ]),

        # Line plots for trends in average salary and performance scores
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-around',
            'flexWrap': 'wrap'
        }, children=[
            
            # Average Salary Trend Line Plot
            dcc.Graph(
                id='avg-salary-trend',
                figure={
                    'data': [
                        go.Scatter(
                            x=months,
                            y=average_salaries,
                            mode='lines+markers',
                            name='Average Salary Trend',
                            line=dict(color='#007bff')
                        )
                    ],
                    'layout': go.Layout(
                        title='Average Salary Trend Over Months',
                        titlefont=dict(size=16),
                        xaxis={'title': 'Month'},
                        yaxis={'title': 'Average Salary'},
                        plot_bgcolor='#f4f4f4',  
                        paper_bgcolor='#f4f4f4',  
                        font=dict(color='#555'),
                        margin=dict(l=60, r=20, t=50, b=40)
                    )
                },
                style={"width": "40%", "height": "250px"}
            ),

            # Employee Performance Score Trend Line Plot
            dcc.Graph(
                id='performance-score-trend',
                figure={
                    'data': [
                        go.Scatter(
                            x=months,
                            y=performance_scores,
                            mode='lines+markers',
                            name='Performance Score Trend',
                            line=dict(color='#28a745')
                        )
                    ],
                    'layout': go.Layout(
                        title='Employee Performance Score Trend Over Months',
                        titlefont=dict(size=16),
                        xaxis={'title': 'Month'},
                        yaxis={'title': 'Performance Score'},
                        plot_bgcolor='#f4f4f4',  
                        paper_bgcolor='#f4f4f4',  
                        font=dict(color='#555'),
                        margin=dict(l=60, r=20, t=50, b=40)
                    )
                },
                style={"width": "40%", "height": "250px"}
            ),
            
        ]),

       
        
    ])

    return dash_app
