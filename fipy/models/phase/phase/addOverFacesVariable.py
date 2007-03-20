#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "tools.py"
 #                                    created: 11/12/03 {10:39:23 AM} 
 #                                last update: 9/3/04 {10:43:04 PM}
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
 # 
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-12 JEG 1.0 original
 # ###################################################################
 ##

import Numeric

import fipy.tools.array
import fipy.tools.inline.inline as inline
from fipy.variables.cellVariable import CellVariable
import fipy.variables.cellVariable 

class AddOverFacesVariable(CellVariable):
    def __init__(self,
                 faceGradient = None,
                 faceVariable = None):
    

        CellVariable.__init__(self, faceVariable.getMesh(), hasOld = 0)
    
        self.faceGradient = self.requires(faceGradient)
        self.faceVariable = self.requires(faceVariable)

    def _calcValuePy(self):

        contributions = fipy.tools.array.sum(self.mesh.getAreaProjections() * self.faceGradient[:],1)   
        contributions = contributions * self.faceVariable[:]
##        contributions[len(self.mesh.getInteriorFaces()):] = 0.
        extFaceIDs = self.mesh.getExteriorFaceIDs()

        fipy.tools.array.put(contributions, extFaceIDs, Numeric.zeros(Numeric.shape(extFaceIDs), 'd'))
        ids = self.mesh.getCellFaceIDs()
        
        contributions = fipy.tools.array.take(contributions[:], ids.flat)

        NCells = self.mesh.getNumberOfCells()

        contributions = fipy.tools.array.reshape(contributions,(NCells,-1))
        
        orientations = fipy.tools.array.reshape(self.mesh.getCellFaceOrientations(),(NCells,-1))

        orientations = Numeric.array(orientations)
        
        self.value = fipy.tools.array.sum(orientations * contributions,1) / self.mesh.getCellVolumes()

        
    def _calcValueInline(self):

        NCells = self.mesh.getNumberOfCells()
	ids = self.mesh.getCellFaceIDs()
##         ids = Numeric.reshape(ids,(NCells,self.mesh.getMaxFacesPerCell()))

        inline.runInline("""
        int i;
        
        for(i = 0; i < numberOfInteriorFaces; i++)
          {
            int j;
            int faceID = interiorFaceIDs(i);
            
            for(j = 0; j < numberOfDimensions; j++)
              {
                contributions(faceID) += areaProjections(faceID, j) * faceGradient(faceID, j);
              }
            contributions(faceID) = contributions(faceID) * faceVariable(faceID);
          }
        
        for(i = 0; i < numberOfCells; i++)
          {
          int j;
          value(i) = 0.;
          for(j = 0; j < numberOfCellFaces; j++)
            {
              value(i) += orientations(i,j) * contributions(ids(i,j));
            }
            value(i) = value(i) / cellVolume(i);
          }
          """,numberOfInteriorFaces = len(self.mesh.getInteriorFaceIDs()),
              numberOfDimensions = self.mesh.getDim(),
              numberOfCellFaces = self.mesh.getMaxFacesPerCell(),
              numberOfCells = NCells,
              interiorFaceIDs = self.mesh.getInteriorFaceIDs(),
              contributions =  Numeric.zeros((self.mesh.getNumberOfFaces()),'d'),
              areaProjections = Numeric.array(self.mesh.getAreaProjections()),
              faceGradient = self.faceGradient.getNumericValue()[:],
              faceVariable = self.faceVariable.getNumericValue()[:],
              ids = Numeric.array(ids),
              value = self._getArray(),
              orientations = Numeric.array(self.mesh.getCellFaceOrientations()),
              cellVolume = Numeric.array(self.mesh.getCellVolumes()))

    def _calcValue(self):

        inline.optionalInline(self._calcValueInline, self._calcValuePy)



    

