""" Pyramid height by pyramid complex bar plot without timeline """

import pandas as pd
import numpy as np
from plotly import graph_objects as go

def average_of_two(val):
    """
    Get the height column to be interpreted as numeric by taking the average 
    of values containing two height estimates, or by using the projected 
    heights as opposed to actual heights, as directed by Christelle during 
    a meeting.

    Input: 
        val: String, int, or float representing a pyramid dimension value
    Output: 
        Numeric type (likely float, possibly int) representing the pyramid 
        dimension value
    """
    if isinstance(val, int) or isinstance(val, float) or pd.isna(val): 
        return val

    # Temporary: Deals with that one weird actual AND projected value
    if ',' in val: 
        return 72    

    nums = val.split('-')
    if len(nums) == 1: 
        return float(nums[0])
    
    return (float(nums[0]) + float(nums[1])) / 2

def prepare_dataframe(df):
    """
    Prepare a subset of the original dataframe to allow for the creation of 
    our desired plot.

    Input:
        df: Pandas dataframe containing the original normalized pyramid data
    Output:
        Pandas dataframe representing a subset of the original dataframe with 
        additional modifications to allow for proper plotting
    """

    # Fill in 'start_of_reign' for every row where it is NA with the year of the 
    # respective King's start of reign (ie max value of 'start_of_reign' for 
    # that complex).
    #
    # TODO (?): Add this functionality to the cleanup script
    temp = df
    complex_dict = df.groupby('pyramid_complex')['start_of_reign'].max().to_dict()
    temp['start_of_reign'] = df['pyramid_complex'].map(complex_dict)

    # This had to be done to get it in the correct order (value was missing)
    temp.loc[temp['pyramid_complex'] == 'Sneferu 3', 'start_of_reign'] = 2574

    # Information conflicts with this individual pyramid. It was requested to 
    # place this pyramid after Djedefre's, despite the rule dates currently in
    # the dataset. The same goes for the name change.
    temp.loc[temp['pyramid_owner'] == 'Nebka?', 'start_of_reign'] = 2527
    temp.loc[temp['pyramid_owner'] == 'Nebka?', 'dynasty'] = 4 
    temp.loc[temp['pyramid_owner'] == 'Nebka?', 'title'] = 'Pyramid of Zawyet el-Aryan'

    # Drop rows with no pyramid height value
    temp.dropna(subset='height', inplace=True)

    # Sort all remaining rows in chronological order
    temp.sort_values(by=['start_of_reign', 'royal_status'], ascending=[False, True], inplace=True)

    # Take the averages for elements with two height estimates
    temp['height'] = temp['height'].map(average_of_two).astype(float)

    # Create a new dataframe with a subset of data that is needed for the plot
    columns  = ['dynasty', 'pyramid_owner', 'start_of_reign', 'end_of_reign',
            'length_of_reign', 'height', 'royal_status', 'relationship_to_king',
            'title', 'pyramid_texts', 'state_of_completion']
    tl = temp[columns]

    return tl

def create_figure(tl):
    """
    Create a bar plot of the pyramid data with each pyramid grouped by 
    its respective complex on the x-axis, its height on the y-axis, the 
    royal status of the pyramid owner determining the color of the bar, the 
    state of completion determining the bar pattern shape, and the presence 
    of pyramid texts determining the bar outline color.

    Input:
        tl: The dataframe containing the pyramid data
    Output:
        A Plotly graph objects bar plot of the pyramid data
    """

    # Graph objects bar plot
    fig = go.Figure(go.Bar(
        x = [tl['dynasty'], tl['title']],
        y = tl["height"].values, 
        marker={"color": tl['royal_status'].map({'King': '#83B0E1', 
                                                 'Queen': '#FFBA78'}),
                "pattern_shape": tl['state_of_completion'].map({'Unfinished': 'x', 
                                                                'Unfinished?': 'x', 
                                                                'Completed': '', 
                                                                '': '', 
                                                                np.nan: ''}),
                # Alters border color + size of bars representing pyramids 
                # that contain pyramid texts.
                # Currently unused, may be wanted later.
                #"line_color": tl['pyramid_texts'].map({'Yes': 'black', 
                #                                    np.nan: 'white'}),
                #"line_width": tl['pyramid_texts'].map({'Yes': 2.5, 
                #                                       np.nan: 0.5})},
        },
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
    fig.add_trace(
        go.Bar(
        x=["Dummy"],
        y=[0],
        name="Queen",
        marker_color="#FFBA78",
        legendgroup='royal'))
    fig.add_trace(
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
    ''' Currently unused, but may be wanted later.
        Add a legend trace to represent 'Unfinished?' pyramids with 
        a pattern shape of '/'.
    fig.add_trace(
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
    '''
    fig.add_trace(
        go.Bar(
            x=[None],
            y=[None],
            name='Pyramid Texts',
            legendgroup='texts',
            marker_color='white',
            marker_line_color='white',
            marker_line_width=2.5
        )
    )

    # Ensure that the king legend trace doesn't have a pattern shape
    fig.update_traces(marker=dict(pattern_shape=''),
                    selector=dict(name="King"))

    # Final plot adjustments
    fig.update_layout(
        title = "Height of Pyramids By Complex",
        xaxis = dict(title = "Pyramid Owner (Grouped By Dynasty)", 
                    dividercolor='#e8e8e8'),
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
    
    return fig

def main():
    # Import the pyramid dataset
    df = pd.DataFrame(pd.read_csv("assets/normalized_pyramid_data.csv"))

    # Prepare the dataframe for plotting
    pyramids_and_owners = prepare_dataframe(df)

    # Create the plot
    fig = create_figure(pyramids_and_owners)

    # Output plot as a png image
    fig.write_image('images/jose-total-complex-height-by-status-bar.png')

if __name__ == "__main__":
    main()