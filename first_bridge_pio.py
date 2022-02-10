# Import 'FEModel3D' and 'Visualization' from 'PyNite'
from PyNite.FEModel3D import FEModel3D
from PyNite import Visualization

# Create a new model
frame = FEModel3D()

# Define the nodes
frame.add_node('N1', 0, 0, 0)
frame.add_node('N2', 0, 0, 15)
frame.add_node('N3', 0, 0, 30)
frame.add_node('N4', -10, 0, 30)
frame.add_node('N5', -10, 0, 15)
frame.add_node('N6', -10, 0, 0)

# Define the supports
frame.def_support('N1', True, True, True, True, True, True)
frame.def_support('N3', True, True, True, True, True, True)
frame.def_support('N4', True, True, True, True, True, True)
frame.def_support('N6', True, True, True, True, True, True)

# Create members (all members will have the same properties in this example)
J = 0.2
Iy = 0.5
Iz = 0.5
E = 35000000
G = 16000000
A = 1.0

frame.add_member('M1', 'N1', 'N2', E, G, Iy, Iz, J, A)
frame.add_member('M2', 'N2', 'N3', E, G, Iy, Iz, J, A)
frame.add_member('M3', 'N3', 'N4', E, G, Iy, Iz, J, A)
frame.add_member('M4', 'N4', 'N5', E, G, Iy, Iz, J, A)
frame.add_member('M5', 'N5', 'N6', E, G, Iy, Iz, J, A)
frame.add_member('M6', 'N6', 'N1', E, G, Iy, Iz, J, A)
frame.add_member('M7', 'N5', 'N2', E, G, Iy, Iz, J, A)

# Add nodal loads
frame.add_node_load('N2', 'FY', -400)
frame.add_node_load('N5', 'FY', -400)

# Analyze the model
frame.analyze(check_statics=True)

# Render the deformed shape
Visualization.render_model(frame, deformed_shape=True, deformed_scale=200, render_loads=True)

# Print the node 1 displacements
print('Node 1 deformations:')
print('Calculated values: ', frame.Nodes['N2'].DX, frame.Nodes['N2'].DY, frame.Nodes['N2'].DZ, frame.Nodes['N2'].RX, frame.Nodes['N2'].RY, frame.Nodes['N2'].RZ)
# print('Expected values: ', 7.098e-5, -0.014, -2.352e-3, -3.996e-3, 1.78e-5, -1.033e-4)