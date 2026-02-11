import math

def generate_rd_xml(filename="rd_structure.xml"):
    # Vertices of Rhombic Dodecahedron
    # 6 "Axis" vertices (Octahedron tips)
    # 8 "Corner" vertices (Cube corners)
    
    # Scale
    s = 1.2  # Overall size scale (Human Size: ~2.4m span)
    z_offset = 2.0 # Height off ground
    
    # Axis Vertices (Distance 1.0 * s)
    axis_verts = [
        (s, 0, 0), (-s, 0, 0),
        (0, s, 0), (0, -s, 0),
        (0, 0, s), (0, 0, -s)
    ]

    # --- DYNAMIC PHYSICS IMPLEMENTATION ---
    
    # Defaults
    xml_header = """<mujoco>
    <option timestep="0.0005" integrator="implicit" gravity="0 0 -9.81"/>
    
    <default>
        <geom rgba="0.8 0.6 0.4 1" contype="1" conaffinity="1" condim="3" solref="0.005 1" solimp="0.9 0.95 0.001" margin="0.001"/>
        <site size="0.01" rgba="1 0 0 1" group="3"/>
        <joint damping="0.5" armature="0.02"/>
        <tendon width="0.02" rgba="0.2 0.6 1 1" limited="false"/>
        <muscle ctrllimited="true" ctrlrange="0 1" scale="5"/>
    </default>

    <visual>
        <rgba haze="0.15 0.25 0.35 1"/>
        <quality shadowsize="2048"/>
        <map stiffness="700" shadowscale="0.5" fogstart="10" fogend="15" zfar="40" haze="0.3"/>
    </visual>
    
    <worldbody>
        <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1" castshadow="false"/>
"""

    # --- 1. GYROSCOPE ASSEMBLY (ROOT) ---
    
    # Defaults for geometry
    th_struct = s * 0.015 # Thinner structure
    
    xml_body = ""
    
    # Helper for Ring Geoms

    def get_ring_geoms(radius, color, axis='z', phase=0):
        g = ""
        seg = 16 # Smoother
        gap = 0.2
        # Two Arcs
        for start in [gap, math.pi + gap]:
            for i in range(seg):
                a1 = start + i * (math.pi - 2*gap)/seg + phase
                a2 = start + (i+1) * (math.pi - 2*gap)/seg + phase
                
                c1, s1 = math.cos(a1), math.sin(a1)
                c2, s2 = math.cos(a2), math.sin(a2)
                
                if axis == 'z':
                    p1 = (radius*c1, radius*s1, 0)
                    p2 = (radius*c2, radius*s2, 0)
                elif axis == 'y':
                    p1 = (radius*c1, 0, radius*s1)
                    p2 = (radius*c2, 0, radius*s2)
                elif axis == 'x':
                    p1 = (0, radius*c1, radius*s1)
                    p2 = (0, radius*c2, radius*s2)
                else:
                    p1 = (radius*c1, radius*s1, 0)
                    p2 = (radius*c2, radius*s2, 0)
                    
                g += '        <geom type="capsule" fromto="{:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}" size="{}" rgba="{}" mass="0.1"/>\n'.format(
                    p1[0], p1[1], p1[2], p2[0], p2[1], p2[2], th_struct, color
                )
        return g

    # --- 1. GYROSCOPE (Central Structure) ---
    # ROOT BODY: Floating Base for the Gyroscope
    xml_body += '    <body name="gyro_root" pos="0 0 {}">\n'.format(z_offset)
    xml_body += '        <freejoint/>\n'
    # Root Mass for Stability (100kg)
    xml_body += '        <geom type="sphere" size="0.2" mass="100.0" rgba="0.5 0.5 0.5 0.3" contype="0" conaffinity="0"/>\n'
    
    # ---------------------------------------------------------
    # OUTER RING (Gold, YZ Plane) - Y-Axis Joint
    # ---------------------------------------------------------
    xml_body += '        <body name="gyro_outer" pos="0 0 0">\n'
    xml_body += '            <joint name="motor_outer" axis="0 1 0"/>\n' # Y-Axis Pivot
    
    # Visual: Gold Ring (Radius 0.55s)
    xml_body += get_ring_geoms(s*0.55, "1 0.8 0 1", axis='x', phase=math.pi/2)

    # Payload: Axis Nodes 2 and 3 (Y-Axis: 0, +/-s, 0)
    # Node 2
    xml_body += '            <site name="node_2" pos="0 {} 0"/>\n'.format(s)
    xml_body += '            <geom type="sphere" pos="0 {} 0" size="{}" rgba="0.2 0.8 0.2 1" mass="0.1"/>\n'.format(s, s*0.06)
    xml_body += '            <geom type="capsule" fromto="0 {} 0 0 {} 0" size="{}" rgba="1 0.8 0 1" mass="0.01"/>\n'.format(s*0.55, s, th_struct)
    
    # Node 3
    xml_body += '            <site name="node_3" pos="0 {} 0"/>\n'.format(-s)
    xml_body += '            <geom type="sphere" pos="0 {} 0" size="{}" rgba="0.2 0.8 0.2 1" mass="0.1"/>\n'.format(-s, s*0.06)
    xml_body += '            <geom type="capsule" fromto="0 {} 0 0 {} 0" size="{}" rgba="1 0.8 0 1" mass="0.01"/>\n'.format(-s*0.55, -s, th_struct)

    # ---------------------------------------------------------
    # MIDDLE RING (Silver, XY Plane) - X-Axis Joint
    # ---------------------------------------------------------
    xml_body += '            <body name="gyro_middle" pos="0 0 0">\n'
    xml_body += '                <joint name="motor_middle" axis="1 0 0"/>\n' # X-Axis Pivot
    
    # Visual: Silver Ring (Radius 0.50s)
    xml_body += get_ring_geoms(s*0.50, "0.8 0.8 0.8 1", axis='z', phase=math.pi/2)

    # Payload: Axis Nodes 0 and 1 (X-Axis: +/-s, 0, 0)
    # Node 0
    xml_body += '                <site name="node_0" pos="{} 0 0"/>\n'.format(s)
    xml_body += '                <geom type="sphere" pos="{} 0 0" size="{}" rgba="0.2 0.8 0.2 1" mass="0.1"/>\n'.format(s, s*0.06)
    xml_body += '                <geom type="capsule" fromto="{} 0 0 {} 0 0" size="{}" rgba="0.8 0.8 0.8 1" mass="0.01"/>\n'.format(s*0.50, s, th_struct)

    # Node 1
    xml_body += '                <site name="node_1" pos="{} 0 0"/>\n'.format(-s)
    xml_body += '                <geom type="sphere" pos="{} 0 0" size="{}" rgba="0.2 0.8 0.2 1" mass="0.1"/>\n'.format(-s, s*0.06)
    xml_body += '                <geom type="capsule" fromto="{} 0 0 {} 0 0" size="{}" rgba="0.8 0.8 0.8 1" mass="0.01"/>\n'.format(-s*0.50, -s, th_struct)

    # ---------------------------------------------------------
    # INNER RING (Bronze, XZ Plane) - Z-Axis Joint
    # ---------------------------------------------------------
    xml_body += '                <body name="gyro_inner" pos="0 0 0">\n'
    xml_body += '                    <joint name="motor_inner" axis="0 0 1"/>\n' # Z-Axis Pivot
    
    # Visual: Bronze Ring (Radius 0.45s)
    xml_body += get_ring_geoms(s*0.45, "0.8 0.5 0.2 1", axis='y')

    # Payload: Axis Nodes 4 and 5 (Z-Axis: 0, 0, +/-s)
    # Node 4
    xml_body += '                    <site name="node_4" pos="0 0 {}"/>\n'.format(s)
    xml_body += '                    <geom type="sphere" pos="0 0 {}" size="{}" rgba="0.2 0.8 0.2 1" mass="0.1"/>\n'.format(s, s*0.06)
    xml_body += '                    <geom type="capsule" fromto="0 0 {} 0 0 {}" size="{}" rgba="0.8 0.5 0.2 1" mass="0.01"/>\n'.format(s*0.45, s, th_struct)

    # Node 5
    xml_body += '                    <site name="node_5" pos="0 0 {}"/>\n'.format(-s)
    xml_body += '                    <geom type="sphere" pos="0 0 {}" size="{}" rgba="0.2 0.8 0.2 1" mass="0.1"/>\n'.format(-s, s*0.06)
    xml_body += '                    <geom type="capsule" fromto="0 0 {} 0 0 {}" size="{}" rgba="0.8 0.5 0.2 1" mass="0.01"/>\n'.format(-s*0.45, -s, th_struct)

    xml_body += '                </body>\n' # End Inner
    xml_body += '            </body>\n' # End Middle
    xml_body += '        </body>\n' # End Outer
    xml_body += '    </body>\n' # End Root

    # --- 2. CUBE NODES (FLOATING BODIES) ---
    # Nodes 6-13
    # cube_coords list has the positions.
    
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

    for i, v in enumerate(cube_coords):
        idx = 6 + i
        xml_body += '    <body name="node_{}" pos="{} {} {}">\n'.format(idx, v[0], v[1], v[2] + z_offset)
        # Wait, if Gyro is at 1.0, and these are absolute coords...
        # We should put/init them at 1.0 Z as well.
        # all_nodes in the list are centered at 0.
        # So we add 1.0 to Z.
        xml_body += '        <freejoint/>\n'
        xml_body += '        <site name="node_{}"/>\n'.format(idx)
        xml_body += '        <geom type="sphere" size="{}" rgba="0.2 0.8 0.2 1" mass="0.1" contype="1" conaffinity="1" condim="3"/>\n'.format(s*0.03)
        xml_body += '    </body>\n'

    
    # --- 3. TENDONS & ACTUATORS ---
    xml_tendon = '    <tendon>\n'
    xml_actuator = '    <actuator>\n'
    
    # Gyro Actuators (Torque Control)
    # Range -1 to 1 maps to -200 to 200 Torque.
    xml_actuator += '        <motor name="act_outer"  joint="motor_outer"  gear="200" ctrllimited="true" ctrlrange="-1 1"/>\n'
    xml_actuator += '        <motor name="act_middle" joint="motor_middle" gear="200" ctrllimited="true" ctrlrange="-1 1"/>\n'
    xml_actuator += '        <motor name="act_inner"  joint="motor_inner"  gear="200" ctrllimited="true" ctrlrange="-1 1"/>\n'
    
    # A. CUBE LINEAR ACTUATORS (Green Pistons)
    # Connect Cube Nodes to each other with physical telescoping struts
    cube_edge_len = s
    cube_tol = 0.01 * s
    count_muscle = 0
    xml_equality = '    <equality>\n'
    
    # We need to loop indices 6-13
    for i in range(len(cube_coords)):
        for j in range(i + 1, len(cube_coords)):
            p1 = cube_coords[i]
            p2 = cube_coords[j]
            dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
            if abs(dist - cube_edge_len) < cube_tol:
                # Create Physical Piston Assembly
                p_name = f"piston_{count_muscle}"
                
                # Midpoint for initial placement (doesn't matte much with freejoint + equality, but helps solver)
                mid_x = (p1[0] + p2[0]) / 2
                mid_y = (p1[1] + p2[1]) / 2
                mid_z = (p1[2] + p2[2]) / 2 + z_offset # Offset by 1.0 Z
                
                # Determine Orientation (Align Z-axis of Piston with Edge Vector)
                dx, dy, dz = p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]
                
                # Barrel Length (overlap needed)
                # s=1.0. If h_len=0.4, rest=0.4. To reach 1.0, slide needs +0.6. 
                # Rod=0.4. Slide=0.6. Rod leaves barrel.
                # Increase to 0.6. Rest=0.6. To reach 1.0, slide needs +0.4.
                # Rod=0.6. Slide=0.4. Overlap=0.2. Safe.
                h_len = cube_edge_len * 0.6
                
                # Piston Outer Body (Barrel)
                # Use zaxis to align local Z with the edge vector P1->P2
                xml_body += f'    <body name="{p_name}_barrel" pos="{mid_x} {mid_y} {mid_z}" zaxis="{dx} {dy} {dz}">\n'
                xml_body += '        <freejoint/>\n'
                xml_body += f'        <geom type="capsule" fromto="0 0 {-h_len/2} 0 0 {h_len/2}" size="{th_struct*1.5}" rgba="0 1 0 1" mass="0.05" contype="1" conaffinity="1" condim="3"/>\n'
                xml_body += f'        <site name="{p_name}_anchor_a" pos="0 0 {-h_len/2}"/>\n'
                
                # Piston Inner Body (Rod) - slides along Z
                xml_body += f'        <body name="{p_name}_rod" pos="0 0 0">\n'
                # Slide Joint (Z axis of rod frame) with limits (Increased to 0.15)
                xml_body += f'            <joint name="slide_{p_name}" type="slide" axis="0 0 1" limited="true" range="-0.15 0.15"/>\n'
                xml_body += f'            <geom type="capsule" fromto="0 0 {-h_len/2} 0 0 {h_len/2}" size="{th_struct}" rgba="0.5 1 0.5 1" mass="0.05" contype="1" conaffinity="1" condim="3"/>\n'
                xml_body += f'            <site name="{p_name}_anchor_b" pos="0 0 {h_len/2}"/>\n'
                xml_body += '        </body>\n'
                xml_body += '    </body>\n'
                
                # Constraints: Anchor A to Node i, Anchor B to Node j
                # Use Wets (Rigid) to prevent hinging/rotation at the nodes.
                # This creates a rigid frame where edges can only telescope.
                xml_equality += f'        <weld name="weld_{p_name}_a" body1="{p_name}_barrel" body2="node_{6+i}"/>\n'
                xml_equality += f'        <weld name="weld_{p_name}_b" body1="{p_name}_rod" body2="node_{6+j}"/>\n'
                
                # Actuator: Position on the slide joint (Servo-like)
                # "Make them fixed" -> Position Control with high KP
                xml_actuator += f'        <position name="act_{p_name}" joint="slide_{p_name}" kp="500" ctrllimited="true" ctrlrange="-0.15 0.15"/>\n'
                
                count_muscle += 1

    xml_body += '    </worldbody>\n'

    # B. RHOMBIC SPRINGS (Red)
    # Connect Axis Nodes (0-5) to Cube Nodes (6-13)
    rd_edge_len = math.sqrt(0.75) * s
    rd_tol = 0.01 * s
    count_spring = 0
    
    for i in range(len(axis_coords)): # 0-5
        for j in range(len(cube_coords)): # 6-13
            p1 = axis_coords[i]
            p2 = cube_coords[j]
            dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
            if abs(dist - rd_edge_len) < rd_tol:
                # Add Spring
                t_name = f"spring_{count_spring}"
                xml_tendon += f'        <spatial name="{t_name}" stiffness="10" damping="1.0" width="0.01" rgba="1 0.4 0.2 1">\n'
                xml_tendon += f'            <site site="node_{i}"/>\n' # Axis Node (on Gyro)
                xml_tendon += f'            <site site="node_{6+j}"/>\n' # Cube Node (Floating)
                xml_tendon += '        </spatial>\n'
                count_spring += 1
                
    xml_tendon += '    </tendon>\n'
    xml_equality += '    </equality>\n'
    

    
    xml_actuator += '    </actuator>\n'
    
    xml_footer = """</mujoco>
"""
    
    with open(filename, "w") as f:
        f.write(xml_header + xml_body + xml_equality + xml_tendon + xml_actuator + xml_footer)
    
    print(f"Generated {filename} with Dynamic Tensegrity Physics.")

if __name__ == "__main__":
    generate_rd_xml("public/mujoco/menagerie/unitree_g1/rd_structure.xml")
