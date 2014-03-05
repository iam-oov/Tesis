#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Clemens' Bezier Problemoo with PySide/Qt
# 2011-01-20 18:15 Thomas Perl <thp.io/about>
#

from PySide.QtCore import *
from PySide.QtGui import *

import sys
import random

# Canvas size for output
SIZE = 500, 500

# Border width around canvas (for window)
BORDER = 14

# Number of segments for each bezier curve
SEGMENTS = 100

# Should the bezier lines be wiggly? (if so, how much?)
WIGGLY = 2


def interp(p1, p2, v):
    """Interpolate between p1 and p2 at value v

    p1 and p2 are each a two-number tuple (x, y).
    v is a float value 0..1.

    If v is 0, the result is p1.
    If v is 1, the result is p2.
    """
    return (p1[0]*v+p2[0]*(1-v), p1[1]*v+p2[1]*(1-v))


def segments(p):
    """Convert a list of points into line segments

    p is an iterable having two-number tuples (x, y)
    as elements. The result is a list of segments
    ((x1, y1), (x2, y2)) connecting all points.

    Duplicate points are ignored (i.e. no lines are
    created in the result where x1==x2 and y1==y2).
    """
    result = []

    first = None
    last = None

    for x in p:
        if first is None:
            first = x

        if last is not None:
            if x != last:
                result.append((last, x))

        last = x

    return result


def bezier(p0, p1, p2):
    """Create a bezier line from p0 to p2 using p1

    p0 is a two-number tuple (x, y) of the start point.
    p1 is a two-number tuple (x, y) of the control point.
    p2 is a two-number tuple (x, y) of the end point.

    The global constant SEGMENTS will be used to set
    the number of points/segments. The more segments,
    the more smooth the resulting bezier line is.
    """
    yield p0

    for i in range(SEGMENTS-1):
        v = 1.-(float(i+1)/SEGMENTS)
        q1 = interp(p0, p1, v)
        q2 = interp(p1, p2, v)
        p = interp(q1, q2, v)
        yield p

    yield p2

class BezierSegment(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, pen):
        QGraphicsLineItem.__init__(self, x1, y1, x2, y2)
        self.setPen(pen)
        self.coords = x1, y1, x2, y2

    def transform(self, c):
        return [x + random.uniform(-WIGGLY, WIGGLY) for x in c]

    def wiggle(self, oldpos=None, last=False):
        if oldpos is None:
            oldpos = list(self.coords[:2])
        newpos = list(self.coords[2:])
        if not last:
            newpos = self.transform(newpos)
        self.setLine(*(oldpos+newpos))
        return newpos

class Bezier(object):
    def __init__(self, s, p0, p1, p2, color=None):
        """Add a bezier line to a QGraphicsScene

        s is a QGraphicsScene to which the line is added
        p0, p1 and p2 are two-number tuples (x, y) for the bezier line
        color is either a QColor or a Qt global color (e.g. Qt.red)
        """
        self.children = []

        pe = QPen(color) if color else QPen()
        br = QBrush(color) if color else QBrush()
        gr = (QPen(Qt.gray),)

        # Gray lines p0<->p1<->p2
        s.addLine(*(p0+p1+gr))
        s.addLine(*(p1+p2+gr))

        self.lines = list(segments(bezier(p0, p1, p2)))

        # Create the bezier curve and transform into line segments
        for a, b in self.lines:
            l = BezierSegment(*(a+b+(pe,)))
            self.children.append(l)
            s.addItem(l)

        # Wiggle all segments, fixing the first and last point to
        # their original values to have a proper attachment
        self.wiggle()

    def wiggle(self):
        oldpos = None
        end = len(self.children) - 1
        for i, c in enumerate(self.children):
            oldpos = c.wiggle(oldpos, i == end)

class MyScene(QGraphicsScene):
    COLORS = (
            Qt.red,
            Qt.green,
            Qt.blue,
            Qt.darkCyan,
            Qt.darkMagenta,
            Qt.darkYellow,
    )

    def __init__(self):
        QGraphicsScene.__init__(self)
        self.curves = 0
        self.coords = []
        self.beziers = []

    def mouseReleaseEvent(self, event):
        c = MyScene.COLORS[self.curves % len(MyScene.COLORS)]
        x, y = event.scenePos().x(), event.scenePos().y()
        self.coords.append((x, y))
        self.addEllipse(QRectF(x-3, y-3, 6, 6), QPen(c), QBrush(c))
        if len(self.coords) == 3:
            self.coords.append(c)
            print self.coords
            self.beziers.append(Bezier(self, *self.coords))
            self.coords = []
            self.curves += 1

# Create the GUI application structures
app = QApplication(sys.argv)
scene = MyScene()
scene.setSceneRect(QRectF(0, 0, *SIZE).adjusted(*((-BORDER,)*2 + (BORDER,)*2)))

# Render the created scene on-screen
view = QGraphicsView(scene)
view.setRenderHint(QPainter.Antialiasing)
view.setWindowTitle('Wiggly bezier curves')
view.show()

# Qt main loop
sys.exit(app.exec_())
