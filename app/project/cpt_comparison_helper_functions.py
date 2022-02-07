"""Copyright (c) 2022 VIKTOR B.V.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

VIKTOR B.V. PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from itertools import cycle
from math import ceil
from math import floor
from typing import List

import plotly as plt
from plotly import graph_objects as go
from plotly.subplots import make_subplots

from viktor.core import progress_message
from ..cpt_file.model import CPT


def visualize_multiple_cpts_in_single_graph(cpts: List[CPT], draw_rf: bool = False) -> go.Figure:
    """
    Plot the Qc signal for multiple cpts in a single graph for comparison purposes. If requested, also draw
    a graph for the resistances. In the latter case signal are added per cpt and can be swichted off
    through the legend, the y-axis is shared.
    """
    color_cycle = cycle(plt.colors.qualitative.G10)

    # make subplots
    if draw_rf:
        fig = make_subplots(rows=1, cols=2, shared_yaxes=True,
                            subplot_titles=("cone resistance", "friction number"))
    else:
        fig = make_subplots(rows=1, cols=1)

    for i, cpt in enumerate(cpts):
        progress_message(f"Adding cpt {cpt.name} to comparison", percentage=(i/len(cpts)*100))
        selected_color = next(color_cycle)

        # Plot the Qc signal
        fig.add_trace(
            go.Scatter(name=f'Qc {cpt.name}',
                       hovertext=f'{cpt.name}',
                       x=cpt.parsed_cpt.qc,
                       y=[el * 1e-3 for el in cpt.parsed_cpt.elevation],
                       mode='lines',
                       line=dict(color=selected_color, width=1.25),
                       legendgroup=f'{cpt.name}'),
            row=1, col=1
        )

        # Draw resistance if requested
        if draw_rf:
            fig.add_trace(
                go.Scatter(name=f'Rf {cpt.name}',
                           hovertext=f'{cpt.name}',
                           x=[rfval * 100 if rfval else rfval for rfval in cpt.parsed_cpt.Rf],
                           y=[el * 1e-3 if el else el for el in cpt.parsed_cpt.elevation],
                           mode='lines',
                           line=dict(color=selected_color, width=1.25),
                           legendgroup=f'{cpt.name}'),
                row=1, col=2
            )

    # Format axes and grids per subplot
    standard_grid_options = dict(showgrid=True, gridwidth=1, gridcolor='DarkGrey')
    standard_line_options = dict(showline=True, linewidth=2, linecolor='DarkGrey')

    fig.update_xaxes(row=1, col=1, **standard_line_options, **standard_grid_options,
                     range=[0, 30], tick0=0, dtick=1, title_text="Qc [MPa]")
    fig.update_yaxes(row=1, col=1, **standard_grid_options, title_text="Depth [m] w.r.t. NAP",
                     tick0=floor(min([cpt.parsed_cpt.elevation[-1] for cpt in cpts])/1e3)-5, dtick=1)
    if draw_rf:
        fig.update_xaxes(row=1, col=2, **standard_line_options, **standard_grid_options,
                         range=[10, 0], tick0=0, dtick=1, title_text="Rf [%]")
        fig.update_yaxes(row=1, col=2, **standard_grid_options,
                         tick0=floor(min([cpt.parsed_cpt.elevation[-1] for cpt in cpts])/1e3)-5, dtick=1)

    fig.update_layout(template='plotly_white')  # Forces white background

    return fig


def visualize_multiple_cpts_in_multiple_graphs(cpts: List[CPT], draw_rf: bool = False) -> go.Figure:
    """
    Plot the Qc signal for multiple cpts as a collection of subplots on a horizontal layout. If requested,
    also draw a series of subplots graph for the resistances.
    """

    # make subplots
    if draw_rf:
        fig = make_subplots(rows=2, cols=len(cpts), shared_yaxes=True, shared_xaxes='rows',
                            column_titles=[f'{cpt.name[:-4]}' for cpt in cpts])
    else:
        fig = make_subplots(rows=1, cols=len(cpts), shared_yaxes=True, shared_xaxes='rows',
                            column_titles=[f'{cpt.name[:-4]}' for cpt in cpts])

    for i, cpt in enumerate(cpts, start=1):
        progress_message(f"Adding Qc plot for cpt {cpt.name} to comparison", percentage=((i-1)/len(cpts)*100))

        # Plot the Qc signal
        fig.add_trace(
            go.Scatter(
                name=f'Qc {cpt.name}',
                hovertext=f'{cpt.name}',
                x=cpt.parsed_cpt.qc,
                y=[el * 1e-3 for el in cpt.parsed_cpt.elevation],
                mode='lines',
                line=dict(color='mediumblue', width=1.25)),
            row=1, col=i
        )

    # Draw resistance if requested
    if draw_rf:
        for i, cpt in enumerate(cpts, start=1):
            progress_message(f"Adding Rf plot for cpt {cpt.name} to comparison", percentage=((i-1)/len(cpts)*100))
            fig.add_trace(
                go.Scatter(
                    name='Friction number',
                    x=[rfval * 100 if rfval else rfval for rfval in cpt.parsed_cpt.Rf],
                    y=[el * 1e-3 if el else el for el in cpt.parsed_cpt.elevation],
                    mode='lines',
                    line=dict(color='red', width=1.25)),
                row=2, col=i
            )

    # Format axes and grids per subplot
    standard_grid_options = dict(showgrid=True, gridwidth=1, gridcolor='DarkGrey')
    standard_line_options = dict(showline=True, linewidth=2, linecolor='DarkGrey')

    fig.update_xaxes(
        row=1,
        **standard_line_options,
        **standard_grid_options,
        range=[0, 30],
        tick0=0,
        dtick=1,
        title_text="Qc [MPa]"
    )

    fig.update_yaxes(
        **standard_grid_options,
        range=[
            floor(min([cpt.parsed_cpt.elevation[-1] for cpt in cpts])/1e3)-5,
            ceil(max([cpt.parsed_cpt.elevation[0] for cpt in cpts])/1e3)+1
        ],
        tick0=ceil(max([cpt.parsed_cpt.elevation[0] for cpt in cpts])/1e3)+1,
        dtick=1
    )

    fig.update_yaxes(
        col=1,
        **standard_grid_options,
        title_text="Depth [m]",
        range=[
            floor(min([cpt.parsed_cpt.elevation[-1] for cpt in cpts])/1e3)-5,
            ceil(max([cpt.parsed_cpt.elevation[0] for cpt in cpts])/1e3)+1
        ],
        tick0=ceil(max([cpt.parsed_cpt.elevation[0] for cpt in cpts])/1e3)+1,
        dtick=1
    )

    if draw_rf:
        fig.update_xaxes(
            row=2,
            **standard_line_options,
            **standard_grid_options,
            range=[10, 0],
            tick0=0,
            dtick=1,
            title_text="Rf [%]"
        )

    # Set subplot titles to a lower fontsize, because they are usually long names
    for subplot_title in fig['layout']['annotations']:
        subplot_title['font'] = dict(size=10)

    fig.update_layout(template='plotly_white', showlegend=False)  # Forces white background

    return fig
