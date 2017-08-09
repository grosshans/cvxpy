"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from cvxpy import settings as s
from cvxpy.expressions.leaf import Leaf
import cvxpy.lin_ops.lin_utils as lu


class Parameter(Leaf):
    """Parameters in optimization problems.

    Parameters are constant expressions whose value may be specified
    after problem creation. The only way to modify a problem after its
    creation is through parameters. For example, you might choose to declare
    the hyper-parameters of a machine learning model to be Parameter objects;
    more generally, Parameters are useful for computing trade-off curves.
    """
    PARAM_COUNT = 0

    def __init__(self, shape=(), name=None, value=None, **kwargs):
        self.id = lu.get_id()
        if name is None:
            self._name = "%s%d" % (s.PARAM_PREFIX, self.id)
        else:
            self._name = name
        # Initialize with value if provided.
        self._value = None
        super(Parameter, self).__init__(shape, value, **kwargs)

    def get_data(self):
        """Returns info needed to reconstruct the expression besides the args.
        """
        return [self.shape, self._name, self.value, self.attributes]

    def name(self):
        return self._name

    # Getter and setter for parameter value.
    @property
    def value(self):
        """NumPy.ndarray or None: The numeric value of the parameter.
        """
        return self._value

    @value.setter
    def value(self, val):
        self._value = self._validate_value(val)

    @property
    def grad(self):
        """Gives the (sub/super)gradient of the expression w.r.t. each variable.

        Matrix expressions are vectorized, so the gradient is a matrix.

        Returns:
            A map of variable to SciPy CSC sparse matrix or None.
        """
        return {}

    def parameters(self):
        """Returns itself as a parameter.
        """
        return [self]

    def canonicalize(self):
        """Returns the graph implementation of the object.

        Returns:
            A tuple of (affine expression, [constraints]).
        """
        obj = lu.create_param(self, self.shape)
        return (obj, [])

    def __repr__(self):
        """String to recreate the object.
        """
        attr_str = self._get_attr_str()
        if len(attr_str) > 0:
            return "Parameter(%s%s)" % (self.shape, attr_str)
        else:
            return "Parameter(%s)" % (self.shape,)
