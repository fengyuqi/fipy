#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "gist1DViewer.py"
 #                                    created: 11/10/03 {2:48:25 PM} 
 #                                last update: 4/5/05 {5:34:27 PM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

__docformat__ = 'restructuredtext'

import Numeric
 
from fipy.viewers.gistViewer import _GistViewer

class Gist1DViewer(_GistViewer):
    """
    Displays a y vs. x plot of one or more 1D `CellVariable` objects.
    Usage:

    ::
    
        viewer = Gist1DViewer(vars)
        viewer.plot()

    """
    
    def __init__(self, vars, title = None, limits = None, xlog = 0, ylog = 0, style = "work.gs"):
        """
        Creates a `Gist1DViewer`.
        
        :Parameters:
          - `vars`: a `CellVariable` or tuple of `CellVariable` objects to plot
          - `limits`: a dictionary with possible keys `'xmin'`, `'xmax'`, 
            `'ymin'`, `'ymax'`, `'zmin'`, `'zmax'`, `'datamin'`, `'datamax'`.  A 1D
            Viewer will only use `'xmin'` and `'xmax'`, a 2D viewer will also
            use `'ymin'` and `'ymax'`, and so on.  All viewers will use
            `'datamin'` and `'datamax'`.  Any limit set to a (default) value of
            `None` will autoscale.
          - `title`: displayed at the top of the Viewer window
          - `xlog`: set `True` to give logarithmic scaling of the x axis
          - `ylog`: set `True` to give logarithmic scaling of the y axis
          - `style`: the Gist style file to use

        """
        _GistViewer.__init__(self, vars = vars, limits = limits, title = title)
	self.xlog = xlog
	self.ylog = ylog
	self.style = style
        
    def _getLimit(self, key):
        subs = {'ymin': 'datamin', 'ymax': 'datamax'}
        
        if subs.has_key(key):
            limit = _GistViewer._getLimit(self, key = subs[key])
            if limit == 'e':
                limit = _GistViewer._getLimit(self, key = key)
        else:
            limit = _GistViewer._getLimit(self, key = key)
            if limit == 'e':
                subs = {'datamin': 'ymin', 'datamax': 'ymax'}
                limit = _GistViewer._getLimit(self, key = key)
            
        return limit

    def _getArrays(self):
	arrays = []
        
	for var in self.vars:
            arrays.append((Numeric.array(var), Numeric.array(var.getMesh().getCellCenters()[:,0])))
            
	return arrays
	
    def _plotArrays(self):
	import gist
	
	for array in self._getArrays():
            gist.plg(*array)
            
	gist.logxy(self.xlog, self.ylog)

    def plot(self):
        """
        Plot the `CellVariable` or list of `CellVariables` as a y vs x plot.
        """
	import gist

	gist.window(self.id, wait = 1, style = self.style)
	gist.pltitle(self.title)
	gist.animate(1)

        if self.limits != None:
            gist.limits(self._getLimit('xmin'), self._getLimit('xmax'), self._getLimit('datamin'), self._getLimit('datamax'))
	    
	self._plotArrays()
	    
	gist.fma()