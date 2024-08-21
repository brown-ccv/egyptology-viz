# Pyramid height by pyramid complex histogram without timeline

import pandas as pd
import numpy as np
from plotly import graph_objects as go

'''
    Dataframe creation/manipulation
'''

# Import the pyramid dataset
df = pd.DataFrame(pd.read_csv("assets/normalized_pyramid_data.csv"))

# Drop pyramids with no known complex
key = ['unknown', 'pyramid?']
complexes = df[~df['pyramid_complex'].isin(key)]

# Fill in 'start_of_reign' for every row where it is NA with the year of the respective King's start of reign
# TODO: Add this functionality to the cleanup script
unique_comp = complexes['pyramid_complex'].unique()
temp = df

for comp in unique_comp:
    start = temp[temp['pyramid_complex'] == comp]['start_of_reign'].max()
    temp[temp['pyramid_complex'] == comp]['start_of_reign'] = temp[temp['pyramid_complex'] == comp]['start_of_reign'].replace(np.nan, start)

temp.loc[temp['pyramid_complex'] == 'Sneferu 3', 'start_of_reign'] = 2574   # This had to be done to get it in the correct order (value was missing)

# Drop rows with no pyramid height value
temp.dropna(subset='height', inplace=True)
# Sort all remaining rows in chronological order
temp.sort_values(by='start_of_reign', ascending=False, inplace=True)

''' 
Get the height column to be interpreted as numeric by taking the average of 
values containing two height estimates, or by using the projected heights 
as opposed to actual heights, as directed by Christelle during a meeting.

Input: String, int, or float representing a pyramid dimension value
Output: Numeric type (likely float, possibly int) representing the pyramid dimension value
'''
def average_of_two(val):
    if isinstance(val, int) or isinstance(val, float) or pd.isna(val): return val

    if ',' in val: return 72    # Temporary: Deals with that one weird value

    nums = val.split('-')
    if len(nums) == 1: return float(nums[0])
    return (float(nums[0]) + float(nums[1])) / 2
temp['height'] = temp['height'].map(average_of_two).astype(float)

# Create a new dataframe with a subset of data that is needed for the plot
tl = temp[['pyramid_complex', 'pyramid_owner', 'start_of_reign', 'end_of_reign',
           'length_of_reign', 'height', 'royal_status', 'relationship_to_king',
           'title', 'pyramid_texts', 'state_of_completion']]
# Omit Khentkaus I (Queen, not at a King's complex)
tl = tl.drop(tl[tl['pyramid_complex'] == 'Khentkaus I'].index)

''' 
    Plotly portion
'''

# Create list of colors for the bars to indicate royal status
def setColor(y):
    if y == "King": return '#636EFA'     # default plotly blue
    elif y == "Queen": return '#EF553B'  # default plotly red
colors = [setColor(y) for y in tl['royal_status'].values]

# Graph objects histogram
horizontal = go.Figure(go.Bar(
    x = tl.loc[:,["pyramid_complex", "title"]].T.values, 
    y = tl["height"].values, 
    marker={"color": colors,
            "pattern_shape": tl['state_of_completion'].map({'Unfinished': 'x', 
                                                            'Unfinished?': '/', 
                                                            'Completed': '', '': '', np.nan: ''}),
            "line_color": tl['pyramid_texts'].map({'Yes': 'black', np.nan: 'white'}),
            "line_width": tl['pyramid_texts'].map({'Yes': 2.5, np.nan: 0.5})},
    name = "King",
    legendgroup='royal',
    customdata = np.stack((tl['pyramid_owner'], 
                           tl['relationship_to_king'].fillna('Self'), 
                           tl['pyramid_texts'].fillna('No'),
                           tl['state_of_completion'].fillna('Completed')), 
                           axis=-1),
    hovertemplate='<br>'.join([
        'Pyramid Complex: %{x[0]}',
        'State of Completion: %{customdata[3]}',
        'Height: %{y} m',
        'Pyramid Owner: %{customdata[0]}',
        'Relationship To King: %{customdata[1]}',
        'Pyramid Texts?: %{customdata[2]}'
        '<extra></extra>'
    ])))

# Create dummy traces for the legend because plotly wouldn't do it automatically
horizontal.add_trace(
    go.Bar(
    x=["Dummy"],
    y=[0],
    name="Queen",
    legendgroup='royal'))
horizontal.add_trace(
    go.Bar(
        x=[None],
        y=[None],
        name='Unfinished',
        legendgroup='completion',
        marker_color = 'white',
        marker_pattern_shape = 'x',
        marker_line_width = 0
    )
)
horizontal.add_trace(
    go.Bar(
        x=[None],
        y=[None],
        name='Unfinished?',
        legendgroup='completion',
        marker_color = 'white',
        marker_pattern_shape = '/',
        marker_line_width = 0
    )
)
horizontal.add_trace(
    go.Bar(
        x=[None],
        y=[None],
        name='Pyramid Texts',
        legendgroup='texts',
        marker_color='white',
        marker_line_color='black',
        marker_line_width=2.5
    )
)

# Final plot adjustments
horizontal.update_layout(
    title = "Height of Pyramids By Complex",
    xaxis = dict(title = "Pyramid Owner (Grouped By Complex)", dividercolor='#e8e8e8'),
    yaxis = dict(
        title = "Height (meters)", 
        dtick = 10),
    showlegend = True,
    width = 1200,
    height = 800,
    bargap = 0.15,
    bargroupgap = 0,
    legend = dict(
        yanchor = "top",
        y = 1.2,
        xanchor = "left",
        x = 0.4,
        orientation='h'
    ))

# Output plot as a png image
horizontal.write_image('images/jose-total-complex-height-by-status-bar.png')