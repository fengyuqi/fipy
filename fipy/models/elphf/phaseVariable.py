## -*-Pyth-*-
 # ###################################################################
 #  PFM - Python-based phase field solver
 # 
 #  FILE: "phaseVariable.py"
 #                                    created: 12/18/03 {12:18:05 AM} 
 #                                last update: 12/27/03 {5:25:32 PM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
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
 # ###################################################################
 ##

from variables.cellVariable import CellVariable

class PhaseVariable(CellVariable):
    def __init__(self, mesh, name = '', value=0., hasOld = 1):
	CellVariable.__init__(self, mesh, name, value, hasOld = hasOld)
	self.p = self**3 * (6. * self**2 - 15. * self + 10.)
	self.g = (self * (1. - self))**2
	
    def get_p(self):
	return self.p
	
    def get_g(self):
	return self.g

