import math

def generate_rd_xml(filename="rd_structure.xml"):
    # Vertices of Rhombic Dodecahedron
    # 6 "Axis" vertices (Octahedron tips)
    # 8 "Corner" vertices (Cube corners)
    
    # Scale
    s = 0.2  # Overall size scale
    
    # Axis Vertices (Distance 1.0 * s) - actually distance 1.0 is standard, let's allow scale
    axis_verts = [
        (s, 0, 0), (-s, 0, 0),
        (0, s, 0), (0, -s, 0),
        (0, 0, s), (0, 0, -s)
    ]
    
    # Corner Vertices (Distance 0.5 from planes? No, simple coordinates)
    # In standard canonical form, if axis are at +/- 1, corners are at +/- 0.5.
    corner_verts = []
    for x in [-0.5, 0.5]:
        for y in [-0.5, 0.5]:
            for z in [-0.5, 0.5]:
                corner_verts.append((x*s*2, y*s*2, z*s*2)) # Wait, if Axis is 1, corner is 0.5. So if Axis is s, corner is s*0.5
    
    # Let's re-verify logic.
    # Unit Radius RD:
    # Axis points: (+/- 1, 0, 0)
    # Cube points: (+/- 0.5, +/- 0.5, +/- 0.5)
    # Connectivity: Each Axis point connects to the 4 nearest Cube points.
    
    # Recalculate with 's' as the 1.0 unit
    axis_coords = [
        (s, 0, 0), (-s, 0, 0),
        (0, s, 0), (0, -s, 0),
        (0, 0, s), (0, 0, -s)
    ]
    
    cube_coords = []
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                # 0.5 * s
                cube_coords.append((x * 0.5 * s, y * 0.5 * s, z * 0.5 * s))
                
    # Generate Edges
    # Edge connects Axis to Cube if they are "close"
    edges = []
    
    # Combined List of Nodes (for rendering nodes loop)
    all_nodes = axis_coords + cube_coords
    
    # User Request: "keep the cube-octahedron edges as structs and the rhombic doodecahedron edges as tensors"
    # User Request: "make the cube green and the octahedron blue"
    
    cube_structs = []  # Green
    octa_structs = []  # Blue
    tensors = []       # Tensors (Rhombic Dodecahedron edges)
    
    # 1. Cube Edges (Green Structs)
    cube_edge_len = s
    cube_tolerance = 0.01 * s
    for i in range(len(cube_coords)):
        for j in range(i + 1, len(cube_coords)):
            p1 = cube_coords[i]
            p2 = cube_coords[j]
            dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
            if abs(dist - cube_edge_len) < cube_tolerance:
                cube_structs.append((p1, p2))

    # 2. Octahedron Edges (Blue Structs)
    octa_edge_len = math.sqrt(2) * s
    octa_tolerance = 0.01 * s
    for i in range(len(axis_coords)):
        for j in range(i + 1, len(axis_coords)):
            p1 = axis_coords[i]
            p2 = axis_coords[j]
            dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
            if abs(dist - octa_edge_len) < octa_tolerance:
                octa_structs.append((p1, p2))

    # 3. Rhombic Dodecahedron Edges (Tensors)
    rd_edge_len = math.sqrt(0.75) * s
    rd_tolerance = 0.01 * s
    for i in range(len(all_nodes)):
        for j in range(i + 1, len(all_nodes)):
            p1 = all_nodes[i]
            p2 = all_nodes[j]
            dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
            if abs(dist - rd_edge_len) < rd_tolerance:
                tensors.append((p1, p2))

    # XML Content
    xml_header = """<mujocoinclude>
    <body name="rd_tensegrity" pos="0 0 1.0">
        <freejoint/>
        <!-- User Request: "replace the sphefe collision for a real colission system" -->
        <!-- Removed central sphere. Collision will be handled by individual geoms. -->
""".format(s * 1.0)
    
    xml_body = ""
    
    # Render Nodes (Spheres)
    # Enable collision (default is colliding if no class specified, or we can be explicit)
    for i, v in enumerate(all_nodes):
        xml_body += '        <body name="node_{}" pos="{} {} {}">\n'.format(i, v[0], v[1], v[2])
        # condim=3 for friction, friction=1 for grip
        xml_body += '            <geom type="sphere" size="{}" rgba="0.8 0.8 0.8 1" mass="0.01" condim="3" friction="1 0.005 0.0001"/>\n'.format(s*0.06)
        xml_body += '        </body>\n'
        
    # Render Cube Structs (Green)
    for index, (start, end) in enumerate(cube_structs):
        xml_body += '        <body name="cube_struct_{}" pos="0 0 0">\n'.format(index)
        xml_body += '            <geom type="capsule" size="{}" fromto="{} {} {} {} {} {}" rgba="0 1 0 1" mass="0.05" condim="3"/>\n'.format(
            s*0.04, start[0], start[1], start[2], end[0], end[1], end[2]
        )
        xml_body += '        </body>\n'

    # Render Octahedron Structs (Blue)
    for index, (start, end) in enumerate(octa_structs):
        xml_body += '        <body name="octa_struct_{}" pos="0 0 0">\n'.format(index)
        xml_body += '            <geom type="capsule" size="{}" fromto="{} {} {} {} {} {}" rgba="0 0 1 1" mass="0.05" condim="3"/>\n'.format(
            s*0.04, start[0], start[1], start[2], end[0], end[1], end[2]
        )
        xml_body += '        </body>\n'

    # Render Tensors (Thin Capsules - Red/Orange)
    for index, (start, end) in enumerate(tensors):
        xml_body += '        <body name="tensor_{}" pos="0 0 0">\n'.format(index)
        xml_body += '            <geom type="capsule" size="{}" fromto="{} {} {} {} {} {}" rgba="1 0.4 0.2 1" mass="0.01" condim="3"/>\n'.format(
            s*0.015, start[0], start[1], start[2], end[0], end[1], end[2]
        )
        xml_body += '        </body>\n'

    xml_footer = """    </body>
</mujocoinclude>
"""
    
    with open(filename, "w") as f:
        f.write(xml_header + xml_body + xml_footer)
    
    print(f"Generated {filename} with {len(edges)} struts.")

if __name__ == "__main__":
    generate_rd_xml("public/mujoco/menagerie/unitree_g1/rd_structure.xml")
