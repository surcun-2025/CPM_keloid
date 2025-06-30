from cc3d import CompuCellSetup

from .clusterMitosisSteppables import VolumeParamSteppable
CompuCellSetup.register_steppable(steppable=VolumeParamSteppable(frequency=1))

from .clusterMitosisSteppables import ElongationFlexSteppable
CompuCellSetup.register_steppable(steppable=ElongationFlexSteppable(frequency=1))

from .clusterMitosisSteppables import NeighborTrackerPrinterSteppable
CompuCellSetup.register_steppable(steppable=NeighborTrackerPrinterSteppable(frequency=1))

from .clusterMitosisSteppables import Motility2DSteppable
CompuCellSetup.register_steppable(steppable=Motility2DSteppable(frequency=1))

from .clusterMitosisSteppables import ScreenshotSteppable
CompuCellSetup.register_steppable(steppable=ScreenshotSteppable(frequency=1))

CompuCellSetup.run()


