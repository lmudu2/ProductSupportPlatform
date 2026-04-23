import pandas as pd
import numpy as np
import os
import random
import hashlib
from datetime import datetime, timedelta

# Core configuration
RECORDS_COUNT = 50000
SENSORS_COUNT = 200000

# Define base directory relative to this script (scripts/generate_data.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LABOR_RATES = {"Automotive": 280, "Industrial": 180, "Mobile": 60, "Appliance": 110}

MODEL_REGISTRY = {
    "Automotive": [
        "Tesla Model S", "Tesla Model S Pro", "Tesla Model S Performance", "Tesla Model S Long Range",
        "Tesla Model S GT", "Tesla Model 3 Long Range", "Tesla Model 3 Pro", "Tesla Model 3 Ultra",
        "Tesla Model 3 GT", "Tesla Model 3", "Tesla Model 3 Performance", "Tesla Model Y",
        "Tesla Model Y Sport", "Tesla Model Y Ultra", "Tesla Model Y Long Range", "Tesla Model Y GT",
        "Tesla Model Y Performance", "Tesla Model Y Pro", "Tesla Model Y Plaid", "Tesla Cybertruck Plaid",
        "Tesla Cybertruck Sport", "Tesla Cybertruck GT", "Tesla Cybertruck Performance", "Tesla Cybertruck",
        "Tesla Cybertruck Ultra", "Tesla Cybertruck Long Range", "Tesla Cybertruck Pro", "Ford F-150 Performance",
        "Ford F-150 Long Range", "Ford F-150 Sport", "Ford F-150", "Ford F-150 GT",
        "Ford F-150 Ultra", "Ford F-150 Plaid", "Ford Mustang Pro", "Ford Mustang GT",
        "Ford Mustang Performance", "Ford Mustang", "Ford Mustang Plaid", "Ford Mustang Sport",
        "Ford Mustang Ultra", "BMW i4 Long Range", "BMW i4 GT", "BMW i4 Performance",
        "BMW i4 Ultra", "BMW i4 Pro", "BMW i4 Plaid", "BMW i4",
        "BMW i4 Sport", "BMW iX Plaid", "BMW iX Ultra", "BMW iX Performance",
        "BMW iX", "BMW iX Long Range", "Audi e-tron Ultra", "Audi e-tron Performance",
        "Audi e-tron Plaid", "Audi e-tron Sport", "Audi e-tron Long Range", "Lucid Air Pro",
        "Lucid Air Long Range", "Lucid Air Sport", "Lucid Air Performance", "Lucid Air",
        "Lucid Air GT", "Lucid Air Plaid", "Rivian R1T Performance", "Rivian R1T Plaid",
        "Rivian R1T Ultra", "Rivian R1T Sport", "Rivian R1T Long Range", "Rivian R1T GT",
        "Rivian R1S", "Rivian R1S Long Range", "Rivian R1S Sport", "Rivian R1S Performance",
        "Rivian R1S Plaid", "Rivian R1S Ultra", "Rivian R1S Pro", "Porsche Taycan Pro",
        "Porsche Taycan Long Range", "Porsche Taycan Sport", "Porsche Taycan Plaid", "Porsche Taycan GT",
        "Porsche Taycan Performance", "Mercedes EQS Performance", "Mercedes EQS Sport", "Mercedes EQS Long Range",
        "Mercedes EQS Pro", "Mercedes EQS Ultra", "Mercedes EQS Plaid", "Mercedes EQS GT",
        "Mercedes EQS", "Hyundai IONIQ Plaid", "Hyundai IONIQ Long Range", "Hyundai IONIQ GT",
        "Hyundai IONIQ Sport", "Hyundai IONIQ", "Hyundai IONIQ Pro", "Hyundai IONIQ Performance",
        "Kia EV Performance", "Kia EV Ultra", "Kia EV Pro", "Kia EV Plaid",
        "Kia EV", "Kia EV Long Range", "Volvo EX Sport", "Volvo EX GT",
        "Volvo EX Performance", "Volvo EX Ultra", "Volvo EX", "Volvo EX Pro",
        "Volvo EX Plaid", "Volvo EX Long Range", "Lamborghini Long Range", "Lamborghini Performance",
        "Lamborghini Plaid", "Lamborghini Sport", "Lamborghini Pro", "Lamborghini",
        "Lamborghini GT", "Ferrari Long Range", "Ferrari Ultra", "Ferrari Pro",
        "Ferrari Performance", "Ferrari Sport", "Ferrari", "Toyota BZ4X Performance",
        "Toyota BZ4X GT", "Toyota BZ4X Ultra", "Toyota BZ4X", "Toyota BZ4X Sport",
        "Toyota BZ4X Long Range", "Toyota BZ4X Pro", "Nissan Ariya Pro", "Nissan Ariya Ultra",
        "Nissan Ariya Performance", "Nissan Ariya Long Range", "Nissan Ariya", "Chevrolet Bolt Long Range",
        "Chevrolet Bolt", "Chevrolet Bolt Pro", "Chevrolet Bolt Plaid", "Chevrolet Bolt Ultra",
        "Chevrolet Bolt Performance", "Honda Prologue Performance", "Honda Prologue Pro", "Honda Prologue Plaid",
        "Honda Prologue GT", "Honda Prologue Long Range", "Honda Prologue Ultra", "Mazda MX-30 Plaid",
        "Mazda MX-30 GT", "Mazda MX-30 Pro", "Mazda MX-30 Long Range", "Mazda MX-30 Performance",
        "Mazda MX-30 Ultra", "Mazda MX-30 Sport", "Mazda MX-30", "Subaru Solterra Long Range",
        "Subaru Solterra Sport", "Subaru Solterra Ultra", "Subaru Solterra", "Subaru Solterra Performance",
        "Subaru Solterra GT", "Subaru Solterra Plaid", "Subaru Solterra Pro",
    ],
    "Mobile": [
        "iPhone 15 Pro", "iPhone 15 Mini", "iPhone 15 FE", "iPhone 15",
        "iPhone 15 Lite", "iPhone 14", "iPhone 14 FE", "iPhone 14 Pro Max",
        "iPhone 14 Lite", "iPhone 14 Pro", "Galaxy S24 Lite", "Galaxy S24 Pro",
        "Galaxy S24 Ultra", "Galaxy S24 FE", "Galaxy S24 Plus", "Galaxy S24",
        "Galaxy S24 Mini", "Galaxy Z Fold Plus", "Galaxy Z Fold", "Galaxy Z Fold FE",
        "Galaxy Z Fold Lite", "Galaxy Z Fold Pro Max", "Galaxy Z Fold Pro", "Galaxy Z Fold Ultra",
        "Galaxy Z Fold Mini", "Pixel 8 Pro", "Pixel 8", "Pixel 8 Plus",
        "Pixel 8 Pro Max", "Pixel 8 FE", "Pixel Fold Plus", "Pixel Fold Pro",
        "Pixel Fold Ultra", "Pixel Fold Lite", "Pixel Fold FE", "Pixel Fold Mini",
        "OnePlus 12 Ultra", "OnePlus 12 Plus", "OnePlus 12 Pro", "OnePlus 12",
        "OnePlus 12 FE", "OnePlus 12 Pro Max", "Xiaomi 14", "Xiaomi 14 Mini",
        "Xiaomi 14 Ultra", "Xiaomi 14 Lite", "Xiaomi 14 FE", "Asus ROG Phone Pro Max",
        "Asus ROG Phone Plus", "Asus ROG Phone FE", "Asus ROG Phone Mini", "Asus ROG Phone Pro",
        "Asus ROG Phone Ultra", "Sony Xperia Pro Max", "Sony Xperia Plus", "Sony Xperia",
        "Sony Xperia FE", "Sony Xperia Lite", "Nothing Phone Ultra", "Nothing Phone Plus",
        "Nothing Phone Mini", "Nothing Phone Lite", "Nothing Phone FE", "Nothing Phone",
        "Nothing Phone Pro Max", "Nothing Phone Pro", "Motorola Edge", "Motorola Edge Ultra",
        "Motorola Edge Mini", "Motorola Edge FE", "Motorola Edge Lite", "Motorola Edge Pro Max",
        "Huawei Mate", "Huawei Mate Lite", "Huawei Mate Ultra", "Huawei Mate Plus",
        "Huawei Mate Pro", "Huawei Mate FE", "Huawei Mate Pro Max", "Zenfone Pro",
        "Zenfone Ultra", "Zenfone", "Zenfone Lite", "Zenfone Plus",
        "Zenfone Mini", "Vivo X", "Vivo X Ultra", "Vivo X Lite",
        "Vivo X Plus", "Vivo X Pro Max", "Vivo X Pro", "Redmi Note Mini",
        "Redmi Note Pro", "Redmi Note Pro Max", "Redmi Note Plus", "Redmi Note FE",
        "Redmi Note Lite", "Oppo Find Lite", "Oppo Find Pro Max", "Oppo Find",
        "Oppo Find Mini", "Oppo Find Plus", "Oppo Find FE", "Oppo Find Ultra",
        "Realme GT Plus", "Realme GT Ultra", "Realme GT Pro Max", "Realme GT Pro",
        "Realme GT Mini", "Honor Magic Plus", "Honor Magic Pro Max", "Honor Magic FE",
        "Honor Magic Pro", "Honor Magic Lite", "Nokia G", "Nokia G Mini",
        "Nokia G Ultra", "Nokia G Pro Max", "Nokia G Lite", "Nokia G Plus",
        "Nokia G Pro",
    ],
    "Appliance": [
        "IceLogic Smart Fridge", "IceLogic Chest Freezer", "IceLogic Mini Fridge",
        "Whirlpool Smart Fridge", "Whirlpool Chest Freezer", "Whirlpool Mini Fridge",
        "SmartVortex Dryer v8", "SmartVortex Front-Load Washer",
        "LG Electric Dryer", "LG Mega-Capacity Washer",
        "AeroTherm Convection Oven", "AeroTherm Over-Range Microwave",
        "GE Profile Cooktop Oven", "GE Profile Cooktop Cooktop",
        "AquaFresh Water Purifier", "AquaFresh Under-Sink Filter",
        "HydroWash 9000 Pro", "HydroWash 8000 Basic",
        "Samsung Front-Load Washer", "Samsung Bespoke Fridge Dryer",
        "AquaFlow Dishwasher X", "AquaFlow Dishwasher Mini",
        "Bosch Dishwasher 800 Series", "Bosch Dishwasher 300 Series",
        "PureAir HEPA Purifier", "PureAir Tower Filter",
        "AirPure 4000 Purifier", "AirPure 5000 Max",
        "Dyson Purifier Cool", "Dyson Purifier Hot+Cool",
        "PrecisionGrind Coffee System", "PrecisionGrind Espresso",
        "SmartBrew Coffee Station", "SmartBrew Pod Maker",
        "Breville Espresso Machine", "Breville Coffee System",
        "TurboClean Robot Vacuum", "TurboClean Stick Vacuum",
        "Samsung Jet Stick Vacuum", "Samsung JetBot",
        "SmartSous-Vide Precision", "SmartSous-Vide Pro",
        "Anova Sous-Vide Nano", "Anova Sous-Vide Pro",
        "HeatSync Induction Cooktop", "HeatSync Gas Cooktop",
        "CoolLogic Wine Cabinet", "CoolLogic Beverage Center",
        "Brita Water Purifier", "Brita Under-Sink Filter",
        "IceLogic Fridge Pro", "IceLogic Fridge Smart", "IceLogic Fridge Max", "IceLogic Fridge Plus",
        "IceLogic Fridge Elite", "IceLogic Freezer Compact", "IceLogic Freezer Smart", "IceLogic Freezer Elite",
        "IceLogic Freezer Pro", "IceLogic Freezer Eco", "IceLogic Freezer Plus", "IceLogic Freezer Max",
        "SmartVortex Washer", "SmartVortex Washer Plus", "SmartVortex Washer Smart", "SmartVortex Washer Compact",
        "SmartVortex Washer Elite", "SmartVortex Washer Eco", "SmartVortex Washer Max", "SmartVortex Dryer Elite",
        "SmartVortex Dryer Smart", "SmartVortex Dryer Plus", "SmartVortex Dryer Pro", "SmartVortex Dryer Compact",
        "SmartVortex Dryer Eco", "SmartVortex Dryer Max", "AeroTherm Oven Pro", "AeroTherm Oven",
        "AeroTherm Oven Smart", "AeroTherm Oven Plus", "AeroTherm Oven Eco", "AeroTherm Microwave Elite",
        "AeroTherm Microwave Compact", "AeroTherm Microwave Pro", "AeroTherm Microwave", "AeroTherm Microwave Plus",
        "AeroTherm Microwave Smart", "AeroTherm Microwave Max", "AquaFresh Filter Compact", "AquaFresh Filter Smart",
        "AquaFresh Filter Pro", "AquaFresh Filter", "AquaFresh Filter Elite", "AquaFresh Filter Plus",
        "AquaFresh Filter Eco", "HydroWash Dishwasher Compact", "HydroWash Dishwasher Eco", "HydroWash Dishwasher Pro",
        "HydroWash Dishwasher Smart", "HydroWash Dishwasher Plus", "HydroWash Dishwasher", "PureAir Purifier Smart",
        "PureAir Purifier Eco", "PureAir Purifier Compact", "PureAir Purifier Pro", "PureAir Purifier Elite",
        "PureAir Purifier", "PrecisionGrind Maker Eco", "PrecisionGrind Maker Plus", "PrecisionGrind Maker",
        "PrecisionGrind Maker Compact", "PrecisionGrind Maker Pro", "SmartBrew Machine Plus", "SmartBrew Machine Elite",
        "SmartBrew Machine Eco", "SmartBrew Machine Pro", "SmartBrew Machine Max", "SmartBrew Machine",
        "TurboClean Vacuum Eco", "TurboClean Vacuum Elite", "TurboClean Vacuum Plus", "TurboClean Vacuum",
        "TurboClean Vacuum Smart", "TurboClean Vacuum Pro", "SmartSous-Vide Stick Smart", "SmartSous-Vide Stick",
        "SmartSous-Vide Stick Eco", "SmartSous-Vide Stick Elite", "SmartSous-Vide Stick Pro", "SmartSous-Vide Stick Max",
        "SmartSous-Vide Stick Compact", "SmartSous-Vide Stick Plus", "HeatSync Cooktop Eco", "HeatSync Cooktop Elite",
        "HeatSync Cooktop Smart", "HeatSync Cooktop Plus", "HeatSync Cooktop Compact", "CoolLogic Cooler Eco",
        "CoolLogic Cooler Max", "CoolLogic Cooler Pro", "CoolLogic Cooler Elite", "CoolLogic Cooler",
        "LG Instaview Fridge", "LG Instaview Fridge Max", "LG Instaview Fridge Eco", "LG Instaview Fridge Pro",
        "LG Instaview Fridge Elite", "LG Instaview Fridge Smart", "LG Instaview Fridge Plus", "LG Instaview Fridge Compact",
        "Samsung Bespoke Fridge Pro", "Samsung Bespoke Fridge Smart", "Samsung Bespoke Fridge Elite", "Samsung Bespoke Fridge Max",
        "Samsung Bespoke Fridge Eco", "Samsung Bespoke Fridge Compact", "Samsung Bespoke Fridge Plus", "Whirlpool Cabrio Oven Eco",
        "Whirlpool Cabrio Oven Smart", "Whirlpool Cabrio Oven Elite", "Whirlpool Cabrio Oven Max", "Whirlpool Cabrio Oven Pro",
        "Whirlpool Cabrio Oven", "Whirlpool Cabrio Oven Compact", "GE Profile Cooktop Elite", "GE Profile Cooktop Max",
        "GE Profile Cooktop Eco", "GE Profile Cooktop Plus", "GE Profile Cooktop Compact", "GE Profile Cooktop Smart",
        "GE Profile Cooktop", "GE Profile Cooktop Pro", "Bosch Serie Dishwasher Compact", "Bosch Serie Dishwasher Plus",
        "Bosch Serie Dishwasher Max", "Bosch Serie Dishwasher Smart", "Bosch Serie Dishwasher Elite", "Bosch Serie Dishwasher Pro",
        "Bosch Serie Dishwasher Eco", "KitchenAid Artisan Espresso Compact", "KitchenAid Artisan Espresso Max", "KitchenAid Artisan Espresso Plus",
        "KitchenAid Artisan Espresso Pro", "KitchenAid Artisan Espresso", "KitchenAid Artisan Espresso Eco", "KitchenAid Artisan Espresso Elite",
        "KitchenAid Artisan Espresso Smart",
    ],
    "Industrial": [
        "RoboArm Compact", "RoboArm v2", "RoboArm Max", "RoboArm Industrial",
        "RoboArm v1", "RoboArm Heavy-Duty", "Titan CNC Precision", "Titan CNC Compact",
        "Titan CNC v1", "Titan CNC Heavy-Duty", "Titan CNC Max", "Titan CNC Pro",
        "GenSet Power Max", "GenSet Power Heavy-Duty", "GenSet Power Precision", "GenSet Power v2",
        "GenSet Power Compact", "GenSet Power Pro", "HydraPress v2", "HydraPress Max",
        "HydraPress Heavy-Duty", "HydraPress Precision", "HydraPress Compact", "Vortex Turbine v1",
        "Vortex Turbine Compact", "Vortex Turbine v2", "Vortex Turbine Precision", "Vortex Turbine Heavy-Duty",
        "Vortex Turbine Max", "Vortex Turbine Industrial", "Vortex Turbine Pro", "LaserCut Max",
        "LaserCut Precision", "LaserCut Compact", "LaserCut Heavy-Duty", "LaserCut v2",
        "LaserCut Pro", "LaserCut Industrial", "LaserCut v1", "DeepDrill Rig Heavy-Duty",
        "DeepDrill Rig Max", "DeepDrill Rig Industrial", "DeepDrill Rig Pro", "DeepDrill Rig Precision",
        "DeepDrill Rig Compact", "DeepDrill Rig v1", "SolarArray Precision", "SolarArray v1",
        "SolarArray Industrial", "SolarArray Pro", "SolarArray v2", "SolarArray Heavy-Duty",
        "SolarArray Compact", "BioReactor v2", "BioReactor Precision", "BioReactor Max",
        "BioReactor Industrial", "BioReactor Heavy-Duty", "BioReactor Pro", "BioReactor v1",
        "ConveyorSync v2", "ConveyorSync Heavy-Duty", "ConveyorSync Max", "ConveyorSync Pro",
        "ConveyorSync Industrial", "ConveyorSync Precision", "ArcWelder Heavy-Duty", "ArcWelder Max",
        "ArcWelder Precision", "ArcWelder Industrial", "ArcWelder v1", "PneumoPress Precision",
        "PneumoPress v1", "PneumoPress Pro", "PneumoPress Industrial", "PneumoPress Heavy-Duty",
        "PneumoPress v2", "PneumoPress Max", "PneumoPress Compact", "ThermoForge Compact",
        "ThermoForge Heavy-Duty", "ThermoForge Max", "ThermoForge v1", "ThermoForge Industrial",
        "ThermoForge v2", "CompressMax Pro", "CompressMax Max", "CompressMax Heavy-Duty",
        "CompressMax v2", "CompressMax v1", "CompressMax Compact", "CompressMax Industrial",
        "CompressMax Precision", "DriveSync Pro", "DriveSync Max", "DriveSync Heavy-Duty",
        "DriveSync v2", "DriveSync v1", "DriveSync Compact", "DriveSync Precision",
        "DriveSync Industrial", "Siemens PLC Precision", "Siemens PLC Pro", "Siemens PLC Max",
        "Siemens PLC Heavy-Duty", "Siemens PLC Industrial", "Siemens PLC v2", "ABB Controller v2",
        "ABB Controller Heavy-Duty", "ABB Controller v1", "ABB Controller Compact", "ABB Controller Industrial",
        "ABB Controller Precision", "ABB Controller Max", "Fanuc Robot v1", "Fanuc Robot Max",
        "Fanuc Robot Precision", "Fanuc Robot v2", "Fanuc Robot Compact", "KUKA Arm Pro",
        "KUKA Arm v2", "KUKA Arm Max", "KUKA Arm Heavy-Duty", "KUKA Arm v1",
        "Rockwell Drive Precision", "Rockwell Drive Industrial", "Rockwell Drive Pro", "Rockwell Drive Max",
        "Rockwell Drive v2", "Rockwell Drive Compact",
    ],
}


SUPPLIERS = {
    "Automotive": ["AutoZone Commercial", "Advance Auto Parts", "NAPA Auto Parts", "O'Reilly Auto Parts"],
    "Industrial": ["Grainger Industrial Supply", "Fastenal", "Global Industrial", "Motion Industries"],
    "Appliance": ["Sears PartsDirect", "RepairClinic", "AppliancePartsPros", "Marcone Supply"],
    "Mobile": ["Digi-Key Electronics", "Mouser Electronics", "iFixit Pro", "MobileSentrix"]
}

MSRP_MAP = {
    # Automotive
    "Tesla Model S": 85000,
    "Tesla Model S Pro": 110500,
    "Tesla Model S Performance": 136000,
    "Tesla Model S Long Range": 110500,
    "Tesla Model S GT": 170000,
    "Tesla Model 3 Long Range": 58500,
    "Tesla Model 3 Pro": 58500,
    "Tesla Model 3 Ultra": 72000,
    "Tesla Model 3 GT": 90000,
    "Tesla Model 3": 45000,
    "Tesla Model 3 Performance": 72000,
    "Tesla Model Y": 50000,
    "Tesla Model Y Sport": 100000,
    "Tesla Model Y Ultra": 80000,
    "Tesla Model Y Long Range": 65000,
    "Tesla Model Y GT": 100000,
    "Tesla Model Y Performance": 80000,
    "Tesla Model Y Pro": 65000,
    "Tesla Model Y Plaid": 100000,
    "Tesla Cybertruck Plaid": 160000,
    "Tesla Cybertruck Sport": 160000,
    "Tesla Cybertruck GT": 160000,
    "Tesla Cybertruck Performance": 128000,
    "Tesla Cybertruck": 80000,
    "Tesla Cybertruck Ultra": 128000,
    "Tesla Cybertruck Long Range": 104000,
    "Tesla Cybertruck Pro": 104000,
    "Ford F-150 Performance": 64000,
    "Ford F-150 Long Range": 52000,
    "Ford F-150 Sport": 80000,
    "Ford F-150": 40000,
    "Ford F-150 GT": 80000,
    "Ford F-150 Ultra": 64000,
    "Ford F-150 Plaid": 80000,
    "Ford Mustang Pro": 58500,
    "Ford Mustang GT": 90000,
    "Ford Mustang Performance": 72000,
    "Ford Mustang": 45000,
    "Ford Mustang Plaid": 90000,
    "Ford Mustang Sport": 90000,
    "Ford Mustang Ultra": 72000,
    "BMW i4 Long Range": 71500,
    "BMW i4 GT": 110000,
    "BMW i4 Performance": 88000,
    "BMW i4 Ultra": 88000,
    "BMW i4 Pro": 71500,
    "BMW i4 Plaid": 110000,
    "BMW i4": 55000,
    "BMW i4 Sport": 110000,
    "BMW iX Plaid": 170000,
    "BMW iX Ultra": 136000,
    "BMW iX Performance": 136000,
    "BMW iX": 85000,
    "BMW iX Long Range": 110500,
    "Audi e-tron Ultra": 104000,
    "Audi e-tron Performance": 104000,
    "Audi e-tron Plaid": 130000,
    "Audi e-tron Sport": 130000,
    "Audi e-tron Long Range": 84500,
    "Lucid Air Pro": 104000,
    "Lucid Air Long Range": 104000,
    "Lucid Air Sport": 160000,
    "Lucid Air Performance": 128000,
    "Lucid Air": 80000,
    "Lucid Air GT": 160000,
    "Lucid Air Plaid": 160000,
    "Rivian R1T Performance": 112000,
    "Rivian R1T Plaid": 140000,
    "Rivian R1T Ultra": 112000,
    "Rivian R1T Sport": 140000,
    "Rivian R1T Long Range": 91000,
    "Rivian R1T GT": 140000,
    "Rivian R1S": 75000,
    "Rivian R1S Long Range": 97500,
    "Rivian R1S Sport": 150000,
    "Rivian R1S Performance": 120000,
    "Rivian R1S Plaid": 150000,
    "Rivian R1S Ultra": 120000,
    "Rivian R1S Pro": 97500,
    "Porsche Taycan Pro": 117000,
    "Porsche Taycan Long Range": 117000,
    "Porsche Taycan Sport": 180000,
    "Porsche Taycan Plaid": 180000,
    "Porsche Taycan GT": 180000,
    "Porsche Taycan Performance": 144000,
    "Mercedes EQS Performance": 160000,
    "Mercedes EQS Sport": 200000,
    "Mercedes EQS Long Range": 130000,
    "Mercedes EQS Pro": 130000,
    "Mercedes EQS Ultra": 160000,
    "Mercedes EQS Plaid": 200000,
    "Mercedes EQS GT": 200000,
    "Mercedes EQS": 100000,
    "Hyundai IONIQ Plaid": 90000,
    "Hyundai IONIQ Long Range": 58500,
    "Hyundai IONIQ GT": 90000,
    "Hyundai IONIQ Sport": 90000,
    "Hyundai IONIQ": 45000,
    "Hyundai IONIQ Pro": 58500,
    "Hyundai IONIQ Performance": 72000,
    "Kia EV Performance": 76800,
    "Kia EV Ultra": 76800,
    "Kia EV Pro": 62400,
    "Kia EV Plaid": 96000,
    "Kia EV": 48000,
    "Kia EV Long Range": 62400,
    "Volvo EX Sport": 100000,
    "Volvo EX GT": 100000,
    "Volvo EX Performance": 80000,
    "Volvo EX Ultra": 80000,
    "Volvo EX": 50000,
    "Volvo EX Pro": 65000,
    "Volvo EX Plaid": 100000,
    "Volvo EX Long Range": 65000,
    "Lamborghini Long Range": 286000,
    "Lamborghini Performance": 352000,
    "Lamborghini Plaid": 440000,
    "Lamborghini Sport": 440000,
    "Lamborghini Pro": 286000,
    "Lamborghini": 220000,
    "Lamborghini GT": 440000,
    "Ferrari Long Range": 390000,
    "Ferrari Ultra": 480000,
    "Ferrari Pro": 390000,
    "Ferrari Performance": 480000,
    "Ferrari Sport": 600000,
    "Ferrari": 300000,
    "Toyota BZ4X Performance": 67200,
    "Toyota BZ4X GT": 84000,
    "Toyota BZ4X Ultra": 67200,
    "Toyota BZ4X": 42000,
    "Toyota BZ4X Sport": 84000,
    "Toyota BZ4X Long Range": 54600,
    "Toyota BZ4X Pro": 54600,
    "Nissan Ariya Pro": 52000,
    "Nissan Ariya Ultra": 64000,
    "Nissan Ariya Performance": 64000,
    "Nissan Ariya Long Range": 52000,
    "Nissan Ariya": 40000,
    "Chevrolet Bolt Long Range": 36400,
    "Chevrolet Bolt": 28000,
    "Chevrolet Bolt Pro": 36400,
    "Chevrolet Bolt Plaid": 56000,
    "Chevrolet Bolt Ultra": 44800,
    "Chevrolet Bolt Performance": 44800,
    "Honda Prologue Performance": 72000,
    "Honda Prologue Pro": 58500,
    "Honda Prologue Plaid": 90000,
    "Honda Prologue GT": 90000,
    "Honda Prologue Long Range": 58500,
    "Honda Prologue Ultra": 72000,
    "Mazda MX-30 Plaid": 70000,
    "Mazda MX-30 GT": 70000,
    "Mazda MX-30 Pro": 45500,
    "Mazda MX-30 Long Range": 45500,
    "Mazda MX-30 Performance": 56000,
    "Mazda MX-30 Ultra": 56000,
    "Mazda MX-30 Sport": 70000,
    "Mazda MX-30": 35000,
    "Subaru Solterra Long Range": 58500,
    "Subaru Solterra Sport": 90000,
    "Subaru Solterra Ultra": 72000,
    "Subaru Solterra": 45000,
    "Subaru Solterra Performance": 72000,
    "Subaru Solterra GT": 90000,
    "Subaru Solterra Plaid": 90000,
    "Subaru Solterra Pro": 58500,
    # Mobile
    "iPhone 15 Pro": 1038,
    "iPhone 15 Mini": 639,
    "iPhone 15 FE": 799,
    "iPhone 15": 799,
    "iPhone 15 Lite": 639,
    "iPhone 14": 699,
    "iPhone 14 FE": 699,
    "iPhone 14 Pro Max": 1118,
    "iPhone 14 Lite": 559,
    "iPhone 14 Pro": 908,
    "Galaxy S24 Lite": 639,
    "Galaxy S24 Pro": 1038,
    "Galaxy S24 Ultra": 1278,
    "Galaxy S24 FE": 799,
    "Galaxy S24 Plus": 1038,
    "Galaxy S24": 799,
    "Galaxy S24 Mini": 639,
    "Galaxy Z Fold Plus": 1950,
    "Galaxy Z Fold": 1500,
    "Galaxy Z Fold FE": 1500,
    "Galaxy Z Fold Lite": 1200,
    "Galaxy Z Fold Pro Max": 2400,
    "Galaxy Z Fold Pro": 1950,
    "Galaxy Z Fold Ultra": 2400,
    "Galaxy Z Fold Mini": 1200,
    "Pixel 8 Pro": 908,
    "Pixel 8": 699,
    "Pixel 8 Plus": 908,
    "Pixel 8 Pro Max": 1118,
    "Pixel 8 FE": 699,
    "Pixel Fold Plus": 1820,
    "Pixel Fold Pro": 1820,
    "Pixel Fold Ultra": 2240,
    "Pixel Fold Lite": 1120,
    "Pixel Fold FE": 1400,
    "Pixel Fold Mini": 1120,
    "OnePlus 12 Ultra": 1118,
    "OnePlus 12 Plus": 908,
    "OnePlus 12 Pro": 908,
    "OnePlus 12": 699,
    "OnePlus 12 FE": 699,
    "OnePlus 12 Pro Max": 1118,
    "Xiaomi 14": 599,
    "Xiaomi 14 Mini": 479,
    "Xiaomi 14 Ultra": 958,
    "Xiaomi 14 Lite": 479,
    "Xiaomi 14 FE": 599,
    "Asus ROG Phone Pro Max": 1598,
    "Asus ROG Phone Plus": 1298,
    "Asus ROG Phone FE": 999,
    "Asus ROG Phone Mini": 799,
    "Asus ROG Phone Pro": 1298,
    "Asus ROG Phone Ultra": 1598,
    "Sony Xperia Pro Max": 1438,
    "Sony Xperia Plus": 1168,
    "Sony Xperia": 899,
    "Sony Xperia FE": 899,
    "Sony Xperia Lite": 719,
    "Nothing Phone Ultra": 798,
    "Nothing Phone Plus": 648,
    "Nothing Phone Mini": 399,
    "Nothing Phone Lite": 399,
    "Nothing Phone FE": 499,
    "Nothing Phone": 499,
    "Nothing Phone Pro Max": 798,
    "Nothing Phone Pro": 648,
    "Motorola Edge": 599,
    "Motorola Edge Ultra": 958,
    "Motorola Edge Mini": 479,
    "Motorola Edge FE": 599,
    "Motorola Edge Lite": 479,
    "Motorola Edge Pro Max": 958,
    "Huawei Mate": 799,
    "Huawei Mate Lite": 639,
    "Huawei Mate Ultra": 1278,
    "Huawei Mate Plus": 1038,
    "Huawei Mate Pro": 1038,
    "Huawei Mate FE": 799,
    "Huawei Mate Pro Max": 1278,
    "Zenfone Pro": 778,
    "Zenfone Ultra": 958,
    "Zenfone": 599,
    "Zenfone Lite": 479,
    "Zenfone Plus": 778,
    "Zenfone Mini": 479,
    "Vivo X": 699,
    "Vivo X Ultra": 1118,
    "Vivo X Lite": 559,
    "Vivo X Plus": 908,
    "Vivo X Pro Max": 1118,
    "Vivo X Pro": 908,
    "Redmi Note Mini": 239,
    "Redmi Note Pro": 388,
    "Redmi Note Pro Max": 478,
    "Redmi Note Plus": 388,
    "Redmi Note FE": 299,
    "Redmi Note Lite": 239,
    "Oppo Find Lite": 559,
    "Oppo Find Pro Max": 1118,
    "Oppo Find": 699,
    "Oppo Find Mini": 559,
    "Oppo Find Plus": 908,
    "Oppo Find FE": 699,
    "Oppo Find Ultra": 1118,
    "Realme GT Plus": 518,
    "Realme GT Ultra": 638,
    "Realme GT Pro Max": 638,
    "Realme GT Pro": 518,
    "Realme GT Mini": 319,
    "Honor Magic Plus": 778,
    "Honor Magic Pro Max": 958,
    "Honor Magic FE": 599,
    "Honor Magic Pro": 778,
    "Honor Magic Lite": 479,
    "Nokia G": 199,
    "Nokia G Mini": 159,
    "Nokia G Ultra": 318,
    "Nokia G Pro Max": 318,
    "Nokia G Lite": 159,
    "Nokia G Plus": 258,
    "Nokia G Pro": 258,
    # Appliance
    "IceLogic Smart Fridge": 3400, "IceLogic Chest Freezer": 549, "IceLogic Mini Fridge": 299,
    "Whirlpool Smart Fridge": 2800, "Whirlpool Chest Freezer": 499, "Whirlpool Mini Fridge": 250,
    "SmartVortex Dryer v8": 1199, "SmartVortex Front-Load Washer": 1099,
    "LG Electric Dryer": 1050, "LG Mega-Capacity Washer": 1250,
    "AeroTherm Convection Oven": 2799, "AeroTherm Over-Range Microwave": 449,
    "GE Profile Cooktop Oven": 2499, "GE Profile Cooktop Cooktop": 1599,
    "AquaFresh Water Purifier": 319, "AquaFresh Under-Sink Filter": 199,
    "HydroWash 9000 Pro": 1449, "HydroWash 8000 Basic": 899,
    "Samsung Front-Load Washer": 1199, "Samsung Bespoke Fridge Dryer": 1399,
    "AquaFlow Dishwasher X": 949, "AquaFlow Dishwasher Mini": 499,
    "Bosch Dishwasher 800 Series": 1299, "Bosch Dishwasher 300 Series": 899,
    "PureAir HEPA Purifier": 449, "PureAir Tower Filter": 299,
    "AirPure 4000 Purifier": 399, "AirPure 5000 Max": 599,
    "Dyson Purifier Cool": 649, "Dyson Purifier Hot+Cool": 749,
    "PrecisionGrind Coffee System": 579, "PrecisionGrind Espresso": 399,
    "SmartBrew Coffee Station": 629, "SmartBrew Pod Maker": 199,
    "Breville Espresso Machine": 799, "Breville Coffee System": 699,
    "TurboClean Robot Vacuum": 799, "TurboClean Stick Vacuum": 299,
    "Samsung Jet Stick Vacuum": 499, "Samsung JetBot": 899,
    "SmartSous-Vide Precision": 379, "SmartSous-Vide Pro": 499,
    "Anova Sous-Vide Nano": 199, "Anova Sous-Vide Pro": 399,
    "HeatSync Induction Cooktop": 1099, "HeatSync Gas Cooktop": 899,
    "CoolLogic Wine Cabinet": 2199, "CoolLogic Beverage Center": 1499,
    "Brita Water Purifier": 299, "Brita Under-Sink Filter": 150,
    "IceLogic Fridge Pro": 1950,
    "IceLogic Fridge Smart": 1500,
    "IceLogic Fridge Max": 2400,
    "IceLogic Fridge Plus": 1950,
    "IceLogic Fridge Elite": 2400,
    "IceLogic Freezer Compact": 640,
    "IceLogic Freezer Smart": 800,
    "IceLogic Freezer Elite": 1280,
    "IceLogic Freezer Pro": 1040,
    "IceLogic Freezer Eco": 640,
    "IceLogic Freezer Plus": 1040,
    "IceLogic Freezer Max": 1280,
    "SmartVortex Washer": 800,
    "SmartVortex Washer Plus": 1040,
    "SmartVortex Washer Smart": 800,
    "SmartVortex Washer Compact": 640,
    "SmartVortex Washer Elite": 1280,
    "SmartVortex Washer Eco": 640,
    "SmartVortex Washer Max": 1280,
    "SmartVortex Dryer Elite": 1280,
    "SmartVortex Dryer Smart": 800,
    "SmartVortex Dryer Plus": 1040,
    "SmartVortex Dryer Pro": 1040,
    "SmartVortex Dryer Compact": 640,
    "SmartVortex Dryer Eco": 640,
    "SmartVortex Dryer Max": 1280,
    "AeroTherm Oven Pro": 1560,
    "AeroTherm Oven": 1200,
    "AeroTherm Oven Smart": 1200,
    "AeroTherm Oven Plus": 1560,
    "AeroTherm Oven Eco": 960,
    "AeroTherm Microwave Elite": 640,
    "AeroTherm Microwave Compact": 320,
    "AeroTherm Microwave Pro": 520,
    "AeroTherm Microwave": 400,
    "AeroTherm Microwave Plus": 520,
    "AeroTherm Microwave Smart": 400,
    "AeroTherm Microwave Max": 640,
    "AquaFresh Filter Compact": 160,
    "AquaFresh Filter Smart": 200,
    "AquaFresh Filter Pro": 260,
    "AquaFresh Filter": 200,
    "AquaFresh Filter Elite": 320,
    "AquaFresh Filter Plus": 260,
    "AquaFresh Filter Eco": 160,
    "HydroWash Dishwasher Compact": 560,
    "HydroWash Dishwasher Eco": 560,
    "HydroWash Dishwasher Pro": 910,
    "HydroWash Dishwasher Smart": 700,
    "HydroWash Dishwasher Plus": 910,
    "HydroWash Dishwasher": 700,
    "PureAir Purifier Smart": 300,
    "PureAir Purifier Eco": 240,
    "PureAir Purifier Compact": 240,
    "PureAir Purifier Pro": 390,
    "PureAir Purifier Elite": 480,
    "PureAir Purifier": 300,
    "PrecisionGrind Maker Eco": 120,
    "PrecisionGrind Maker Plus": 195,
    "PrecisionGrind Maker": 150,
    "PrecisionGrind Maker Compact": 120,
    "PrecisionGrind Maker Pro": 195,
    "SmartBrew Machine Plus": 156,
    "SmartBrew Machine Elite": 192,
    "SmartBrew Machine Eco": 96,
    "SmartBrew Machine Pro": 156,
    "SmartBrew Machine Max": 192,
    "SmartBrew Machine": 120,
    "TurboClean Vacuum Eco": 320,
    "TurboClean Vacuum Elite": 640,
    "TurboClean Vacuum Plus": 520,
    "TurboClean Vacuum": 400,
    "TurboClean Vacuum Smart": 400,
    "TurboClean Vacuum Pro": 520,
    "SmartSous-Vide Stick Smart": 100,
    "SmartSous-Vide Stick": 100,
    "SmartSous-Vide Stick Eco": 80,
    "SmartSous-Vide Stick Elite": 160,
    "SmartSous-Vide Stick Pro": 130,
    "SmartSous-Vide Stick Max": 160,
    "SmartSous-Vide Stick Compact": 80,
    "SmartSous-Vide Stick Plus": 130,
    "HeatSync Cooktop Eco": 720,
    "HeatSync Cooktop Elite": 1440,
    "HeatSync Cooktop Smart": 900,
    "HeatSync Cooktop Plus": 1170,
    "HeatSync Cooktop Compact": 720,
    "CoolLogic Cooler Eco": 400,
    "CoolLogic Cooler Max": 800,
    "CoolLogic Cooler Pro": 650,
    "CoolLogic Cooler Elite": 800,
    "CoolLogic Cooler": 500,
    "LG Instaview Fridge": 2000,
    "LG Instaview Fridge Max": 3200,
    "LG Instaview Fridge Eco": 1600,
    "LG Instaview Fridge Pro": 2600,
    "LG Instaview Fridge Elite": 3200,
    "LG Instaview Fridge Smart": 2000,
    "LG Instaview Fridge Plus": 2600,
    "LG Instaview Fridge Compact": 1600,
    "Samsung Bespoke Fridge Pro": 2860,
    "Samsung Bespoke Fridge Smart": 2200,
    "Samsung Bespoke Fridge Elite": 3520,
    "Samsung Bespoke Fridge Max": 3520,
    "Samsung Bespoke Fridge Eco": 1760,
    "Samsung Bespoke Fridge Compact": 1760,
    "Samsung Bespoke Fridge Plus": 2860,
    "Whirlpool Cabrio Oven Eco": 480,
    "Whirlpool Cabrio Oven Smart": 600,
    "Whirlpool Cabrio Oven Elite": 960,
    "Whirlpool Cabrio Oven Max": 960,
    "Whirlpool Cabrio Oven Pro": 780,
    "Whirlpool Cabrio Oven": 600,
    "Whirlpool Cabrio Oven Compact": 480,
    "GE Profile Cooktop Elite": 1760,
    "GE Profile Cooktop Max": 1760,
    "GE Profile Cooktop Eco": 880,
    "GE Profile Cooktop Plus": 1430,
    "GE Profile Cooktop Compact": 880,
    "GE Profile Cooktop Smart": 1100,
    "GE Profile Cooktop": 1100,
    "GE Profile Cooktop Pro": 1430,
    "Bosch Serie Dishwasher Compact": 640,
    "Bosch Serie Dishwasher Plus": 1040,
    "Bosch Serie Dishwasher Max": 1280,
    "Bosch Serie Dishwasher Smart": 800,
    "Bosch Serie Dishwasher Elite": 1280,
    "Bosch Serie Dishwasher Pro": 1040,
    "Bosch Serie Dishwasher Eco": 640,
    "KitchenAid Artisan Espresso Compact": 280,
    "KitchenAid Artisan Espresso Max": 560,
    "KitchenAid Artisan Espresso Plus": 455,
    "KitchenAid Artisan Espresso Pro": 455,
    "KitchenAid Artisan Espresso": 350,
    "KitchenAid Artisan Espresso Eco": 280,
    "KitchenAid Artisan Espresso Elite": 560,
    "KitchenAid Artisan Espresso Smart": 350,
    # Industrial
    "RoboArm Compact": 40000,
    "RoboArm v2": 50000,
    "RoboArm Max": 80000,
    "RoboArm Industrial": 100000,
    "RoboArm v1": 40000,
    "RoboArm Heavy-Duty": 65000,
    "Titan CNC Precision": 104000,
    "Titan CNC Compact": 64000,
    "Titan CNC v1": 64000,
    "Titan CNC Heavy-Duty": 104000,
    "Titan CNC Max": 128000,
    "Titan CNC Pro": 104000,
    "GenSet Power Max": 32000,
    "GenSet Power Heavy-Duty": 26000,
    "GenSet Power Precision": 26000,
    "GenSet Power v2": 20000,
    "GenSet Power Compact": 16000,
    "GenSet Power Pro": 26000,
    "HydraPress v2": 40000,
    "HydraPress Max": 64000,
    "HydraPress Heavy-Duty": 52000,
    "HydraPress Precision": 52000,
    "HydraPress Compact": 32000,
    "Vortex Turbine v1": 80000,
    "Vortex Turbine Compact": 80000,
    "Vortex Turbine v2": 100000,
    "Vortex Turbine Precision": 130000,
    "Vortex Turbine Heavy-Duty": 130000,
    "Vortex Turbine Max": 160000,
    "Vortex Turbine Industrial": 200000,
    "Vortex Turbine Pro": 130000,
    "LaserCut Max": 96000,
    "LaserCut Precision": 78000,
    "LaserCut Compact": 48000,
    "LaserCut Heavy-Duty": 78000,
    "LaserCut v2": 60000,
    "LaserCut Pro": 78000,
    "LaserCut Industrial": 120000,
    "LaserCut v1": 48000,
    "DeepDrill Rig Heavy-Duty": 195000,
    "DeepDrill Rig Max": 240000,
    "DeepDrill Rig Industrial": 300000,
    "DeepDrill Rig Pro": 195000,
    "DeepDrill Rig Precision": 195000,
    "DeepDrill Rig Compact": 120000,
    "DeepDrill Rig v1": 120000,
    "SolarArray Precision": 13000,
    "SolarArray v1": 8000,
    "SolarArray Industrial": 20000,
    "SolarArray Pro": 13000,
    "SolarArray v2": 10000,
    "SolarArray Heavy-Duty": 13000,
    "SolarArray Compact": 8000,
    "BioReactor v2": 30000,
    "BioReactor Precision": 39000,
    "BioReactor Max": 48000,
    "BioReactor Industrial": 60000,
    "BioReactor Heavy-Duty": 39000,
    "BioReactor Pro": 39000,
    "BioReactor v1": 24000,
    "ConveyorSync v2": 15000,
    "ConveyorSync Heavy-Duty": 19500,
    "ConveyorSync Max": 24000,
    "ConveyorSync Pro": 19500,
    "ConveyorSync Industrial": 30000,
    "ConveyorSync Precision": 19500,
    "ArcWelder Heavy-Duty": 6500,
    "ArcWelder Max": 8000,
    "ArcWelder Precision": 6500,
    "ArcWelder Industrial": 10000,
    "ArcWelder v1": 4000,
    "PneumoPress Precision": 15600,
    "PneumoPress v1": 9600,
    "PneumoPress Pro": 15600,
    "PneumoPress Industrial": 24000,
    "PneumoPress Heavy-Duty": 15600,
    "PneumoPress v2": 12000,
    "PneumoPress Max": 19200,
    "PneumoPress Compact": 9600,
    "ThermoForge Compact": 20000,
    "ThermoForge Heavy-Duty": 32500,
    "ThermoForge Max": 40000,
    "ThermoForge v1": 20000,
    "ThermoForge Industrial": 50000,
    "ThermoForge v2": 25000,
    "CompressMax Pro": 10400,
    "CompressMax Max": 12800,
    "CompressMax Heavy-Duty": 10400,
    "CompressMax v2": 8000,
    "CompressMax v1": 6400,
    "CompressMax Compact": 6400,
    "CompressMax Industrial": 16000,
    "CompressMax Precision": 10400,
    "DriveSync Pro": 5200,
    "DriveSync Max": 6400,
    "DriveSync Heavy-Duty": 5200,
    "DriveSync v2": 4000,
    "DriveSync v1": 3200,
    "DriveSync Compact": 3200,
    "DriveSync Precision": 5200,
    "DriveSync Industrial": 8000,
    "Siemens PLC Precision": 2600,
    "Siemens PLC Pro": 2600,
    "Siemens PLC Max": 3200,
    "Siemens PLC Heavy-Duty": 2600,
    "Siemens PLC Industrial": 4000,
    "Siemens PLC v2": 2000,
    "ABB Controller v2": 2500,
    "ABB Controller Heavy-Duty": 3250,
    "ABB Controller v1": 2000,
    "ABB Controller Compact": 2000,
    "ABB Controller Industrial": 5000,
    "ABB Controller Precision": 3250,
    "ABB Controller Max": 4000,
    "Fanuc Robot v1": 36000,
    "Fanuc Robot Max": 72000,
    "Fanuc Robot Precision": 58500,
    "Fanuc Robot v2": 45000,
    "Fanuc Robot Compact": 36000,
    "KUKA Arm Pro": 62400,
    "KUKA Arm v2": 48000,
    "KUKA Arm Max": 76800,
    "KUKA Arm Heavy-Duty": 62400,
    "KUKA Arm v1": 38400,
    "Rockwell Drive Precision": 4550,
    "Rockwell Drive Industrial": 7000,
    "Rockwell Drive Pro": 4550,
    "Rockwell Drive Max": 5600,
    "Rockwell Drive v2": 3500,
    "Rockwell Drive Compact": 2800,
}

# Product Suppliers: 4-6 per sector (shared across models, like real life)
# e.g., Best Buy sells both Samsung and LG fridges
PRODUCT_SUPPLIERS = {
    "Automotive": [
        {"name": "AutoNation Certified", "discount_pct": 4, "speed": "Standard (5-10 Days)"},
        {"name": "Carvana Direct", "discount_pct": 7, "speed": "Standard (5-10 Days)"},
        {"name": "Hendrick Automotive Group", "discount_pct": 3, "speed": "2-Day Priority"},
        {"name": "Penske Motor Group", "discount_pct": 5, "speed": "Standard (5-10 Days)"},
        {"name": "Sonic Automotive", "discount_pct": 6, "speed": "2-Day Priority"},
        {"name": "Lithia Motors", "discount_pct": 8, "speed": "Standard (5-10 Days)"},
    ],
    "Industrial": [
        {"name": "Siemens Industrial Hub", "discount_pct": 12, "speed": "Freight (14-30 Days)"},
        {"name": "ABB Global Sales", "discount_pct": 10, "speed": "Freight (14-30 Days)"},
        {"name": "Caterpillar Distribution", "discount_pct": 8, "speed": "LTL Freight (10-21 Days)"},
        {"name": "Rockwell Automation Direct", "discount_pct": 15, "speed": "Freight (14-30 Days)"},
        {"name": "Schneider Electric Commercial", "discount_pct": 11, "speed": "LTL Freight (10-21 Days)"},
    ],
    "Appliance": [
        {"name": "Best Buy Appliance Center", "discount_pct": 10, "speed": "Standard (3-7 Days)"},
        {"name": "Home Depot Pro", "discount_pct": 8, "speed": "Standard (3-7 Days)"},
        {"name": "Lowe's Commercial", "discount_pct": 12, "speed": "Standard (3-7 Days)"},
        {"name": "AJ Madison Direct", "discount_pct": 15, "speed": "Next-Day Air"},
        {"name": "Abt Electronics", "discount_pct": 6, "speed": "2-Day Priority"},
        {"name": "P.C. Richard & Son", "discount_pct": 9, "speed": "Standard (3-7 Days)"},
    ],
    "Mobile": [
        {"name": "Apple Authorized Reseller", "discount_pct": 0, "speed": "Next-Day Air"},
        {"name": "Best Buy Mobile Pro", "discount_pct": 5, "speed": "Next-Day Air"},
        {"name": "Samsung Direct Store", "discount_pct": 8, "speed": "2-Day Priority"},
        {"name": "Verizon Business Solutions", "discount_pct": 10, "speed": "Next-Day Air"},
        {"name": "T-Mobile for Business", "discount_pct": 12, "speed": "2-Day Priority"},
    ],
}

# Real-world cost ranges by sector
COST_STRUCTURE = {
    "Automotive": {
        "installation": (495, 1500),    # Dealer prep, accessories, PDI
        "hauling": (350, 1200),          # Flatbed/enclosed carrier transport
        "shipping": (195, 850),          # Dealer-to-dealer transfer
        "eta_range": (7, 30),            # Days to delivery
    },
    "Industrial": {
        "installation": (2500, 8500),    # Rigging, crane, foundation, alignment
        "hauling": (850, 3500),          # Heavy equipment flatbed
        "shipping": (450, 2200),         # LTL/FTL freight
        "eta_range": (14, 45),
    },
    "Appliance": {
        "installation": (79, 249),       # Water hookup, gas line, electrical
        "hauling": (49, 129),            # Old appliance haul-away
        "shipping": (0, 99),             # Free delivery common above $500
        "eta_range": (3, 10),
    },
    "Mobile": {
        "installation": (0, 49),         # Data transfer, screen protector
        "hauling": (0, 0),               # N/A for handheld
        "shipping": (0, 14.99),          # Small parcel
        "eta_range": (1, 5),
    },
}


def initialize_fault_registry():
    """Generates 500 high-fidelity fault records with realistic professional-grade costs."""
    base_definitions = {
        "Automotive": [
            ("EV_BATT_THERM","Thermal","Battery Coolant Loop Failure",3,4850.0,9.5),
            ("EV_DRIVE_INV","Power Train","Drive Unit Inverter Anomaly",3,6800.0,12.5),
            ("SUSP_AIR_LEAK","Chassis","Active Air Suspension Leak",3,3200.0,6.5),
            ("ERR_OBC_FAIL","Charging","On-Board Charger Failure",3,2450.0,4.5),
            ("P0700","Transmission","TCM/PDK Control Malfunction",3,2400.0,10.5),
            ("U0100","Communication","High-Voltage Gateway Comm Loss",3,1550.0,5.5),
            ("P0300","Engine","Misfire Cluster Detected ICE",3,125.0,6.6),
            ("P0128","Cooling","Thermostat Rationality Error",1,850.0,2.5),
            ("P0171","Fuel System","Fuel Trim System Lean Bank 1",2,420.0,3.0),
            ("P0420","Exhaust","Catalyst System Efficiency Below Threshold",2,2200.0,4.0),
            ("P0505","Throttle","Idle Control System Malfunction",1,380.0,2.5),
            ("P0340","Ignition","Camshaft Position Sensor Circuit",2,320.0,3.5),
            ("P0455","Emissions","EVAP System Large Leak Detected",2,180.0,2.0),
            ("B0001","Safety","Airbag Deployment Circuit Fault",3,1850.0,6.0),
            ("C0031","Brakes","ABS Wheel Speed Sensor Fault",2,280.0,2.5),
        ],
        "Mobile": [
            ("ERR_DISP_01","Display","Organic LED Flicker Pro-Grade",1,380.0,1.2),
            ("ERR_BATT_01","Battery","Lithium Ion Cell Swelling",3,245.0,2.0),
            ("ERR_BATT_03","Battery","Degraded Capacity Below 70%",2,225.0,1.4),
            ("ERR_CPU_TEM","Processor","Thermal Throttling Event",3,245.0,1.1),
            ("ERR_WIFI_AN","Networking","Antenna Signal Attenuation",1,195.0,1.8),
            ("ERR_PWR_IC","Power Management","Charge Controller Short Circuit",3,380.0,1.5),
            ("ERR_DISP_BRK","Display","Shattered Display Assembly LTPO OLED",2,650.0,2.5),
            ("ERR_CAM_MOD","Camera","Optical Image Stabilizer Failure",2,320.0,1.8),
            ("ERR_USB_C","Charging","USB-C Port Debris Pin Damage",1,95.0,0.8),
            ("ERR_FACE_ID","Biometrics","TrueDepth Camera Misalignment",2,480.0,2.2),
            ("ERR_SPKR_BLW","Audio","Speaker Voice Coil Blown",1,145.0,1.2),
        ],
        "Appliance": [
            ("E1","Water System","Inlet Valve Obstruction",2,145.0,3.5),
            ("E2","Drainage","Sump Pump Timeout",2,350.0,4.2),
            ("E4","Motor","Drum Induction Error",3,585.0,4.8),
            ("E6","Heating","Thermal Fuse Blown",3,125.0,2.2),
            ("ERR_APP_CORE","Heating","Severe Component Corrosion",3,450.0,5.5),
            ("F1","Latch","Door Interlock Failure",2,220.0,2.5),
            ("F2","Fan","Convection Blower Jammed",1,125.0,2.5),
            ("E7","Control","Control Board Memory Fault",3,380.0,4.0),
            ("E9","Sensor","NTC Thermistor Open Circuit",2,55.0,1.5),
            ("ERR_ICE_MKR","Ice System","Ice Maker Auger Motor Seized",2,195.0,2.8),
            ("ERR_DISP_APP","Display","Touchscreen Panel Fault",1,165.0,2.0),
            ("ERR_CMPRS","Refrigeration","Compressor Start Relay Failure",3,425.0,5.0),
            ("ERR_SEAL_LK","Seals","Door Gasket Seal Degradation",1,85.0,1.5),
        ],
        "Industrial": [
            ("VIB_100","Drive Train","Shaft Dynamic Misalignment",3,6850.0,24.5),
            ("PF_01","Power Train","Phase Sequence Imbalance",3,7200.0,28.3),
            ("LV_02","Pneumatics","Pressure Line Blockage",3,4525.0,15.2),
            ("PR_200","Hydraulics","Pump Cavitation Warning",2,8500.0,18.6),
            ("ERR_IND_HYD_L","Hydraulics","Hydraulic Line Rupture or Wear",3,4150.0,14.5),
            ("VFD_01","VFD","Inverter Arc Fault",3,12240.0,32.1),
            ("HMI_COM","Control","Interface Bus Timeout",1,4138.0,15.7),
            ("ERR_IND_BEAR","Bearings","Rolling Element Bearing Failure",3,2850.0,18.0),
            ("ERR_IND_SEAL","Seals","High-Pressure Seal Extrusion",2,1250.0,8.5),
            ("ERR_IND_COOL","Cooling","Coolant Flow Restriction Heavy",3,1850.0,10.0),
            ("ERR_IND_OVER","Electrical","Motor Overload Trip",3,3200.0,12.0),
            ("ERR_IND_VIBX","Vibration","Excessive Vibration X-Axis",2,950.0,6.0),
            ("ERR_IND_PLC","Control","PLC Firmware Fault",2,2450.0,8.0),
            ("ERR_IND_SEN","Sensor","Proximity Sensor Drift",1,320.0,3.0),
            ("ERR_IND_GEAR","Gearbox","Gearbox Oil Contamination",3,3850.0,16.0),
        ]
    }

    TARGET = 500
    registry = []
    per_sector = TARGET // 4

    for domain, codes in base_definitions.items():
        for code, sys, cause, sev, parts_cost, labor_h in codes:
            registry.append({"fault_code": code, "device_type": domain,
                "system_affected": sys, "root_cause": cause,
                "severity": sev, "avg_parts_cost": parts_cost, "avg_labor_hours": labor_h})
        for i in range(per_sector - len(codes)):
            base = random.choice(codes)
            variant_code = f"{base[0]}_V{i+1:03d}"
            parts_cost = round(base[4] * random.uniform(0.8, 1.2), 2)
            labor_h = round(base[5] * random.uniform(0.85, 1.15), 1)
            registry.append({"fault_code": variant_code, "device_type": domain,
                "system_affected": base[1], "root_cause": base[2] + " (Variant)",
                "severity": base[3], "avg_parts_cost": parts_cost, "avg_labor_hours": labor_h})

    df = pd.DataFrame(registry[:TARGET])
    df.to_csv(f"{DATA_DIR}/fault_labels.csv", index=False)
    print(f"  fault_labels.csv: {len(df)} records written.")
    return df


def generate_parts_catalog():
    """Generates 500 high-fidelity parts with realistic OEM pricing and multi-brand alternatives."""
    TARGET = 500
    base_parts = [
        # (description, device_type, system, [(brand, base_price), ...])
        ("High-Voltage Inverter Plate","Automotive","Power Train",[("BorgWarner",6200),("Hitachi",5800),("Bosch",5650)]),
        ("Rear Axle Drive Module","Automotive","Power Train",[("Magna",8500),("Dana",7200),("ZF",7800)]),
        ("PDK Transmission Clutch Pack","Automotive","Power Train",[("Aisin",3200),("ZF",2950),("Valeo",2800)]),
        ("Ceramic Composite Brake Pad Set","Automotive","Chassis",[("Brembo",1250),("Akebono",950),("Ferodo",1100)]),
        ("Active Air Suspension Strut","Automotive","Chassis",[("Continental",2800),("Bilstein",2100),("Sachs",2300)]),
        ("6-Piston Aluminum Caliper","Automotive","Chassis",[("Brembo",1850),("Wilwood",1650),("AP Racing",1980)]),
        ("Sport Tire Set (Performance Spec)","Automotive","Chassis",[("Michelin",450),("Pirelli",420),("Continental",410)]),
        ("High-Voltage Coolant Heater","Automotive","Thermal",[("Mahle",1850),("Denso",1450),("Modine",1380)]),
        ("Thermal Management Module","Automotive","Thermal",[("Bosch",1200),("Valeo",1100),("Mahle",1050)]),
        ("7.2kW On-Board Charger","Automotive","Charging",[("Eaton",2250),("Delta",1950),("Rectifier EV",1800)]),
        ("DC Fast Charge Port Assembly","Automotive","Charging",[("Bosch",850),("TE Connectivity",780),("Amphenol",820)]),
        ("High-Precision Ignition Coil (M4)","Automotive","Engine",[("Bosch",125),("NGK",115),("Delphi",118)]),
        ("Silver-Electrode Spark Plug (BMW)","Automotive","Engine",[("Bosch",45),("NGK",38),("Denso",42)]),
        ("Direct Fuel Injector (ICE)","Automotive","Engine",[("Denso",350),("Bosch",340),("Delphi",330)]),
        ("Turbo-Charged Intake Valve","Automotive","Engine",[("Bosch",1250),("Valeo",1100),("Gates",1150)]),
        ("Coolant Control Valve","Automotive","Cooling",[("Continental",850),("Gates",780),("Dorman",720)]),
        ("OEM Precision Thermostat","Automotive","Cooling",[("Bosch",420),("Gates",395),("Wahler",380)]),
        ("Performance Radiator Core","Automotive","Cooling",[("Mishimoto",650),("Koyo",620),("CSF",590)]),
        ("Direct-Shift Transmission Unit","Automotive","Transmission",[("Aisin",2400),("ZF",2250),("Jatco",2100)]),
        ("Torque Converter Assembly","Automotive","Transmission",[("Valeo",1200),("Exedy",1150),("Schaeffler",1250)]),
        ("ABS Wheel Speed Sensor","Automotive","Brakes",[("Bosch",280),("Delphi",255),("Meyle",240)]),
        ("Brake Master Cylinder","Automotive","Brakes",[("ATE",380),("TRW",350),("Ate-Teves",370)]),
        ("SRS Airbag Module","Automotive","Safety",[("Autoliv",1850),("TRW",1750),("ZF",1800)]),
        ("Seatbelt Pre-Tensioner","Automotive","Safety",[("Autoliv",420),("TRW",395),("Takata",380)]),
        ("Fuel System Pressure Sensor","Automotive","Fuel System",[("Bosch",420),("Delphi",380),("Siemens VDO",395)]),
        ("High-Pressure Fuel Pump (EV)","Automotive","Fuel System",[("Delphi",950),("Bosch",880),("Denso",860)]),
        ("Catalytic Converter (OEM Spec)","Automotive","Exhaust",[("Walker",2200),("Magneti-Marelli",1950),("Eastern",1800)]),
        ("Lambda / O2 Sensor","Automotive","Exhaust",[("Bosch",95),("Denso",88),("NGK",92)]),
        ("Central Gateway (High-Voltage)","Automotive","Communication",[("Aptiv",1450),("Continental",950),("Bosch",980)]),
        ("Electronic Throttle Body","Automotive","Throttle",[("Bosch",380),("Denso",360),("Siemens VDO",370)]),
        ("EVAP Canister Purge Valve","Automotive","Emissions",[("Bosch",180),("ACDelco",160),("Delphi",170)]),
        ("Camshaft Position Sensor","Automotive","Ignition",[("Bosch",320),("Delphi",295),("Standard Motor",305)]),
        ("LTPO Pro-Grade OLED Panel","Mobile","Display",[("Samsung Display",450),("LG Display",420),("BOE",395)]),
        ("Retina XDR Display Assembly","Mobile","Display",[("Apple Certified",480),("JDI",440),("Sharp",450)]),
        ("5000mAh High-Density Battery","Mobile","Battery",[("Samsung SDI",95),("ATL",88),("CATL",92)]),
        ("Smart Battery Case Module","Mobile","Battery",[("Apple Certified",110),("Desay",98),("Sunwoda",95)]),
        ("3700mAh Flagship Battery Cell","Mobile","Battery",[("Murata",85),("TDK",80),("Panasonic",88)]),
        ("Snapdragon 8 Gen 3 Logic Board","Mobile","Processor",[("Qualcomm",680),("TSMC OEM",650),("Samsung Fab",640)]),
        ("A17 Pro Bionic Logic Board","Mobile","Processor",[("Apple Certified",720),("TSMC OEM",695),("Foxconn",680)]),
        ("48MP Camera Sensor Module","Mobile","Camera",[("Sony",320),("OmniVision",295),("Samsung LSI",305)]),
        ("Periscope Telephoto Module","Mobile","Camera",[("Samsung",380),("LG Innotek",360),("Sunny Optical",340)]),
        ("TrueDepth Camera Array","Mobile","Biometrics",[("Apple Certified",480),("Sony",445),("STMicro",430)]),
        ("Under-Display Fingerprint Sensor","Mobile","Biometrics",[("Qualcomm",220),("Goodix",195),("ISSI",185)]),
        ("USB-C Charging Port Assembly","Mobile","Charging",[("Apple Certified",95),("Foxconn",82),("Amphenol",88)]),
        ("MagSafe Wireless Coil Assembly","Mobile","Charging",[("Apple Certified",145),("TDK",128),("Witricity",135)]),
        ("Wi-Fi 7 Antenna Assembly","Mobile","Networking",[("Qualcomm",195),("Murata",178),("TDK",185)]),
        ("5G mmWave Antenna Kit","Mobile","Networking",[("Qualcomm",285),("Samsung LSI",265),("MediaTek",258)]),
        ("Speaker Receiver Module","Mobile","Audio",[("Apple Certified",145),("GoerTek",128),("AAC Tech",132)]),
        ("Haptic Feedback Assembly","Mobile","Audio",[("Apple Certified",95),("AAC Tech",82),("GoerTek",88)]),
        ("Power Management IC","Mobile","Power Management",[("Texas Instruments",380),("Qualcomm",355),("MaxLinear",340)]),
        ("Voltage Regulator Module","Mobile","Power Management",[("Texas Instruments",220),("Renesas",205),("Analog Devices",215)]),
        ("60Hz Active VFD Inverter","Industrial","VFD",[("Siemens",12240),("ABB",11800),("Rockwell",12000)]),
        ("VFD Thyristor Stack","Industrial","VFD",[("Siemens",2450),("ABB",2300),("Schneider",2380)]),
        ("VFD Control Card","Industrial","VFD",[("Siemens",1850),("ABB",1750),("Fuji Electric",1800)]),
        ("Precision Frequency Drive (High-Torque)","Industrial","Drive",[("ABB",6850),("Siemens",6500),("Danfoss",6200)]),
        ("Servo Drive Amplifier","Industrial","Drive",[("Siemens",4200),("Fanuc",4500),("Mitsubishi",4300)]),
        ("High-Pressure Hydraulic Pump","Industrial","Hydraulics",[("Caterpillar",8500),("Parker",7800),("Bosch Rexroth",8100)]),
        ("Hydraulic Line Pressure Hose (HP)","Industrial","Hydraulics",[("Parker",1250),("Gates",1150),("Eaton",1200)]),
        ("Hydraulic Accumulator","Industrial","Hydraulics",[("Bosch Rexroth",2200),("Parker",2050),("Hydac",2150)]),
        ("Digital Pressure Control Node","Industrial","Control",[("Schneider",3025),("Siemens",2900),("Omron",2850)]),
        ("CompactLogix HMI Interface","Industrial","Control",[("Rockwell",4138),("Siemens",3950),("Mitsubishi",3800)]),
        ("S7-1500 PLC CPU Module","Industrial","Control",[("Siemens",2450),("Allen-Bradley",2650),("Omron",2350)]),
        ("Precision Angular Contact Bearing","Industrial","Bearings",[("SKF",2850),("FAG",2650),("NSK",2750)]),
        ("Cylindrical Roller Bearing (Large)","Industrial","Bearings",[("SKF",1850),("FAG",1750),("Timken",1800)]),
        ("High-Pressure Rotary Seal Kit","Industrial","Seals",[("Parker",1250),("Trelleborg",1150),("Freudenberg",1200)]),
        ("Shaft Lip Seal Set","Industrial","Seals",[("Parker",280),("Trelleborg",260),("NOK",270)]),
        ("Industrial Cooling Pump (Heavy)","Industrial","Cooling",[("Siemens",1850),("Armstrong",1700),("Grundfos",1780)]),
        ("Heat Exchanger Core Module","Industrial","Cooling",[("Alfa Laval",3200),("GEA",3050),("Kelvion",3100)]),
        ("Motor Overload Relay","Industrial","Electrical",[("Siemens",3200),("ABB",2950),("Schneider",3050)]),
        ("High-Current Circuit Breaker","Industrial","Electrical",[("ABB",1850),("Siemens",1780),("Schneider",1820)]),
        ("Vibration Transducer X-Axis","Industrial","Vibration",[("Vibro-Meter",950),("Bruel and Kjaer",1050),("PCB Piezotronics",980)]),
        ("Continuous Online Vibration Monitor","Industrial","Vibration",[("SKF",2800),("Emerson",2650),("Fluke",2700)]),
        ("Inductive Proximity Sensor","Industrial","Sensor",[("IFM",320),("Omron",295),("Turck",305)]),
        ("Precision Multi-Axis Load Cell","Industrial","Sensor",[("HBM",2450),("Parker",2250),("Kistler",2350)]),
        ("Ultrasonic Level Sensor","Industrial","Sensor",[("Endress+Hauser",850),("VEGA",820),("Siemens",800)]),
        ("Industrial Gearbox Assembly","Industrial","Gearbox",[("Bonfiglioli",3850),("Flender",4100),("Sumitomo",3950)]),
        ("Planetary Reduction Gearhead","Industrial","Gearbox",[("Apex Dynamics",2200),("Neugart",2350),("Wittenstein",2450)]),
        ("Precision Pressure Regulator","Industrial","Pneumatics",[("Festo",580),("SMC",550),("Parker",565)]),
        ("5/2 Solenoid Valve","Industrial","Pneumatics",[("Festo",320),("SMC",295),("Parker",310)]),
        ("Direct-Drive Induction Motor","Appliance","Motor",[("Whirlpool",585),("LG",545),("Bosch",560)]),
        ("Brushless DC Circulator Motor","Appliance","Motor",[("Nidec",380),("Regal Beloit",360),("ABB",370)]),
        ("Smart Inverter Control Board","Appliance","Heating",[("LG",450),("Samsung",420),("Bosch",430)]),
        ("Oven Main Support Board","Appliance","Heating",[("GE",395),("Samsung",420),("Whirlpool",410)]),
        ("Thermal Fuse (Safety Cutout)","Appliance","Heating",[("Therm-O-Disc",125),("Limitor",115),("Selco",120)]),
        ("Core Sump Drainage Pump","Appliance","Drainage",[("Maytag",350),("Whirlpool",325),("LG",335)]),
        ("Drain Valves (Dual-Port)","Appliance","Drainage",[("Fluid Systems",85),("Whirlpool",78),("Electrolux",82)]),
        ("Inlet Water Valve (Dual Coil)","Appliance","Water System",[("Aqua-Pure",145),("Whirlpool",135),("Kenmore",140)]),
        ("Water Level Pressure Switch","Appliance","Water System",[("Gems Sensors",65),("Whirlpool",60),("Emerson",62)]),
        ("Door Latch / Interlock Assembly","Appliance","Latch",[("Whirlpool",220),("Fisher & Paykel",205),("Electrolux",212)]),
        ("Magnetic Door Lock Solenoid","Appliance","Latch",[("Sirai",95),("RSA",85),("Custom Coils",90)]),
        ("Convection Blower Motor","Appliance","Fan",[("ERP",125),("Whirlpool",118),("Frigidaire",122)]),
        ("Condenser Fan Motor","Appliance","Fan",[("Nidec",145),("AO Smith",138),("Fasco",142)]),
        ("Main Control Board","Appliance","Control",[("LG",380),("Samsung",365),("Whirlpool",372)]),
        ("IoT Connectivity Module","Appliance","Control",[("Bosch ConnectedControl",220),("Belimo",210),("Schneider",215)]),
        ("NTC Thermistor (OEM)","Appliance","Sensor",[("Semitec",50),("Elpida",55),("Murata",52)]),
        ("Load Cell Weight Sensor","Appliance","Sensor",[("HBK",95),("Mettler Toledo",110),("Vishay",98)]),
        ("Ice Maker Auger Motor","Appliance","Ice System",[("Whirlpool",195),("GE",182),("Frigidaire",188)]),
        ("Ice Level Optical Sensor","Appliance","Ice System",[("Whirlpool",65),("LG",60),("Samsung",62)]),
        ("LCD Touch Control Panel","Appliance","Display",[("Samsung",165),("LG",158),("Sharp Display",162)]),
        ("LED Status Display Module","Appliance","Display",[("Tianma",95),("BOE",88),("AUO",92)]),
        ("Scroll Compressor Start Relay","Appliance","Refrigeration",[("Danfoss",425),("Embraco",395),("Tecumseh",410)]),
        ("Evaporator Coil Assembly","Appliance","Refrigeration",[("Whirlpool",580),("LG",550),("Heatcraft",560)]),
        ("Refrigerator Door Gasket Seal","Appliance","Seals",[("Whirlpool",85),("Frigidaire",78),("LG",82)]),
        ("Pump O-Ring and Seal Kit","Appliance","Seals",[("Parker",45),("Trelleborg",42),("NOK",44)]),
    ]

    parts_data = []
    part_counter = {}
    for description, device_type, system, brand_prices in base_parts:
        for brand, base_price in brand_prices:
            key = f"{device_type[:3]}_{system[:3]}".upper().replace(" ", "")
            part_counter[key] = part_counter.get(key, 0) + 1
            p_id = f"PRT_{key}_{part_counter[key]:04d}"
            price = round(base_price * random.uniform(0.97, 1.03), 2)
            supplier = SUPPLIERS.get(device_type, ["Local Authorized Dealer"])[int(hashlib.md5(p_id.encode()).hexdigest(), 16) % len(SUPPLIERS.get(device_type, ["Local Authorized Dealer"]))]
            # Condition: OEM base parts are typically New or Certified Pre-Owned
            condition = random.choices(
                ["New", "Certified Pre-Owned", "Refurbished", "Never Used (Old Stock)", "Used"],
                weights=[50, 20, 15, 10, 5]
            )[0]
            # Adjust price by condition
            condition_multiplier = {"New": 1.0, "Certified Pre-Owned": 0.82, "Refurbished": 0.68, "Never Used (Old Stock)": 0.90, "Used": 0.55}
            price = round(price * condition_multiplier[condition], 2)
            parts_data.append({"part_number": p_id, "brand": brand, "description": description,
                "device_type": device_type, "system": system, "price_oem": price,
                "in_stock": random.choices([True, False], weights=[75, 25])[0],
                "supplier": supplier, "condition": condition,
                "base_price_raw": base_price}) # Anchor for variant consistency

    # Fill to TARGET=500 with variants
    while len(parts_data) < TARGET:
        base = random.choice(parts_data)
        key = f"{base['device_type'][:3]}_{base['system'][:3]}".upper().replace(" ", "")
        part_counter[key] = part_counter.get(key, 0) + 1
        variant = dict(base)
        variant['part_number'] = f"PRT_{key}_{part_counter[key]:04d}_V"
        variant['supplier'] = SUPPLIERS.get(base['device_type'], ["Local Authorized Dealer"])[int(hashlib.md5(variant['part_number'].encode()).hexdigest(), 16) % len(SUPPLIERS.get(base['device_type'], ["Local Authorized Dealer"]))]
        variant['condition'] = random.choices(
            ["New", "Certified Pre-Owned", "Refurbished", "Never Used (Old Stock)", "Used"],
            weights=[40, 20, 20, 10, 10]
        )[0]
        # RE-CALCULATE PRICE: Base MSRP * Random Noise * Condition Multiplier
        condition_multiplier = {"New": 1.0, "Certified Pre-Owned": 0.82, "Refurbished": 0.68, "Never Used (Old Stock)": 0.90, "Used": 0.55}
        raw_price_with_noise = base['base_price_raw'] * random.uniform(0.95, 1.05)
        variant['price_oem'] = round(raw_price_with_noise * condition_multiplier[variant['condition']], 2)
        parts_data.append(variant)

    df = pd.DataFrame(parts_data[:TARGET])
    df.to_csv(f"{DATA_DIR}/parts_catalog.csv", index=False)
    print(f"  parts_catalog.csv: {len(df)} records written.")
    return df

def generate_supplier_database():
    """Generates realistic metrics for all suppliers in the ecosystem, including Product suppliers."""
    import hashlib
    records = []
    
    # 1. Parts suppliers (existing)
    for sector, vendors in SUPPLIERS.items():
        for vendor in vendors:
            h = int(hashlib.md5(vendor.encode()).hexdigest(), 16)
            rating = ["A+", "A", "B+", "B"][h % 4]
            otd = 90.0 + (h % 95) / 10.0
            defect = 1.0 + (h % 30) / 10.0
            discounts = ["10% Enterprise Vol", "5% Preferred Partner", "Net-30 Terms", "No Auth Discount"]
            discount = discounts[h % len(discounts)]
            speeds = ["Next-Day Air", "2-Day Priority", "Standard (3-5 Days)"]
            speed = speeds[h % len(speeds)]
            records.append({
                "supplier_name": vendor, "sector": sector, "supplier_type": "Parts",
                "rating": rating, "on_time_pct": round(otd, 1), "defect_rate_pct": round(defect, 1),
                "active_discount": discount, "speed_class": speed,
            })
    
    # 2. Product suppliers (new — real-world distributors)
    for sector, supplier_list in PRODUCT_SUPPLIERS.items():
        for sup in supplier_list:
            h = int(hashlib.md5(sup["name"].encode()).hexdigest(), 16)
            rating = ["A+", "A", "A", "B+"][h % 4]  # Product suppliers tend to be higher rated
            otd = 92.0 + (h % 80) / 10.0
            defect = 0.5 + (h % 20) / 10.0
            discount = f"{sup['discount_pct']}% Volume"
            records.append({
                "supplier_name": sup["name"], "sector": sector, "supplier_type": "Product",
                "rating": rating, "on_time_pct": round(otd, 1), "defect_rate_pct": round(defect, 1),
                "active_discount": discount, "speed_class": sup["speed"],
            })
    
    # 3. Bulk-generate additional generic suppliers to fill out the ecosystem (for variety)
    generic_prefixes = ["Apex", "Titan", "Nexus", "Rapid", "Elite", "Core", "Prime", "Smart", "Dynamic", "Global",
                        "Vortex", "Omni", "Eco", "Precision", "Structural", "Optimal", "Advanced", "Summit", "Unified", "Industrial"]
    generic_suffixes = ["Solutions", "Parts", "Supply", "Engineering", "Networks", "Industries", "Tech", "Components",
                        "Services", "Manufacturing", "Systems", "Logistics", "Works", "Resources", "Enterprises", "Dynamics"]
    generic_entity = ["Inc.", "LLC", "Corp.", "Ltd.", "Group", "Co.", "Partners", "International", "Global", "Solutions"]
    
    for sector in ["Automotive", "Industrial", "Appliance", "Mobile"]:
        for sup_type in ["Parts", "Product"]:
            for _ in range(120):
                name = f"{random.choice(generic_prefixes)} {random.choice(generic_suffixes)} {random.choice(generic_entity)}"
                h = int(hashlib.md5(name.encode()).hexdigest(), 16)
                rating = ["A+", "A", "B+", "B"][h % 4]
                otd = 90.0 + (h % 95) / 10.0
                defect = 1.0 + (h % 30) / 10.0
                discounts = ["10% Enterprise Vol", "5% Preferred Partner", "Net-30 Terms", "No Auth Discount"]
                speeds = ["Next-Day Air", "2-Day Priority", "Standard (3-5 Days)"]
                records.append({
                    "supplier_name": name, "sector": sector, "supplier_type": sup_type,
                    "rating": rating, "on_time_pct": round(otd, 1), "defect_rate_pct": round(defect, 1),
                    "active_discount": discounts[h % len(discounts)], "speed_class": speeds[h % len(speeds)],
                })
    
    df = pd.DataFrame(records)
    df = df.drop_duplicates(subset=["supplier_name", "sector", "supplier_type"])
    df.to_csv(f"{DATA_DIR}/supplier_database.csv", index=False)
    print(f"  supplier_database.csv: {len(df)} records written.")
    return df

def apply_domain_fingerprint(fault_code, temp, vibration, pressure, current):
    h_idx = sum(ord(c) for c in fault_code)
    temp += (h_idx % 25) * 1.5
    vibration += (h_idx % 15) * 0.4
    pressure += (h_idx % 20) * 2.0
    current += (h_idx % 12) * 0.8
    return temp, vibration, pressure, current


def generate_telemetry_stream(fault_registry):
    """
    Uses sector-specific physics engines to generate domain-accurate telemetry.
    IMPORTANT: Only uses canonical base fault codes (not variants) for ML training accuracy.
    More samples per class = dramatically higher diagnostic accuracy.
    """
    # Only use base (non-variant) fault codes for ML training
    base_registry = fault_registry[~fault_registry['fault_code'].str.contains('_V\\d{3}', regex=True)].copy()
    print(f"  Using {len(base_registry)} canonical fault codes for training ({RECORDS_COUNT // len(base_registry):.0f} samples/class)")
    stream_records = []
    for i in range(RECORDS_COUNT):
        profile = base_registry.sample(1).iloc[0]
        domain = profile["device_type"]
        sys = profile["system_affected"]
        fault_code = profile["fault_code"]
        l_rate = LABOR_RATES.get(domain, 150)
        load = random.uniform(5, 95)
        if domain == "Mobile":
            voltage = random.uniform(3.5, 4.2); temp = 25 + (load * 0.4); current = (load * 0.05)
            rpm, pressure, o2, coolant = 0.0, 0.0, 0.0, 0.0; batt_health = random.uniform(60, 100); freq = 0.0
        elif domain == "Automotive":
            voltage = random.uniform(12.6, 14.4); temp = 70 + (load * 0.3); current = 20 + (load * 0.5)
            rpm = 800 + (load * 30); pressure = 30 + (load * 0.5); o2 = 0.9 + random.uniform(0.1, 0.2)
            coolant = temp - 10; batt_health = random.uniform(85, 100); freq = 0.0
        elif domain == "Industrial":
            voltage = 480 + random.normalvariate(0, 5); temp = 40 + (load * 0.6); current = 100 + (load * 2.5)
            rpm = 1200 + (load * 45); pressure = 100 + (load * 5.0); o2 = 0.0
            coolant = temp + 5.0; batt_health = 100.0; freq = 50.0 + random.uniform(-0.1, 0.1)
        else:
            voltage = random.choice([110, 220]) + random.normalvariate(0, 1); temp = 18 + (load * 0.25)
            current = 5 + (load * 0.1); rpm = 400 + (load * 5) if "Motor" in profile.get("root_cause","") else 0.0
            pressure = 15 + (load * 0.2); o2 = 0.0; coolant = 0.0; batt_health = 100.0; freq = 60.0
        vibration = (load * 0.02) + random.uniform(0, 0.5)
        temp, vibration, pressure, current = apply_domain_fingerprint(fault_code, temp, vibration, pressure, current)
        if domain == "Mobile" and sys == "Battery": batt_health *= 0.5; temp += 25.0
        if domain == "Automotive" and "Misfire" in profile.get("root_cause",""): vibration *= 3.5; rpm *= 0.85
        if domain == "Industrial" and "Misalignment" in profile.get("root_cause",""): vibration *= 10.0
        age = random.randint(0, 10)
        parts_cost = float(profile["avg_parts_cost"]); labor_h = float(profile["avg_labor_hours"])
        base_cost = parts_cost + (labor_h * l_rate)
        age_penalty = base_cost * (age * 0.035)
        load_penalty = base_cost * ((load - 50) * 0.005) if load > 50 else 0
        total_cost = round(base_cost + age_penalty + load_penalty, 2)
        # Product condition is age-weighted: newer machines are more likely to be in good shape
        if age <= 1:
            condition_weights = [60, 25, 10, 5, 0]   # mostly New / Certified Pre-Owned
        elif age <= 4:
            condition_weights = [20, 35, 25, 10, 10]  # mix
        else:
            condition_weights = [5, 15, 30, 15, 35]   # older machines are often Used / Refurbished
        product_condition = random.choices(
            ["New", "Certified Pre-Owned", "Refurbished", "Never Used (Old Stock)", "Used"],
            weights=condition_weights
        )[0]
        
        # Select product model and look up real MSRP
        model_name = random.choice(MODEL_REGISTRY.get(domain, ["Generic Model"]))
        product_msrp = MSRP_MAP.get(model_name, 1000)
        
        # Assign one of 4-6 product suppliers for this sector
        supplier_pool = PRODUCT_SUPPLIERS.get(domain, [{"name": "Local Dealer", "discount_pct": 0, "speed": "Standard"}])
        chosen_supplier = random.choice(supplier_pool)
        market_supplier = chosen_supplier["name"]
        discount_pct = chosen_supplier["discount_pct"] + random.uniform(-1, 2)  # slight variance
        discount_pct = round(max(0, min(discount_pct, 20)), 1)
        
        # Cost decomposition using real-world sector ranges
        costs = COST_STRUCTURE.get(domain, COST_STRUCTURE["Appliance"])
        labor_cost = round(labor_h * l_rate, 2)
        installation_cost = round(random.uniform(*costs["installation"]), 2)
        hauling_cost = round(random.uniform(*costs["hauling"]), 2)
        shipping_cost = round(random.uniform(*costs["shipping"]), 2)
        actual_price = product_msrp
        after_discount_cost = round(actual_price * (1 - discount_pct / 100), 2)
        eta_days = random.randint(*costs["eta_range"])
        
        stream_records.append({
            "service_id": f"SR_{i:06d}", "device_type": domain,
            "model_name": model_name,
            "product_msrp": product_msrp,
            "fault_code": fault_code, "telemetry_temp": round(temp, 2), "telemetry_rpm": round(rpm, 0),
            "telemetry_voltage": round(voltage, 2), "telemetry_vibration": round(vibration, 4),
            "telemetry_pressure": round(pressure, 2), "telemetry_current": round(current, 2),
            "telemetry_freq": round(freq, 2), "telemetry_o2": round(o2, 3),
            "telemetry_battery": round(batt_health, 1), "telemetry_coolant": round(coolant, 2),
            "telemetry_load_pct": round(load, 1), "age_years": age,
            "product_condition": product_condition,
            "product_supplier": market_supplier,
            "market_supplier": market_supplier,
            "labor_cost": labor_cost,
            "installation_cost": installation_cost,
            "hauling_cost": hauling_cost,
            "shipping_cost": shipping_cost,
            "discount_pct": discount_pct,
            "actual_price": actual_price,
            "after_discount_cost": after_discount_cost,
            "eta_days": eta_days,
            "parts_expenditure": parts_cost, "labor_duration": labor_h, "total_service_cost": total_cost
        })
    pd.DataFrame(stream_records).to_csv(f"{DATA_DIR}/repair_records.csv", index=False)
    print(f"  repair_records.csv: {RECORDS_COUNT} records written.")


def generate_raw_sensor_stream():
    start_time = datetime.now() - timedelta(hours=12)
    sensor_records = []
    for i in range(SENSORS_COUNT):
        s_type = random.choices(["Thermal","Vibration","Pressure","Voltage","Current","RPM"], weights=[3,2,1,2,1,1])[0]
        timestamp = (start_time + timedelta(seconds=i * 2.8)).isoformat()
        if s_type == "Thermal": val = random.uniform(20, 110)
        elif s_type == "Vibration": val = random.uniform(0.01, 12.0)
        elif s_type == "Pressure": val = random.uniform(0, 350)
        elif s_type == "RPM": val = random.uniform(0, 6000)
        else: val = random.uniform(1, 500)
        sensor_records.append({"sensor_id": f"S_{i:06d}", "timestamp": timestamp,
            "device_id": f"DEV_{random.randint(100, 999)}", "sensor_type": s_type, "value": round(val, 4)})
    pd.DataFrame(sensor_records).to_csv(f"{DATA_DIR}/sensor_readings.csv", index=False)
    print(f"  sensor_readings.csv: {SENSORS_COUNT} records written.")


if __name__ == "__main__":
    print("Calibrating Domain Brain (Professional-Grade Injection)...")
    registry = initialize_fault_registry()
    print("Rebuilding Parts Catalog (500 Records)...")
    generate_parts_catalog()
    print("Generating Supplier Intelligence Database...")
    generate_supplier_database()
    print("Generating High-Fidelity Telemetry (50,000 Records)...")
    generate_telemetry_stream(registry)
    print("Synthesizing Live Sensor Stream...")
    generate_raw_sensor_stream()
    print("Global Realism Overhaul Complete.")
