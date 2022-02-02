# pylint:disable=line-too-long                                 # Allows for longer line length inside a Parametrization
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

from viktor.parametrization import ChildEntityMultiSelectField
from viktor.parametrization import LineBreak
from viktor.parametrization import Parametrization
from viktor.parametrization import Section
from viktor.parametrization import Tab
from viktor.parametrization import ToggleButton


class ProjectParametrization(Parametrization):
    """Defines the input fields in left-side of the web UI in the Sample entity (Editor)."""
    visualization = Tab('Visualization')
    visualization.comparison = Section('Compare CPTs')
    visualization.comparison.selected_cpts = ChildEntityMultiSelectField('Select CPTs that you want to compare',
                                                                         entity_type_names=['CPTFile'], flex=60)
    visualization.comparison.lb1 = LineBreak()
    visualization.comparison.single_graph = ToggleButton('Plot selected cpts in a single graph', default=False)
    visualization.comparison.draw_rf = ToggleButton('Plot Rf signal', default=False)
