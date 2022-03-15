import board
import adafruit_mcp3xxx.mcp3008 as MCP

# Made conversion dictionaries for convenience.
pins = {
    5: board.D5,
    6: board.D6,
    16: board.D16,
    17: board.D17,
    22: board.D22,
    23: board.D23,
    24: board.D24,
    25: board.D25,
    26: board.D26,
    27: board.D27,
}

channels = {
    0: MCP.P0,
    1: MCP.P1,
    2: MCP.P2,
    3: MCP.P3,
    4: MCP.P4,
    5: MCP.P5,
    6: MCP.P6,
    7: MCP.P7
}

def clamp(x, low, high):
    """
    Binds or 'locks' a value between an upper and lower bound (inclusive).
    x: the value to clamp
    high: upper bound
    low: lower bound
    """
    if x < low: return low
    if x > high: return high
    return x

def voltageToTemp(v: float):
    """
    Converts float voltage to temperature in °C [Single decimal precision]
    Uses the MCP9700A's specifications.

    v: Input voltage from sensor

    V0 (DC Offset for MCP9700A)              = 500mV = 0.5V
    Tc (Temperature Coefficient of MCP9700A) = 10mV/°C

    Temperature (°C) = (V - V0)/Tc

    Output locked between -40 to 150 °C, which is the range of MCP9700A
    """
    return clamp(round((v-0.5)/0.01, 1), -40.0, 150.0)

def voltageToTDS(v: float):
    """
    Converts float voltage to TDS value in ppm [Single decimal precision]
    
    v: Input voltage from sensor
    
    Range of TDS meter = 0 - 1000 ppm
    Vmin = 0.0V
    Vmax = 2.3V
    TDS Value (ppm) = V * ((1000 - 0)/(Vmax - Vmin))
    """
    return clamp(round(v*(1000/2.3), 1), 0.0, 1000.0)