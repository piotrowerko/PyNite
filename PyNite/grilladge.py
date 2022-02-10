import numpy as np
import math

from FEModel3D import FEModel3D
import Visualization as vis

class Grilladge(FEModel3D):
    def __init__(self, no_of_beams=2, beam_spacing=8, span_data=(2, 28, 28), canti_l=2.5, skew=90): 
        #  https://www.youtube.com/watch?v=MBbVq_FIYDA
        super().__init__()
        self.no_of_beams = no_of_beams
        self.beam_spacing = beam_spacing
        self.span_data = span_data
        self.skew = skew
        self.canti_l = canti_l
 
    def _z_coors_in_g1(self, discr=20):
        """returns numpy array of z coordinates in first girder"""
        if isinstance(discr, int) == False:
            raise TypeError(f"discr must be an integer!")
        z_coors_in_g1 = np.array([0.0])
        for j in range(self.span_data[0]):
            z1_spacing = self.span_data[j+1] / discr
            if j == 0:
                z_local = 0
            else:
                z_local = sum(self.span_data[1:j+1])
            for i in range(discr):
                z_local += z1_spacing
                z_coors_in_g1 = np.append(z_coors_in_g1, [z_local])
        return np.round(z_coors_in_g1, decimals=3)
    
    def _z_coors_in_g(self, discr=20, gird_no=2):
        """returns numpy array of z coordinates in given girder"""
        if isinstance(discr, int) == False:
            raise TypeError(f"discr must be an integer!")
        if isinstance(gird_no, int) == False:
            raise TypeError(f"gird_no must be an integer!")
        if gird_no == 1 or self.skew == 90:
            z_coors_in_g = self._z_coors_in_g1(discr)
        else:
            rad_skew = math.radians(self.skew)  # skew angle in radians
            z_offset = (gird_no - 1) * self.beam_spacing * (1 / math.tan(rad_skew))
            z_coors_in_g = self._z_coors_in_g1() + z_offset
        return np.round(z_coors_in_g, decimals=3)

    def _z_coors_of_cantitip(self, discr=20, edge=1):
        """returns numpy array of z cooridnates of cantilever tips"""
        if isinstance(discr, int) == False:
            raise TypeError(f"discr must be an integer!")
        if isinstance(edge, int) == False:
            raise TypeError(f"edge must be an integer!")
        if self.skew == 90:
            _z_coors_of_cantitip = self._z_coors_in_g1(discr)
        elif edge == 1:
            rad_skew = math.radians(self.skew)  # skew angle in radians
            z_offset = self.canti_l * (1 / math.tan(rad_skew))
            z_coors_of_cantitip = self._z_coors_in_g1(discr) - z_offset
        else:
            rad_skew = math.radians(self.skew) 
            z_offset = (self.canti_l + (self.no_of_beams -1) * self.beam_spacing) \
                * (1 / math.tan(rad_skew))
            z_coors_of_cantitip = self._z_coors_in_g1(discr) + z_offset
        return np.round(z_coors_of_cantitip, decimals=3)
        
        
    def _x_coors_in_g1(self, discr=20):
        """returns numpy array of x coordinates in first girder"""
        if isinstance(discr, int) == False:
            raise TypeError(f"discr must be an integer!")
        x_coors_in_g1 = np.array([0.0])
        for j in range(self.span_data[0]):
            x_local = 0.0
            for i in range(discr):
                x_coors_in_g1 = np.append(x_coors_in_g1, [x_local])
        return np.round(x_coors_in_g1, decimals=3)
    
    def _x_coors_in_g(self, discr=20, gird_no=2):
        """returns numpy array of x coordinates in given girder"""
        if isinstance(discr, int) == False:
            raise TypeError(f"discr must be an integer!")
        x_coors_in_g = self._x_coors_in_g1(discr) + (gird_no-1) * self.beam_spacing
        return np.round(x_coors_in_g, decimals=3)
    
    def _x_coors_of_cantitip(self, discr=20, edge=1):
        """returns numpy array of x cooridnates of cantilever tips"""
        if isinstance(discr, int) == False:
            raise TypeError(f"discr must be an integer!")
        if isinstance(edge, int) == False:
            raise TypeError(f"edge must be an integer!")
        if edge == 1:
            x_coors_of_cantitip = self._x_coors_in_g1(discr) - self.canti_l
        else:
            x_coors_of_cantitip = self._x_coors_in_g1(discr) \
                + self.canti_l + (self.no_of_beams-1) * self.beam_spacing
        return np.round(x_coors_of_cantitip, decimals=3)
    
    
        
        

    
    def _nodes_coor(self, discr=20):
        """
        Parameters
        ----------
        discr : integer
            number of desired finite elements in each girder in each span.
        Raises
        ------
        TypeError
            Occurs when the 'discr' is not integer.
        Returns
        -------
        coordinates of nodes
        """
        pass
        
    
    def grilladge_nodes(self):
        """returns nodes of grilladge"""
        return self.Nodes


def main():
    wd185 = Grilladge(no_of_beams=2, beam_spacing=8, span_data=(2, 30, 30), skew=80)
    print(wd185._z_coors_of_cantitip(discr=10, edge=2))
    print(wd185._z_coors_in_g(discr=10, gird_no=2))
    print(wd185._x_coors_in_g1(discr=10))
    print(wd185._x_coors_in_g(discr=10, gird_no=2))
    print(wd185._x_coors_of_cantitip(discr=10, edge=2))

if __name__ == '__main__':
    main()