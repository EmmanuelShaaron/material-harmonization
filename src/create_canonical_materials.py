import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# Helper function
# ------------------------------------------------------------

materials = []


def add_material(
    canonical_id,
    category,
    description,
    material=None,
    grade=None,
    standard=None,
    diameter_mm=None,
    length_mm=None,
    size_in=None,
    pressure_class=None,
    schedule=None,
    voltage_v=None,
    power_kw=None,
    flow_rate_m3h=None,
    head_m=None,
    cores=None,
    cross_section_mm2=None,
    bearing_number=None,
    valve_type=None,
    flange_type=None,
    gasket_type=None,
    tool_type=None,
    tool_size_mm=None,
    uom="NOS",
):
    materials.append({
        "canonical_id": canonical_id,
        "category": category,
        "canonical_description": description,
        "material": material,
        "grade": grade,
        "standard": standard,
        "diameter_mm": diameter_mm,
        "length_mm": length_mm,
        "size_in": size_in,
        "pressure_class": pressure_class,
        "schedule": schedule,
        "voltage_v": voltage_v,
        "power_kw": power_kw,
        "flow_rate_m3h": flow_rate_m3h,
        "head_m": head_m,
        "cores": cores,
        "cross_section_mm2": cross_section_mm2,
        "bearing_number": bearing_number,
        "valve_type": valve_type,
        "flange_type": flange_type,
        "gasket_type": gasket_type,
        "tool_type": tool_type,
        "tool_size_mm": tool_size_mm,
        "uom": uom,
    })


# ============================================================
# 1. FASTENERS
# ============================================================

fasteners = [
    ("M10 X 50 SS304 HEX BOLT", "STAINLESS STEEL", "SS304", 10, 50),
    ("M12 X 50 SS304 HEX BOLT", "STAINLESS STEEL", "SS304", 12, 50),
    ("M10 X 75 SS316 HEX BOLT", "STAINLESS STEEL", "SS316", 10, 75),
    ("M16 X 60 CARBON STEEL HEX BOLT", "CARBON STEEL", "CS", 16, 60),
    ("M20 X 80 GALVANIZED STEEL HEX BOLT", "GALVANIZED STEEL", "GI", 20, 80),
    ("M8 X 40 CARBON STEEL HEX BOLT", "CARBON STEEL", "CS", 8, 40),
    ("M12 X 80 SS316 HEX BOLT", "STAINLESS STEEL", "SS316", 12, 80),
    ("M16 X 75 SS304 HEX BOLT", "STAINLESS STEEL", "SS304", 16, 75),
    ("M20 X 100 CARBON STEEL HEX BOLT", "CARBON STEEL", "CS", 20, 100),
    ("M10 X 30 SS304 HEX BOLT", "STAINLESS STEEL", "SS304", 10, 30),
]

for i, item in enumerate(fasteners, 1):
    desc, material, grade, dia, length = item
    add_material(
        f"CM{i:04d}",
        "FASTENER",
        desc,
        material=material,
        grade=grade,
        diameter_mm=dia,
        length_mm=length,
        uom="NOS",
    )


# ============================================================
# 2. BEARINGS
# ============================================================

bearings = [
    ("DEEP GROOVE BALL BEARING 6205", "6205"),
    ("DEEP GROOVE BALL BEARING 6206", "6206"),
    ("DEEP GROOVE BALL BEARING 6207", "6207"),
    ("DEEP GROOVE BALL BEARING 6305", "6305"),
    ("DEEP GROOVE BALL BEARING 6306", "6306"),
    ("DEEP GROOVE BALL BEARING 6307", "6307"),
    ("TAPERED ROLLER BEARING 30205", "30205"),
    ("TAPERED ROLLER BEARING 30206", "30206"),
    ("TAPERED ROLLER BEARING 30305", "30305"),
    ("SPHERICAL ROLLER BEARING 22205", "22205"),
]

for i, (desc, number) in enumerate(bearings, 11):
    add_material(
        f"CM{i:04d}",
        "BEARING",
        desc,
        material="STEEL",
        bearing_number=number,
        uom="NOS",
    )


# ============================================================
# 3. VALVES
# ============================================================

valves = [
    ("2 IN SS304 GATE VALVE 150 CLASS", "SS304", 2, 150, "GATE"),
    ("2 IN SS304 GATE VALVE 300 CLASS", "SS304", 2, 300, "GATE"),
    ("3 IN CS GATE VALVE 150 CLASS", "CARBON STEEL", 3, 150, "GATE"),
    ("4 IN SS316 BALL VALVE 150 CLASS", "SS316", 4, 150, "BALL"),
    ("6 IN CS BUTTERFLY VALVE 150 CLASS", "CARBON STEEL", 6, 150, "BUTTERFLY"),
    ("4 IN SS304 GATE VALVE 150 CLASS", "SS304", 4, 150, "GATE"),
    ("6 IN SS316 BALL VALVE 300 CLASS", "SS316", 6, 300, "BALL"),
    ("8 IN CS GATE VALVE 300 CLASS", "CARBON STEEL", 8, 300, "GATE"),
    ("10 IN CS BUTTERFLY VALVE 150 CLASS", "CARBON STEEL", 10, 150, "BUTTERFLY"),
    ("2 IN CS GLOBE VALVE 150 CLASS", "CARBON STEEL", 2, 150, "GLOBE"),
]

for i, (desc, material, size, pressure, valve_type) in enumerate(valves, 21):
    add_material(
        f"CM{i:04d}",
        "VALVE",
        desc,
        material=material,
        size_in=size,
        pressure_class=pressure,
        valve_type=valve_type,
        uom="NOS",
    )


# ============================================================
# 4. PIPES
# ============================================================

pipes = [
    ("2 IN CS SEAMLESS PIPE SCH40", "CARBON STEEL", 2, 40),
    ("3 IN CS SEAMLESS PIPE SCH40", "CARBON STEEL", 3, 40),
    ("4 IN SS304 SEAMLESS PIPE SCH40", "SS304", 4, 40),
    ("6 IN CS SEAMLESS PIPE SCH80", "CARBON STEEL", 6, 80),
    ("8 IN SS316 SEAMLESS PIPE SCH40", "SS316", 8, 40),
    ("2 IN SS304 SEAMLESS PIPE SCH10", "SS304", 2, 10),
    ("3 IN SS316 SEAMLESS PIPE SCH40", "SS316", 3, 40),
    ("4 IN CS SEAMLESS PIPE SCH80", "CARBON STEEL", 4, 80),
    ("6 IN SS304 SEAMLESS PIPE SCH40", "SS304", 6, 40),
    ("8 IN CS SEAMLESS PIPE SCH80", "CARBON STEEL", 8, 80),
]

for i, (desc, material, size, schedule) in enumerate(pipes, 31):
    add_material(
        f"CM{i:04d}",
        "PIPE",
        desc,
        material=material,
        size_in=size,
        schedule=schedule,
        uom="MTR",
    )


# ============================================================
# 5. FLANGES
# ============================================================

flanges = [
    ("2 IN CS WELD NECK FLANGE 150 CLASS", "CARBON STEEL", 2, 150, "WELD NECK"),
    ("2 IN SS304 WELD NECK FLANGE 150 CLASS", "SS304", 2, 150, "WELD NECK"),
    ("3 IN CS SLIP ON FLANGE 150 CLASS", "CARBON STEEL", 3, 150, "SLIP ON"),
    ("4 IN SS316 WELD NECK FLANGE 300 CLASS", "SS316", 4, 300, "WELD NECK"),
    ("6 IN CS SLIP ON FLANGE 150 CLASS", "CARBON STEEL", 6, 150, "SLIP ON"),
    ("8 IN CS WELD NECK FLANGE 300 CLASS", "CARBON STEEL", 8, 300, "WELD NECK"),
    ("10 IN SS304 SLIP ON FLANGE 150 CLASS", "SS304", 10, 150, "SLIP ON"),
    ("12 IN CS WELD NECK FLANGE 150 CLASS", "CARBON STEEL", 12, 150, "WELD NECK"),
    ("4 IN SS304 SLIP ON FLANGE 300 CLASS", "SS304", 4, 300, "SLIP ON"),
    ("6 IN SS316 WELD NECK FLANGE 150 CLASS", "SS316", 6, 150, "WELD NECK"),
]

for i, (desc, material, size, pressure, flange_type) in enumerate(flanges, 41):
    add_material(
        f"CM{i:04d}",
        "FLANGE",
        desc,
        material=material,
        size_in=size,
        pressure_class=pressure,
        flange_type=flange_type,
        uom="NOS",
    )


# ============================================================
# 6. GASKETS
# ============================================================

gaskets = [
    ("2 IN SPIRAL WOUND SS GRAPHITE GASKET 150 CLASS", "SS", 2, 150, "SPIRAL WOUND"),
    ("3 IN SPIRAL WOUND SS GRAPHITE GASKET 150 CLASS", "SS", 3, 150, "SPIRAL WOUND"),
    ("4 IN SPIRAL WOUND GRAPHITE GASKET 300 CLASS", "GRAPHITE", 4, 300, "SPIRAL WOUND"),
    ("6 IN SPIRAL WOUND GRAPHITE GASKET 150 CLASS", "GRAPHITE", 6, 150, "SPIRAL WOUND"),
    ("8 IN PTFE FULL FACE GASKET 150 CLASS", "PTFE", 8, 150, "FULL FACE"),
    ("2 IN PTFE FULL FACE GASKET 150 CLASS", "PTFE", 2, 150, "FULL FACE"),
    ("4 IN SS GRAPHITE GASKET 150 CLASS", "SS", 4, 150, "SPIRAL WOUND"),
    ("6 IN PTFE FULL FACE GASKET 300 CLASS", "PTFE", 6, 300, "FULL FACE"),
    ("10 IN GRAPHITE SPIRAL WOUND GASKET 150 CLASS", "GRAPHITE", 10, 150, "SPIRAL WOUND"),
    ("12 IN GRAPHITE SPIRAL WOUND GASKET 300 CLASS", "GRAPHITE", 12, 300, "SPIRAL WOUND"),
]

for i, (desc, material, size, pressure, gasket_type) in enumerate(gaskets, 51):
    add_material(
        f"CM{i:04d}",
        "GASKET",
        desc,
        material=material,
        size_in=size,
        pressure_class=pressure,
        gasket_type=gasket_type,
        uom="NOS",
    )


# ============================================================
# 7. ELECTRICAL CABLES
# ============================================================

cables = [
    ("1C X 2.5 SQMM PVC CABLE 1.1KV", 1, 2.5, 1100),
    ("1C X 4 SQMM PVC CABLE 1.1KV", 1, 4, 1100),
    ("3C X 2.5 SQMM PVC CABLE 1.1KV", 3, 2.5, 1100),
    ("3C X 4 SQMM PVC CABLE 1.1KV", 3, 4, 1100),
    ("3C X 6 SQMM PVC CABLE 1.1KV", 3, 6, 1100),
    ("4C X 10 SQMM PVC CABLE 1.1KV", 4, 10, 1100),
    ("4C X 16 SQMM PVC CABLE 1.1KV", 4, 16, 1100),
    ("4C X 25 SQMM PVC CABLE 1.1KV", 4, 25, 1100),
    ("3C X 35 SQMM PVC CABLE 1.1KV", 3, 35, 1100),
    ("4C X 50 SQMM PVC CABLE 1.1KV", 4, 50, 1100),
]

for i, (desc, cores, cross_section, voltage) in enumerate(cables, 61):
    add_material(
        f"CM{i:04d}",
        "ELECTRICAL_CABLE",
        desc,
        material="COPPER",
        voltage_v=voltage,
        cores=cores,
        cross_section_mm2=cross_section,
        uom="MTR",
    )


# ============================================================
# 8. MOTORS
# ============================================================

motors = [
    ("3 PHASE INDUCTION MOTOR 5.5KW 415V 50HZ", 5.5, 415),
    ("3 PHASE INDUCTION MOTOR 7.5KW 415V 50HZ", 7.5, 415),
    ("3 PHASE INDUCTION MOTOR 11KW 415V 50HZ", 11, 415),
    ("3 PHASE INDUCTION MOTOR 15KW 415V 50HZ", 15, 415),
    ("3 PHASE INDUCTION MOTOR 18.5KW 415V 50HZ", 18.5, 415),
    ("3 PHASE INDUCTION MOTOR 22KW 415V 50HZ", 22, 415),
    ("3 PHASE INDUCTION MOTOR 30KW 415V 50HZ", 30, 415),
    ("3 PHASE INDUCTION MOTOR 37KW 415V 50HZ", 37, 415),
    ("3 PHASE INDUCTION MOTOR 45KW 415V 50HZ", 45, 415),
    ("3 PHASE INDUCTION MOTOR 55KW 415V 50HZ", 55, 415),
]

for i, (desc, power, voltage) in enumerate(motors, 71):
    add_material(
        f"CM{i:04d}",
        "MOTOR",
        desc,
        material="CAST IRON",
        voltage_v=voltage,
        power_kw=power,
        uom="NOS",
    )


# ============================================================
# 9. PUMPS
# ============================================================

pumps = [
    ("CENTRIFUGAL PUMP 20 M3/H 30M HEAD 5.5KW", 20, 30, 5.5),
    ("CENTRIFUGAL PUMP 30 M3/H 40M HEAD 7.5KW", 30, 40, 7.5),
    ("CENTRIFUGAL PUMP 50 M3/H 50M HEAD 11KW", 50, 50, 11),
    ("CENTRIFUGAL PUMP 75 M3/H 40M HEAD 15KW", 75, 40, 15),
    ("CENTRIFUGAL PUMP 100 M3/H 50M HEAD 22KW", 100, 50, 22),
    ("CENTRIFUGAL PUMP 120 M3/H 60M HEAD 30KW", 120, 60, 30),
    ("CENTRIFUGAL PUMP 150 M3/H 50M HEAD 37KW", 150, 50, 37),
    ("CENTRIFUGAL PUMP 200 M3/H 60M HEAD 45KW", 200, 60, 45),
    ("CENTRIFUGAL PUMP 250 M3/H 70M HEAD 55KW", 250, 70, 55),
    ("CENTRIFUGAL PUMP 300 M3/H 80M HEAD 75KW", 300, 80, 75),
]

for i, (desc, flow, head, power) in enumerate(pumps, 81):
    add_material(
        f"CM{i:04d}",
        "PUMP",
        desc,
        material="CAST IRON",
        power_kw=power,
        flow_rate_m3h=flow,
        head_m=head,
        uom="NOS",
    )


# ============================================================
# 10. INDUSTRIAL TOOLS
# ============================================================

tools = [
    ("ANGLE GRINDER 100MM 750W", "ANGLE GRINDER", 100, 0.75),
    ("ANGLE GRINDER 115MM 900W", "ANGLE GRINDER", 115, 0.90),
    ("ANGLE GRINDER 125MM 1100W", "ANGLE GRINDER", 125, 1.10),
    ("ELECTRIC DRILL 10MM 650W", "DRILL", 10, 0.65),
    ("ELECTRIC DRILL 13MM 800W", "DRILL", 13, 0.80),
    ("IMPACT WRENCH 1/2 IN 500W", "IMPACT WRENCH", 12.7, 0.50),
    ("CUTTING MACHINE 355MM 2000W", "CUTTING MACHINE", 355, 2.00),
    ("WELDING MACHINE 200A", "WELDING MACHINE", None, None),
    ("TORQUE WRENCH 50-250NM", "TORQUE WRENCH", None, None),
    ("BENCH GRINDER 200MM 550W", "BENCH GRINDER", 200, 0.55),
]

for i, (desc, tool_type, size, power) in enumerate(tools, 91):
    add_material(
        f"CM{i:04d}",
        "INDUSTRIAL_TOOL",
        desc,
        tool_type=tool_type,
        tool_size_mm=size,
        power_kw=power,
        uom="NOS",
    )


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(materials)


# ============================================================
# VALIDATION
# ============================================================

print("=" * 60)
print("CANONICAL MATERIAL MASTER CREATED")
print("=" * 60)

print(f"Total materials: {len(df)}")

print("\nCategories:")
print(df["category"].value_counts().sort_index())

print("\nMissing values by column:")
print(df.isnull().sum())

print("\nFirst 10 records:")
print(
    df[
        [
            "canonical_id",
            "category",
            "canonical_description",
            "material",
            "grade",
            "size_in",
            "pressure_class",
            "uom",
        ]
    ].head(10).to_string(index=False)
)


# ============================================================
# SAVE
# ============================================================

output_path = Path("data/benchmark/canonical_materials.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("\n" + "=" * 60)
print(f"Saved to: {output_path}")
print("=" * 60)