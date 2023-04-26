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

from viktor import UserError
from viktor import ViktorController
from viktor.core import progress_message
from viktor.views import WebResult
from viktor.views import WebView
from .cpt_comparison_helper_functions import visualize_multiple_cpts_in_graph
from .parametrization import ProjectParametrization
from ..cpt_file.model import CPT


class ProjectController(ViktorController):
    """Controller class which acts as interface for the Sample entity type."""
    label = "Project"
    children = ['CPTFile']
    show_children_as = 'Table'
    parametrization = ProjectParametrization(width=20)

    @WebView('Compare CPTs', duration_guess=5)
    def compare_cpts(self, params: Munch, **kwargs) -> WebResult:
        """Visualizes multiple cpt that is selected in an optionfield, for comparing"""
        progress_message("Gathering CPTs to add to comparison")
        cpts = self.get_all_cpts(params)
        figure = visualize_multiple_cpts_in_graph(cpts=cpts, single_graph=params.single_graph)

        return WebResult(html=StringIO(figure.to_html()))

    @staticmethod
    def get_all_cpts(params):
        """"retrieve params from selected cpts and create new cpt objects"""
        if not params.selected_cpts:
            raise UserError('Please select CPTs for comparison')

        cpts = []
        for cpt in params.selected_cpts:
            cpts.append(CPT(cpt.last_saved_params))

        return cpts
