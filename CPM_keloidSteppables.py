from cc3d.core.PySteppables import *
from random import uniform
import numpy as np
import numpy.linalg as nalg
import math


class ScreenshotSteppable(SteppableBasePy):
	def __init__(self, frequency=10):
		SteppableBasePy.__init__(self, frequency)

	def step(self, mcs):
		if mcs in [0,799]:
			self.request_screenshot(mcs=mcs, screenshot_label='Cell_Field_CellField_2D_XY_0')



class PixelTrackerSteppable(SteppableBasePy):
	def __init__(self, frequency=1):
		SteppableBasePy.__init__(self, frequency)

	def step(self, mcs):
		if mcs==0:
			output_dir = self.output_dir
			if output_dir is not None:
				output_path = Path(output_dir).joinpath('step_' + str(mcs).zfill(3) + '.dat')
				with open(output_path, 'w') as fout:
					for cell in self.cell_list:
						pixel_list = self.get_cell_pixel_list(cell)



class Motility2DSteppable(SteppableBasePy):

	def __init__(self,frequency=1):

		SteppableBasePy.__init__(self,frequency)

	def step(self,mcs):

		for cell in self.cell_list:
			if (cell.type==1):
				neighbor_list = self.get_cell_neighbor_data_list(cell)
				for neighbor, common_surface_area in neighbor_list:
					if neighbor:				
						Sij=float(neighbor_list.commonSurfaceAreaWithCellTypes(cell_type_list=[1, 2]))
						cell.biasVecX=int(round(100*( 1-int(Sij/200) )*(1+ uniform(-1, 1))))
						cell.biasVecY=int(round(100*( 1-int(Sij/200) )*(1+ uniform(-1, 1))))
					else:
						cell.biasVecX=int(round(100*(1+ uniform(-1, 1))))
						cell.biasVecY=int(round(100*(1+ uniform(-1, 1))))


class NeighborTrackerPrinterSteppable(SteppableBasePy):
	def __init__(self, frequency=1):
		SteppableBasePy.__init__(self, frequency)

	def step(self, mcs):

		for cell in self.cell_list:
			neighbor_list = self.get_cell_neighbor_data_list(cell)
			neighbor_dependent = self.get_xml_element('neighbor_dependent')

			for neighbor, common_surface_area in neighbor_list:
				if neighbor:
					neighbor_dependent.cdata=-100+2.0*float(neighbor_list.commonSurfaceAreaWithCellTypes(cell_type_list=[1, 2]))*float(neighbor_list.commonSurfaceAreaWithCellTypes(cell_type_list=[1, 2])) 



class VolumeParamSteppable(SteppableBasePy):
	def __init__(self, frequency=1):
		SteppableBasePy.__init__(self, frequency)

	def start(self):
		for cell in self.cell_list:
			if (cell.type==1):
				initial_volume = int(np.random.gamma(3.101, scale=692.1, size=1)) #Keloid
				#initial_volume = int(np.random.gamma(4.314, scale=508.8, size=1)) #Healthy
				cell.targetVolume = initial_volume
				cell.lambdaVolume = 1.0

	def step(self, mcs):
		maxshared=200
		minsurf=600
		maxsurf=5000
		for cell in self.cell_list:
			if (cell.type==1):
				neighbor_list = self.get_cell_neighbor_data_list(cell)
			
				for neighbor, common_surface_area in neighbor_list:
					if neighbor:				
						Sij=float(neighbor_list.commonSurfaceAreaWithCellTypes(cell_type_list=[1, 2]))
						if Sij>maxshared:
							cell.targetVolume = minsurf
							
						elif Sij==0:
							cell.targetVolume = maxsurf
							
						else:
							cell.targetVolume = int(round( ( ((minsurf-maxsurf)/maxshared)*Sij+maxsurf ) )	)						
							

class ElongationFlexSteppable(SteppableBasePy):
	def __init__(self, frequency=1):
		SteppableBasePy.__init__(self, frequency)

	def start(self):
		for cell in self.cell_list:
			if cell.type == 1:
				targetLength= 160
				self.lengthConstraintPlugin.setLengthConstraintData(cell,16,targetLength)
				cell.connectivityOn = True

	def step(self, mcs):
		for cell in self.cell_list:
			if (cell.type==1):
				neighbor_list = self.get_cell_neighbor_data_list(cell)
			
				for neighbor, common_surface_area in neighbor_list:
					if neighbor:				
						Sij=float(neighbor_list.commonSurfaceAreaWithCellTypes(cell_type_list=[1, 2]))
						maxshared=200
						minlength=50
						maxlength=250
						if Sij>maxshared:
							self.lengthConstraintPlugin.setLengthConstraintData(cell,16,minlength)
						elif Sij==0:
							self.lengthConstraintPlugin.setLengthConstraintData(cell,16,maxlength)
						else:
							self.lengthConstraintPlugin.setLengthConstraintData(cell,16,int(round( ( ((minlength-maxlength)/maxshared)*Sij+maxlength ) ) ) )
							 
