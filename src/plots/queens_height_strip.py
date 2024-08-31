""" Queen pyramid height with attributes scatterplot """

import pandas as pd
import plotly.express as px

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

    # Fill in 'start_of_reign' for every row where it is NA with the year of 
    # the respective King's start of reign (ie max value of 'start_of_reign' 
    # for that complex).
    #
    # TODO: Add this functionality to the cleanup script (?)
    temp = df
    complex_dict = df.groupby('pyramid_complex')['start_of_reign'].max().to_dict()
    temp['start_of_reign'] = df['pyramid_complex'].map(complex_dict)

    # This had to be done to get it in the correct order (value was missing)
    temp.loc[temp['pyramid_complex'] == 'Sneferu 3', 'start_of_reign'] = 2574

    # Similarly this situates the queen in the correct dynasty in lieu of an
    # actual start_of_reign value (tail end of the dynasty)
    temp.loc[temp['pyramid_owner'] == 'Khentkaus I', 'start_of_reign'] = 2489.0

    # Drop Mehaa because her pyramid height is unknown
    temp = temp.drop(temp[temp['pyramid_owner'] == 'Mehaa'].index)

    # Drop rows with no pyramid height value
    temp.dropna(subset='height', inplace=True)

    # Take the averages for elements with two height estimates
    temp['height'] = temp['height'].map(average_of_two).astype(float)

    # Create a new dataframe with a subset of data that is needed for the plot
    columns = ['pyramid_owner', 'dynasty', 'royal_status', 'daughter_of', 
                'royal_mother_title', 'likely_wife', 'wife_title', 'vizier', 
                'regent', 'relationship_to_king', 'height', 'title', 'start_of_reign']
    # Create a new dataframe with a subset of data that is needed for the plot
    queens = temp[temp['royal_status'] == 'Queen']
    queen_data = queens[columns]
    queen_data['dynasty'] = queen_data['dynasty'].astype(int)

    
    # Reshape queen data from wide to long (Binary categories get put into a 
    # new column, each category applied to a specific queen given a row, with 
    # the status of that category in another column)
    melted_queens = queen_data.melt(ignore_index=False, 
                                    id_vars=['dynasty', 'height', 
                                             'pyramid_owner', 
                                            'relationship_to_king', 
                                            'daughter_of', 'title',
                                            'start_of_reign'], 
                                    value_vars=['vizier', 'regent', 
                                                'royal_mother_title', 
                                                'likely_wife', 
                                                'wife_title']).reset_index()
    # Select only those rows that correspond to some category applying to a 
    # given queen.
    melted_truth = melted_queens[melted_queens['value'] == True]

    # Sort the queens in chronological order
    melted_truth.sort_values(by=['start_of_reign', 'title'], ascending=[False, True], inplace=True)

    return melted_truth

def create_figure(melted_truth):
    """
    Create a strip plot with the queen pyramid data, with the queen pyramids 
    on the x-axis, the pyramid height on the y-axis. Each queen can have 
    one or more attributes associated with her, and each attribute that 
    applies to a given queen will be represented by a point with a color 
    corresponding to the given attribute. If multiple attributes apply to 
    a given queen, each point will be grouped together as closely as possible 
    on the x-axis while maintaining the same position on the y-axis.

    Input:
        tl: The dataframe containing the pyramid data
    Output:
        A Plotly express strip plot of the pyramid data
    """
    fig = px.strip(
        melted_truth,
        x = 'title',
        y = 'height',
        color = 'variable',
        width = 1200,
        title = 'Attributes of Pyramid-owning Queens',
        labels = {
            'title': 'Queen Pyramid',
            'height': 'Height of Pyramid (meters)',
            'variable': 'Attributes',
        }
    )
    fig.update_layout(
        title_x = 0.5,
        xaxis = dict(
            ticks = 'inside'
        ))
    # Ensure the x axis is organized chronologically
    titles = melted_truth['title'].unique()
    fig.update_xaxes(
        categoryorder = 'array',
        categoryarray = titles
    )

    # Update the legend variable names
    new_names = {'vizier': 'Vizier',
                'regent': 'Regent',
                'royal_mother_title': 'Royal Mother Title',
                'likely_wife': 'Likely Wife',
                'wife_title': 'Wife Title'}
    fig.for_each_trace(lambda t: t.update(name = new_names[t.name]))

    return fig

def main():
    # Import the dataset
    df = pd.DataFrame(pd.read_csv("assets/normalized_pyramid_data.csv"))

    # Prepare the dataframe for plotting
    melted_truth = prepare_dataframe(df)

    # Create the scatterplot
    fig = create_figure(melted_truth)

    # Output the plot as a png image
    fig.write_image("images/jose-queen-height-by-status-scatter.png")

if __name__ == "__main__":
    main()