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
from io import StringIO

from munch import Munch

from viktor import UserException
from viktor import ViktorController
from viktor.api_v1 import API
from viktor.core import progress_message
from viktor.result import SetParametersResult
from viktor.views import WebResult
from viktor.views import WebView
from .cpt_comparison_helper_functions import visualize_multiple_cpts_in_multiple_graphs
from .cpt_comparison_helper_functions import visualize_multiple_cpts_in_single_graph
from .parametrization import ProjectParametrization
from ..cpt_file.model import CPT


class ProjectController(ViktorController):
    """Controller class which acts as interface for the Sample entity type."""
    label = "Project"
    children = ['CPTFile']
    show_children_as = 'Table'
    parametrization = ProjectParametrization
    viktor_convert_entity_field = True

    @WebView('Compare CPTs', duration_guess=5)
    def compare_cpts(self, params: Munch, **kwargs) -> WebResult:
        """Visualizes multiple cpt that is selected in an optionfield, for comparing"""
        cpt_entities_selected = params.visualization.comparison.selected_cpts

        cpts = []
        for cpt in cpt_entities_selected:
            cpts.append(CPT(cpt.last_saved_params, cpt.id))

        if not cpt_entities_selected:
            raise UserException('Please select CPTs for comparison')

        progress_message("Gathering CPTs to add to comparison")

        if params.visualization.comparison.single_graph:
            figure = visualize_multiple_cpts_in_single_graph(cpts, draw_rf=params.visualization.comparison.draw_rf)
        else:
            figure = visualize_multiple_cpts_in_multiple_graphs(cpts, draw_rf=params.visualization.comparison.draw_rf)

        return WebResult(html=StringIO(figure.to_html()))
