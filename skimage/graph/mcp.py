from ._mcp import MCP, MCP_Geometric, make_offsets


def route_through_array(array, start, end, fully_connected=True,
                        geometric=True):
    """Simple example of how to use the MCP and MCP_Geometric classes.

    See the MCP and MCP_Geometric class documentation for explanation of the
    path-finding algorithm.

    Parameters
    ----------
    array : ndarray
        Array of costs.
    start : iterable
        n-d index into `array` defining the starting point
    end : iterable
        n-d index into `array` defining the end point
    fully_connected : bool (optional)
        If True, diagonal moves are permitted, if False, only axial moves.
    geometric : bool (optional)
        If True, the MCP_Geometric class is used to calculate costs, if False,
        the MCP base class is used. See the class documentation for
        an explanation of the differences between MCP and MCP_Geometric.

    Returns
    -------
    path : list
        List of n-d index tuples defining the path from `start` to `end`.
    cost : float
        Cost of the path.

    Examples
    --------
    >>> from skimage.graph import route_through_array
    >>> image = np.arange((36)).reshape((6, 6))
    >>> image
    array([[ 0,  1,  2,  3,  4,  5],
           [ 6,  7,  8,  9, 10, 11],
           [12, 13, 14, 15, 16, 17],
           [18, 19, 20, 21, 22, 23],
           [24, 25, 26, 27, 28, 29],
           [30, 31, 32, 33, 34, 35]])
    >>> # Find the path with lowest cost
    >>> indices, weight = route_through_array(image, (0, 0), (5, 5))
    >>> indices = np.array(indices).T
    >>> path = np.zeros_like(image)
    >>> path[indices[0], indices[1]] = 1
    >>> path
    array([[1, 1, 1, 1, 1, 0],
           [0, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 1]])
    >>> # Forbid diagonal steps
    >>> indices, weight = route_through_array(image, (0, 0), (5, 5), \
    fully_connected=False)
    >>> indices = np.array(indices).T
    >>> path = np.zeros_like(image)
    >>> path[indices[0], indices[1]] = 1
    >>> path
    array([[1, 1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 1]])

    """
    start, end = tuple(start), tuple(end)
    if geometric:
        mcp_class = MCP_Geometric
    else:
        mcp_class = MCP
    m = mcp_class(array, fully_connected=fully_connected)
    costs, traceback_array = m.find_costs([start], [end])
    return m.traceback(end), costs[end]
