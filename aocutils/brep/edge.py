# coding: utf-8

r"""edge module of aocutils"""

from __future__ import print_function

import logging

from OCC.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_HCurve
# import OCC.BRepBuilderAPI
from OCC.GCPnts import GCPnts_AbscissaPoint, GCPnts_UniformAbscissa
from OCC.Geom import Geom_TrimmedCurve, Geom_OffsetCurve
from OCC.TopExp import topexp
from OCC.TopoDS import TopoDS_Vertex, TopoDS_Edge, TopoDS_Face
from OCC.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.GeomLProp import GeomLProp_CurveTool
from OCC.BRepLProp import BRepLProp_CLProps
from OCC.GeomLib import geomlib
from OCC.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.ShapeAnalysis import ShapeAnalysis_Edge
from OCC.BRep import BRep_Tool_Curve, BRep_Tool, BRep_Tool_Continuity
from OCC.BRepIntCurveSurface import BRepIntCurveSurface_Inter
# import OCC.BRepCheck

from aocutils.analyze.distance import MinimumDistance
from aocutils.brep.base import BaseObject
from aocutils.brep.edge_make import edge
from aocutils.common import AssertIsDone
from aocutils.brep.vertex import Vertex
from aocutils.types import geom_lut
from aocutils.exceptions import WrongTopologicalType,\
    ParameterOutOfDomainException, UniformAbscissaException, \
    UndefinedPropertyException
from aocutils.fixes import fix_continuity
from aocutils.tolerance import OCCUTILS_DEFAULT_TOLERANCE
from aocutils.display.display import show

logger = logging.getLogger(__name__)


class Edge(BaseObject):
    r"""Wrapper for TopoDS_Edge

    Parameters
    ----------
    topods_edge : TopoDS_Edge

    """
    def __init__(self, topods_edge):
        if not isinstance(topods_edge, TopoDS_Edge):
            msg = 'Need a TopoDS_Edge, got a %s' % topods_edge.__class__
            logger.critical(msg)
            raise WrongTopologicalType(msg)

        if topods_edge.IsNull():
            raise ValueError("topods_edge should no be Null")

        BaseObject.__init__(self, topods_edge, name='edge')

        self._adaptor = None
        self._brep_local_props = None

    @property
    def topods_edge(self):
        return self._wrapped_instance

    @property
    def adaptor(self):
        r"""Adaptor

        Returns
        -------
        OCC.BRepAdaptor.BRepAdaptor_Curve

        """
        if self._adaptor is None:
            self._adaptor = BRepAdaptor_Curve(self._wrapped_instance)
        return self._adaptor

    # def to_adaptor_3d(self):
    #     r"""Abstract curve like geom_type into an adaptor3d
    #
    #     Parameters
    #     ----------
    #     curve
    #
    #     Returns
    #     -------
    #
    #     """
    #     return OCC.BRepAdaptor.BRepAdaptor_Curve(self._wrapped_instance)

    @property
    def is_closed(self):
        r"""

        Returns
        -------
        bool

        """
        return self.adaptor.IsClosed()

    @property
    def is_periodic(self):
        r"""

        Returns
        -------
        bool

        """
        return self.adaptor.IsPeriodic()

    @property
    def is_rational(self):
        r"""

        Returns
        -------
        bool

        """
        return self.adaptor.IsRational()

    @property
    def continuity(self):
        r"""Continuity

        Returns
        -------
        int
            enum GeomAbs_Shape {GeomAbs_C0, GeomAbs_G1, GeomAbs_C1, GeomAbs_G2,
                                GeomAbs_C2, GeomAbs_C3, GeomAbs_CN}

        """
        continuities = ["GeomAbs_C0",
                        "GeomAbs_G1",
                        "GeomAbs_C1",
                        "GeomAbs_G2",
                        "GeomAbs_C2",
                        "GeomAbs_C3",
                        "GeomAbs_CN"]
        return continuities[self.adaptor.Continuity()]

    @property
    def degree(self):
        r"""Degree

        Returns
        -------
        int

        """
        if 'line' in self.geom_type:
            return 1
        elif 'curve' in self.geom_type:
            # TODO : degenerated edge of sphere (degenerated to a point)
            #        has an 'othercurve' geom type
            return self.adaptor.Degree()
        else:
            return 2  # hyperbola, parabola, circle

    @property
    def nb_knots(self):
        r"""Number of knots

        Returns
        -------
        int
            The number of knots

        """
        # todo : fix it for lines and circle edges
        try:
            return self.adaptor.NbKnots()
        except RuntimeError:
            return -1

    @property
    def nb_poles(self):
        r"""Number of poles

        Returns
        -------
        int
            The number of poles

        """
        # todo : fix it for lines and circle edges
        try:
            return self.adaptor.NbPoles()
        except RuntimeError:
            return -1

    @property
    def curve(self):
        r"""Curve

        Returns
        -------
        Geom_Curve

        """
        return self.curve_handle.GetObject()

    # def to_curve(self):
    #     r"""Returns a curve adaptor from an edge
    #
    #     Parameters
    #     ----------
    #     edg : TopoDS_Edge
    #
    #     Returns
    #     -------
    #     OCC.BRepAdaptor.BRepAdaptor_Curve
    #         A curve adaptor from an edge
    #
    #     """
    #     return OCC.BRepAdaptor.BRepAdaptor_Curve(self._wrapped_instance)

    @property
    def curve_handle(self):
        r"""Curve handle

        Returns
        -------
        Handle< Geom_Curve >

        """
        return BRep_Tool_Curve(self._wrapped_instance)[0]

    # def to_hcurve(self):
    #     r"""Adapt edge to HCurve
    #
    #     Parameters
    #     ----------
    #     edg : OCC.topoDS.TopoDS_Edge
    #
    #     Returns
    #     -------
    #     OCC.BRepAdaptor.BRepAdaptor_HCurve
    #
    #     """
    #     brep_adaptor_hcurve = OCC.BRepAdaptor.BRepAdaptor_HCurve()
    #     brep_adaptor_hcurve.ChangeCurve().Initialize(self._wrapped_instance)
    #     return brep_adaptor_hcurve

    @property
    def adaptor_handle(self):
        r"""Adaptor handle

        Returns
        -------

        """
        return BRepAdaptor_HCurve(self.adaptor)

    @property
    def geom_curve_handle(self):
        r"""Geom curve handle

        Returns
        -------
        Handle_Geom_Curve
            Handle_Geom_Curve adapted from `self`

        """
        return self.adaptor.Curve().Curve()

    @property
    def geom_type(self):
        r"""Geom Type

        Returns
        -------
        str
            One of the possible values in types.py/geom_types_dict


        """
        return geom_lut[self.adaptor.Curve().GetType()]

    def pcurve(self, face):
        r"""2d parametric spline that lies on the surface of the face

        Parameters
        ----------
        face

        Returns
        -------
        Geom2d_Curve
        u
        v

        """
        crv, u, v = BRep_Tool().CurveOnSurface(self._wrapped_instance,
                                                        face)
        return crv.GetObject(), u, v

    @property
    def geom_local_props(self):
        r"""Geom local properties of the curve

        Returns
        -------
        GeomLProp_CurveTool

        """
        return GeomLProp_CurveTool()

    @property
    def brep_local_props(self):
        r"""Local properties of the curve

        Returns
        -------
        BRepLProp_CLProps

        """
        if self._brep_local_props is None:
            self._brep_local_props = BRepLProp_CLProps(self.adaptor,
                                                       2,
                                                       self.tolerance)
        return self._brep_local_props

    @property
    def domain(self):
        r"""u,v domain of the curve

        Returns
        -------
        tuple[float]
            Tuple with the first parameter and the last parameter

        """
        return self.adaptor.FirstParameter(), self.adaptor.LastParameter()

    @property
    def domain_start(self):
        return self.domain[0]

    @property
    def domain_end(self):
        return self.domain[1]

    def length(self,
               lbound=None,
               ubound=None,
               tolerance=OCCUTILS_DEFAULT_TOLERANCE):
        r"""Curve length

        If either lbound | ubound | both are given, then the length
        of the curve will be measured over that interval

        Parameters
        ----------
        lbound
        ubound
        tolerance : float

        Returns
        -------
        float
            The length

        """
        _min, _max = self.domain
        if _min < self.adaptor.FirstParameter():
            msg = 'the lbound argument is < to the first parameter of the curve: %s' % self.adaptor.FirstParameter()
            logger.error(msg)
            raise ParameterOutOfDomainException(msg)

        if _max > self.adaptor.LastParameter():
            msg = 'the ubound argument is > to the last parameter of the curve: %s' % self.adaptor.LastParameter()
            logger.error(msg)
            raise ParameterOutOfDomainException(msg)

        lbound = _min if lbound is None else lbound
        ubound = _max if ubound is None else ubound
        return GCPnts_AbscissaPoint().Length(self.adaptor,
                                                        lbound,
                                                        ubound,
                                                        tolerance)

    def trim(self, lbound, ubound):
        r"""Trim the curve

        Parameters
        ----------
        lbound
        ubound

        Returns
        -------
        Edge

        """
        a, b = sorted([lbound, ubound])
        trimmed_curve = Geom_TrimmedCurve(self.adaptor.Curve().Curve(),
                                          a,
                                          b).GetHandle()
        return Edge(edge(trimmed_curve))

    def extend_by_point(self, pnt, continuity=3, after=True):
        r"""Extends the curve to point

        does not extend if the degree of self.curve > 3

        Parameters
        ----------
        pnt : .gp_Pnt
        continuity : int
        after

        """
        if self.continuity > 3:
            raise ValueError('to extend you self.curve should be <= 3, is %s' % self.degree)
        # return geomlib.ExtendCurveToPoint(self.curve, pnt, continuity, after)
        geomlib.ExtendCurveToPoint(self.curve, pnt, continuity, after)

    def closest(self, other):
        r"""Closest

        Parameters
        ----------
        other

        Returns
        -------
        float
            The minimal distance

        """
        return MinimumDistance(self._wrapped_instance, other).minimum_distance

    def project_vertex(self, pnt_or_vertex):
        r"""Returns the closest orthogonal project on pnt on edge

        Parameters
        ----------
        pnt_or_vertex

        Returns
        -------
        Quantity_Parameter, gp_Pnt

        """
        if isinstance(pnt_or_vertex, TopoDS_Vertex):
            pnt_or_vertex = Vertex.to_pnt(pnt_or_vertex)

        project_point_on_curve = GeomAPI_ProjectPointOnCurve(pnt_or_vertex,
                                                             self.curve_handle)
        return (project_point_on_curve.LowerDistanceParameter(),
                project_point_on_curve.NearestPoint())

    def distance_on_curve(self, distance, close_parameter, estimate_parameter):
        r"""Returns the parameter if there is a parameter on the curve with a distance length from u

        Parameters
        ----------
        distance
        close_parameter
        estimate_parameter

        Returns
        -------
        float
            Parameter on the curve of the point solution of this algorithm

        Raises
        ------
        OutOfBoundary
            if no such parameter exists
        """
        abscissa_point = GCPnts_AbscissaPoint(self.adaptor,
                                              distance,
                                              close_parameter,
                                              estimate_parameter,
                                              1e-5)
        with AssertIsDone(abscissa_point, 'could not compute distance on curve'):
            return abscissa_point.Parameter()

    @property
    def midpoint(self):
        r"""Mid point

        Returns
        -------
        float
            the parameter at the mid point of the curve
        .gp_Pnt
            gp_Pnt corresponding to the parameter
        """
        return self.adaptor.Value(self.midpoint_parameter)

    @property
    def midpoint_parameter(self):
        r"""Value of the parameter at the edge midpoint

        Returns
        -------
        float

        """
        _min, _max = self.domain
        return (_min + _max) / 2.

    def divide_by_number_of_points(self, n_pts, lbound=None, ubound=None):
        r"""Nested list of parameters and points on the edge
        at the requested interval [(param, gp_Pnt),...]

        Parameters
        ----------
        n_pts
        lbound
        ubound

        Returns
        -------
        list[tuple]

        """
        _lbound, _ubound = self.domain
        if lbound:
            _lbound = lbound
        elif ubound:
            _ubound = ubound

        # minimally two points or a Standard_ConstructionError is raised
        if n_pts <= 1:
            n_pts = 2

        try:
            npts = GCPnts_UniformAbscissa(self.adaptor,
                                          n_pts,
                                          _lbound,
                                          _ubound)
        except:  # TODO : specify exceptions
            logger.warning("OCC.GCPnts.GCPnts_UniformAbscissa failed")

        if npts.IsDone():
            tmp = []
            for i in range(1, npts.NbPoints()+1):
                param = npts.Parameter(i)
                pnt = self.adaptor.Value(param)
                tmp.append((param, pnt))
            return tmp
        else:
            msg = 'GCPnts_UniformAbscissa is not done'
            logger.error(msg)
            raise UniformAbscissaException(msg)

    def first_vertex(self):
        """First vertex

        Returns
        -------
        TopoDS_Vertex

        """
        return topexp.FirstVertex(self._wrapped_instance)

    def last_vertex(self):
        r"""Last vertex

        Returns
        -------
        TopoDS_Vertex

        """
        return topexp.LastVertex(self._wrapped_instance)

    def common_vertex(self, edge):
        """Finds the vertex  common to the two edges <E1,E2>

        Parameters
        ----------
        edge

        Returns
        -------
        bool
            True if the Vertex exists

        """
        vert = TopoDS_Vertex()
        if topexp.CommonVertex(self._wrapped_instance, edge, vert):
            return vert
        else:
            return False

    def as_vec(self):
        r"""Vector constructed from the first vertex to the last vertex

        Returns
        -------
        gp_Vec

        """
        if self.is_line():
            first, last = list(map(Vertex.to_pnt,
                                   [self.first_vertex(), self.last_vertex()]))
            return gp_Vec(first, last)
        else:
            msg = "edge is not a line, " \
                  "hence no meaningful vector can be returned"
            logger.error(msg)
            raise ValueError(msg)

    def _check_u_in_domain(self, u):
        if not self.domain[0] <= u <= self.domain[1]:
            msg = "Parameter is outside of domain ranging from " \
                  "%s to %s" % (str(self.domain[0]), str(self.domain[0]))
            logger.error(msg)
            raise ParameterOutOfDomainException(msg)
        else:
            pass

    def parameter_to_point(self, u):
        r"""returns the coordinate at parameter u

        Parameters
        ----------
        u

        Returns
        -------
        .gp_Pnt

        """
        self._check_u_in_domain(u)
        return self.adaptor.Value(u)

    def fix_continuity(self, continuity):
        r"""Splits an edge to achieve a level of continuity

        Parameters
        ----------
        continuity : GeomAbs_C*

        Returns
        -------
        TopoDS_Shape

        """
        return fix_continuity(self._wrapped_instance, continuity)

    def continuity_from_faces(self, f1, f2):
        r"""Continuity along self for 2 faces

        Parameters
        ----------
        f1 : TopoDS_Face
        f2 : TopoDS_Face

        Returns
        -------
        OCC.GeomAbs.GeomAbs_Shape

        """
        return BRep_Tool_Continuity(self._wrapped_instance, f1, f2)

    def is_line(self):
        r"""Is the edge a line?

        Returns
        -------
        bool

        """
        if self.nb_knots == 2 and self.nb_poles == 2:
            return True
        else:
            return False

    def is_seam(self, face):
        r"""Is the edge a seam?

        Parameters
        ----------
        face

        Returns
        -------
        bool
            True if the edge has two pcurves on one surface
            (in the case of a sphere for example... )
        """
        sae = ShapeAnalysis_Edge()
        return sae.IsSeam(self._wrapped_instance, face)

    def is_edge_on_face(self, face):
        r"""Checks whether curve lies on a surface or a face

        Parameters
        ----------
        face

        Returns
        -------
        bool?

        """
        return ShapeAnalysis_Edge().HasPCurve(self._wrapped_instance, face)

    def intersect(self, other, tolerance=1e-2):
        r"""Intersect self with a point, curve, edge, face, solid method wraps dealing with the various topologies

        Parameters
        ----------
        other : TopoDS_*
        tolerance : float

        Returns
        -------
        list[.gp_Pnt]

        """
        if isinstance(other, TopoDS_Face):
            face_curve_intersect = BRepIntCurveSurface_Inter()
            face_curve_intersect.Init(other, self.adaptor.Curve(), tolerance)
            pnts = []
            while face_curve_intersect.More():
                face_curve_intersect.Next()
                pnts.append(face_curve_intersect.Pnt())
            return pnts

    def radius(self, u):
        r"""Radius at u

        Parameters
        ----------
        u : float

        Returns
        -------
        .gp_Pnt

        Raises
        ------
        aocutils.exceptions.UndefinedPropertyException
            If the radius is not defined

        """
        self._check_u_in_domain(u)
        # NOT SO SURE IF THIS IS THE SAME THING!!!
        self.brep_local_props.SetParameter(u)
        pnt = .gp_Pnt()
        try:
            self.brep_local_props.CentreOfCurvature(pnt)
            return pnt
        except RuntimeError:
            msg = "Undefined radius for the edge"
            logger.error(msg)
            raise UndefinedPropertyException(msg)

    def curvature(self, u):
        r"""Curvature at u

        Parameters
        ----------
        u : float

        Returns
        -------
        float

        """
        self._check_u_in_domain(u)
        self.brep_local_props.SetParameter(u)
        return self.brep_local_props.Curvature()

    def tangent(self, u):
        r"""sets or gets ( iff vector ) the tangency at the u parameter
        tangency can be constrained so when setting the tangency,
        you're constraining it in fact

        Parameters
        ----------
        u

        Returns
        -------
        .gp_Dir

        """
        self._check_u_in_domain(u)
        self.brep_local_props.SetParameter(u)
        if self.brep_local_props.IsTangentDefined():
            ddd = .gp_Dir()
            self.brep_local_props.Tangent(ddd)
            return ddd
        else:
            raise ValueError('no tangent defined')

    def normal(self, u):
        r"""Normal at u

        computes the main normal if no normal is found

        References
        ----------
        www.opencascade.org/org/forum/thread_645+&cd=10&hl=nl&ct=clnk&gl=nl

        Parameters
        ----------
        u : float

        Returns
        -------
        .gp_Dir

        Raises
        ------
        ValueError
            If the normal is not defined

        """
        self._check_u_in_domain(u)
        try:
            self.brep_local_props.SetParameter(u)
            a_dir = .gp_Dir()
            self.brep_local_props.Normal(a_dir)
            return a_dir
        except:
            raise ValueError('no normal was found')

    def derivative(self, u, n):
        r"""n-th derivatives at parameter b

        Parameters
        ----------
        u : float
        n : int

        Returns
        -------
        gp_Vec

        """
        self._check_u_in_domain(u)
        self.brep_local_props.SetParameter(u)
        deriv = {1: self.brep_local_props.D1(),
                 2: self.brep_local_props.D2(),
                 3: self.brep_local_props.D3(),
                 }
        try:
            return deriv[n]
        except KeyError:
            raise AssertionError('n of derivative is one of [1,2,3]')

    def points_from_tangential_deflection(self):
        r"""

        Returns
        -------

        """
        raise NotImplementedError

    def make_offset(self, offset, vec):
        r"""Offset curve

        Parameters
        ----------
        offset : float
            The distance between self.crv and the curve to offset
        vec :
            Offset direction

        Returns
        -------
        Geom_OffsetCurve

        """
        return Geom_OffsetCurve(self.curve_handle, offset, vec)

    def show(self):
        r"""poles, knots, should render all slightly different.
        here's how...

        http://www.opencascade.org/org/forum/thread_1125/

        """
        show(self._wrapped_instance, "wx")

    # @property
    # def geom_type(self):
    #     r"""Geometrical geom_type"""
    #     return occutils.types.curve_lut[self._wrapped_instance.ShapeType()]

    def __eq__(self, other):
            return self._wrapped_instance.IsEqual(other)

    def __ne__(self, other):
        return not self.__eq__(other)
