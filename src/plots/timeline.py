# King length of rule timeline template

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import the dataset
df = pd.DataFrame(pd.read_csv("assets/normalized_pyramid_data.csv"))

'''
Sort King rows (those with actual values for start_of_reign)  
in chronological order.
'''
tl = df.sort_values(by='start_of_reign', ascending=False)

# Add rule time estimates for Ibi (source: Christelle)
tl.loc[tl['pyramid_complex'] == 'Ibi', ['start_of_reign']] = 2143
tl.loc[tl['pyramid_complex'] == 'Ibi', ['end_of_reign']] = 2141

# Select relevent columns as dataframe and series
tl = tl[['pyramid_owner', 'start_of_reign', 
         'end_of_reign', 'length_of_reign']].dropna()
pyramid_owners = tl['pyramid_owner']
starts = tl['start_of_reign']
ends = tl['end_of_reign']
length = tl['length_of_reign']

# Construct timeline figure
plt.figure(figsize=(16, 8))
#color = cm.rainbow(np.linspace(0, 1, len(starts)))
plt.barh(y=0, 
         width=(ends - starts), 
         height=0.3, 
         left=starts, 
         #color=color, 
         color='none',
         edgecolor='black')
# Tick settings
plt.tick_params(left=False, labelleft=False)
plt.gca().invert_xaxis()
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(10))
# Labeling
plt.xlabel('Year (BCE)')
plt.ylabel('Ruler')
plt.title('Reign of Ruler')

'''
Determine the height and positioning of label lines.

Kept in a hacky attempt at maintaining vertical width of timeline.
Remove alpha variable if label lines are desired.
 '''
levels = np.tile([-2, 2, -1, 1], 
                 int(np.ceil(len(pyramid_owners) / 4)))[:len(pyramid_owners)]
plt.vlines(starts - length/2, 0, levels/2, color='black', alpha=0)

# Figure label text (removed for template version)
'''
for i in range(len(starts)):
    plt.text(starts.iloc[i] - length.iloc[i]/2, 
             (levels[i]*1.05)/2, 
             pyramid_owners.iloc[i], 
             ha='center', 
             fontsize = '7')
'''

# Output figure as a png image
plt.savefig('images/jose_timeline.png')