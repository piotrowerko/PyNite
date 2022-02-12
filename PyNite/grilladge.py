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
            z_coors_in_g = self._z_coors_in_g1(discr) + z_offset
        return np.round(z_coors_in_g, decimals=3)

    def _z_coors_of_cantitip(self, discr=20, edge=1):
        """returns numpy array of z cooridnates of cantilever tips"""
        if isinstance(discr, int) == False:
            raise TypeError(f"discr must be an integer!")
        if isinstance(edge, int) == False:
            raise TypeError(f"edge must be an integer!")
        if self.skew == 90:
            z_coors_of_cantitip = self._z_coors_in_g1(discr)
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
    
    def _z_coors_cross_m(self, discr=20, x_dist=4.0):
        """returns numpy array of z cooridnates of lingitudal arbitrary line (z-line) governing nodes"""
        if isinstance(discr, int) == False:
            raise TypeError(f"discr must be an integer!")
        if isinstance(x_dist, float) == False and isinstance(x_dist, int) == False:
            raise TypeError(f"x_dist must be a float or integer!")
        if self.skew == 90 or x_dist == 0.0:
            _z_coors_cross_m = self._z_coors_in_g1(discr)
        else:
            rad_skew = math.radians(self.skew) 
            z_offset = x_dist * (1 / math.tan(rad_skew))
            _z_coors_cross_m = self._z_coors_in_g1(discr) + z_offset
        return np.round(_z_coors_cross_m, decimals=3)
    
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
    
    def _x_coors_cross_m(self, discr=20, x_dist=4.0):
        """returns numpy array of x cooridnates of lingitudal arbitrary line (z-line) governing nodes"""
        if isinstance(discr, int) == False:
            raise TypeError(f"discr must be an integer!")
        if isinstance(x_dist, float) == False and isinstance(x_dist, int) == False:
            raise TypeError(f"x_dist must be a float or integer!")
        x_coors_cross_m = self._x_coors_in_g1(discr) + x_dist
        return np.round(x_coors_cross_m, decimals=3)
        
    
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
    

    def _nodes_coor_g(self, discr=20):
        """
        Aggregartes all nodes coordinates of girders
        
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
        coordinates of nodes in numpy array
        """
        if isinstance(discr, int) == False:
            raise TypeError(f"discr must be an integer!")
        
        z_coors_g = np.array([])
        x_coors_g = np.array([])
        for i in range(self.no_of_beams):
            z_in_g = self._z_coors_in_g(discr=discr, gird_no=i+1)
            z_coors_g = np.append(z_coors_g, [z_in_g])
            x_in_g = self._x_coors_in_g(discr, i+1)
            x_coors_g = np.append(x_coors_g, [x_in_g])
        
        y_coors_g = np.zeros(self.no_of_beams * self.span_data[0] * discr + self.no_of_beams)
        # self._z_coors_of_cantitip(self, discr=20, edge=1)
        # self._x_coors_in_g(self, discr=20, gird_no=2)
        # self._x_coors_of_cantitip(self, discr=20, edge=1)
        
        
        all_nodes_coor_g = np.stack((z_coors_g, x_coors_g, y_coors_g))
        print(self._z_coors_cross_m(discr))
                
        return all_nodes_coor_g
    
    def _gen_coor_array(self, discr, x_dist_array):
        """generates three numpy arraayes with z, x and y coordinates"""
        z_coors = np.array([])
        x_coors = np.array([])
        y_coors = np.array([])
        for x_dist in x_dist_array:
            z_in_g = self._z_coors_cross_m(discr=discr, x_dist=x_dist)
            z_coors = np.append(z_coors, [z_in_g])
            x_in_g = self._x_coors_cross_m(discr, x_dist=x_dist)
            x_coors = np.append(x_coors, [x_in_g])
        y_coors = np.zeros(len(x_dist_array) * self.span_data[0] * discr + len(x_dist_array))
        return z_coors, x_coors, y_coors
    

    def _nodes_coor(self, discr=20, tr_discr=3):
        """
        Aggregartes all nodes coordinates of girders
        
        Parameters
        ----------
        discr : integer
            number of desired finite elements in each girder in each span.
        tr_discr : integer
            number of desired finite elements in each cross member between girders
        Raises
        ------
        TypeError
            Occurs when the 'discr' is not integer.
        Returns
        -------
        coordinates of girders, cintilevel tips, trnsers memebers nodes in numpy array
        """
        if isinstance(discr, int) == False or isinstance(tr_discr, int) == False:
            raise TypeError(f"discr and tr_discr must be an integer!")
        #  generating girder nodes coordinates:
        x_dist_arr_g = np.array([])
        for i in range(self.no_of_beams):
            x_dist_arr_g = np.append(x_dist_arr_g, [i * self.beam_spacing])
        z_coors_g, x_coors_g, y_coors_g = self._gen_coor_array(discr, x_dist_arr_g)
        all_nodes_coor_g = np.stack((z_coors_g, x_coors_g, y_coors_g))
        
        #  generating cantilevel nodes coordinates:
        x_dist_arr_c = np.array([- self.canti_l, self.canti_l + (self.no_of_beams-1) * self.beam_spacing])
        z_coors_c, x_coors_c, y_coors_c = self._gen_coor_array(discr, x_dist_arr_c)
        all_nodes_coor_c = np.stack((z_coors_c, x_coors_c, y_coors_c))
        
        #  generating cross member nodes coordinates:
        x_dist_arr_cr = np.array([])
        for i in range(self.no_of_beams-1):
            for j in range(tr_discr-1):
                x_dist_arr_cr = np.append(x_dist_arr_cr, [(j+1) * self.beam_spacing / tr_discr])
        print(x_dist_arr_cr)
        z_coors_cr, x_coors_cr, y_coors_cr = self._gen_coor_array(discr, x_dist_arr_cr)
        all_nodes_coor_cr = np.stack((z_coors_cr, x_coors_cr, y_coors_cr))
        return all_nodes_coor_g, all_nodes_coor_c, all_nodes_coor_cr

    def grilladge_nodes(self):
        """returns nodes of grilladge"""
        return self.Nodes


def main():
    wd185 = Grilladge(no_of_beams=2, beam_spacing=8, span_data=(2, 30, 30), skew=80)
    # print(wd185._z_coors_of_cantitip(discr=10, edge=2))
    # print(wd185._z_coors_in_g(discr=10, gird_no=2))
    # print(wd185._x_coors_in_g1(discr=10))
    # print(wd185._x_coors_in_g(discr=10, gird_no=2))
    print(wd185._nodes_coor(discr=2, tr_discr=3))
    
if __name__ == '__main__':
    main()