import plotly.express as px
import numpy as np
from Statistic import DataStatistic


# plot data statistic function; data - data of attribute 'attribute_name'
def plot_data(statistic: DataStatistic, attribute_name: str, data):
    value_count = len(data)
    x = np.linespace(1, value_count, value_count)
    fig = px.scatter(x=x, y=data, labels={'x': 'items', 'y': 'value'})
    fig.show()
