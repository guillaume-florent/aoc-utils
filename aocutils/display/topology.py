# coding: utf-8

r"""topology oriented display functions"""

import logging
import time

# import OCC.Display.SimpleGui
from OCC.Core.AIS import AIS_Shape

from aocutils.display.color import prism_color_sequence
from aocutils.topology import Topo
from aocutils.brep.face import Face
from aocutils.brep.edge import Edge

logger = logging.getLogger(__name__)


def solids(display,
           shape,
           transparency=0.,
           color_sequence=None):
    r"""Display each solid of shape in a different color

    Parameters
    ----------
    display :
        Reference to display
    shape : OCC.TopoDS.TopoDS_Shape
    transparency : float
    color_sequence : aocutils.display.color.*_sequence

    """
    if color_sequence is None:
        color_sequence = prism_color_sequence
    the_solids = Topo(shape, return_iter=False).solids
    logger.info("%i solid(s) to display" % len(the_solids))
    ais_context = display.GetContext().GetObject()

    for i, solid in enumerate(the_solids):
        ais_face = AIS_Shape(solid)
        ais_face.SetColor(color_sequence[i % len(color_sequence)])
        ais_face.SetTransparency(transparency)
        ais_context.Display(ais_face.GetHandle())


def shells(display,
           shape,
           transparency=0.,
           color_sequence=None):
    r"""Display each shell of shape in a different color

    Parameters
    ----------
    display :
        Reference to display
    shape : OCC.TopoDS.TopoDS_Shape
    transparency : float
    color_sequence : aocutils.display.color.*_sequence

    """
    if color_sequence is None:
        color_sequence = prism_color_sequence
    the_shells = Topo(shape, return_iter=False).shells
    logger.info("%i shell(s) to display" % len(the_shells))
    ais_context = display.GetContext().GetObject()

    for i, shell in enumerate(the_shells):
        ais_face = AIS_Shape(shell)
        ais_face.SetColor(color_sequence[i % len(color_sequence)])
        ais_face.SetTransparency(transparency)
        ais_context.Display(ais_face.GetHandle())


def faces(display,
          shape,
          transparency=0.,
          show_numbers=True,
          numbers_height=20,
          color_sequence=None):
    r"""Display each face of shape in a different color

    Parameters
    ----------
    display :
        Reference to display
    shape : OCC.TopoDS.TopoDS_Shape
    transparency : float
    show_numbers : bool
        Show the numbering of faces
    numbers_height : int
        Height of displayed numbers if show_numbers is True
    color_sequence : aocutils.display.color.*_sequence

    """
    if color_sequence is None:
        color_sequence = prism_color_sequence
    the_faces = Topo(shape, return_iter=False).faces
    logger.info("%i face(s) to display" % len(the_faces))
    ais_context = display.GetContext().GetObject()

    for i, face in enumerate(the_faces):
        ais_face = AIS_Shape(face)
        ais_face.SetColor(color_sequence[i % len(color_sequence)])
        ais_face.SetTransparency(transparency)
        if show_numbers:
            display.DisplayMessage(point=Face(face).midpoint,
                                   text_to_write=str(i),
                                   height=numbers_height,
                                   message_color=(0, 0, 0))
        ais_context.Display(ais_face.GetHandle())


def edges(display,
          shape,
          width=4,
          show_numbers=True,
          numbers_height=20,
          color_sequence=None):
    r"""Display each edge of shape in a different color

    Parameters
    ----------
    display :
        Reference to display
    shape : OCC.TopoDS.TopoDS_Shape
    width : int
        Edge width for display
    show_numbers : bool
        Show the numbering of faces
    numbers_height : int
        Height of displayed numbers if show_numbers is True
    color_sequence : aocutils.display.color.*_sequence

    """
    if color_sequence is None:
        color_sequence = prism_color_sequence
    the_edges = Topo(shape, return_iter=False).edges
    logger.info("%i edges(s) to display" % len(the_edges))
    ais_context = display.GetContext().GetObject()

    for i, edge in enumerate(the_edges):
        ais_edge = AIS_Shape(edge)
        ais_edge.SetWidth(width)
        ais_edge.SetColor(color_sequence[i % len(color_sequence)])
        if show_numbers:
            display.DisplayMessage(point=Edge(edge).midpoint,
                                   text_to_write=str(i),
                                   height=numbers_height,
                                   message_color=(0, 0, 0))
        ais_context.Display(ais_edge.GetHandle())


def wires(display,
          shape,
          width=4,
          show_numbers=True,
          numbers_height=50,
          repeat=2,
          delay=1.,
          color_sequence=None):
    r"""Display each edge of shape in a different color

    Parameters
    ----------
    display :
        Reference to display
    shape : OCC.TopoDS.TopoDS_Shape
    width : int
        Wire width for display
    show_numbers : bool
        Show the numbering of faces
    numbers_height : int
        Height of displayed numbers if show_numbers is True
    repeat : int
        Number of times to repeat the display sequence
    delay : float
        Number of seconds a wire can be visualized
    color_sequence : aocutils.display.color.*_sequence

    Notes
    -----
    Wires may overlap or a wire may cover another because one or more wires
    use the same edge. This causes the display of wires to be confusing.
    This is the reason why this function displays each wire in turn.

    """
    if color_sequence is None:
        color_sequence = prism_color_sequence
    the_wires = Topo(shape, return_iter=False).wires
    logger.info("%i wire(s) to display" % len(the_wires))
    ais_context = display.GetContext().GetObject()

    # make sure the zoom is about right
    display.DisplayShape(shape)
    display.FitAll()

    # for n in range(repeat):
    for _ in range(repeat):
        for i, wire in enumerate(the_wires):
            display.EraseAll()
            ais_edge = AIS_Shape(wire)
            ais_edge.SetWidth(width)
            ais_edge.SetColor(color_sequence[i % len(color_sequence)])
            ais_context.Display(ais_edge.GetHandle())
            if show_numbers:
                first_edge_of_wire = Topo(wire, return_iter=False).edges[0]
                wrapped_first_edge = Edge(first_edge_of_wire)
                display.DisplayMessage(point=wrapped_first_edge.midpoint,
                                       text_to_write=str(i),
                                       height=numbers_height,
                                       message_color=(0, 0, 0),
                                       update=True)
            time.sleep(delay)  # wait before displaying the next wire
