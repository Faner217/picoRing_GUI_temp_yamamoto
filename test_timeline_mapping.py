#!/usr/bin/env python3
"""
Test the complete timeline peak mapping flow
"""
import numpy as np

def apply_demo_mode_mapping(peak_freq, demo_mode_enabled, demo_mode_bands, no_peak_value):
    """Updated version with tolerance and float conversion"""
    if not demo_mode_enabled or not demo_mode_bands:
        return peak_freq
    
    # Use a small tolerance for floating-point comparison
    if abs(float(peak_freq) - float(no_peak_value)) < 0.001:
        return no_peak_value
    
    # Search for matching band
    for min_f, max_f, target_f in demo_mode_bands:
        if min_f <= float(peak_freq) <= max_f:
            return target_f
    
    # If no band matches, return no_peak_value
    return no_peak_value

# Simulate the scenario
demo_mode_enabled = True
demo_mode_bands = [
    (27.25, 27.36, 27.3),
    (27.45, 27.55, 27.5),
    (27.62, 27.7, 27.65),
    (27.77, 27.86, 27.82),
]
no_peak_value = 27.0

# Simulate timeline_y array (50 points)
timeline_y = np.full(50, no_peak_value)

# Simulate multiple peaks detected across multiple updates
test_peaks = [
    27.0,    # No peak
    27.31,   # In band 1 - should map to 27.3
    27.32,   # In band 1 - should map to 27.3
    27.4,    # Between bands - should map to 27.0
    27.5,    # In band 2 - should map to 27.5
    27.65,   # In band 3 - should map to 27.65
    27.82,   # In band 4 - should map to 27.82
    27.9,    # Above band 4 - should map to 27.0
    27.0,    # No peak again
    27.3,    # Exact band 1 target
]

print("=" * 70)
print("Timeline Peak Mapping Simulation")
print("=" * 70)
print(f"Demo Mode: {demo_mode_enabled}")
print(f"No Peak Value: {no_peak_value}")
print(f"Bands: {len(demo_mode_bands)}")
for i, (min_f, max_f, target_f) in enumerate(demo_mode_bands, 1):
    print(f"  Band {i}: [{min_f}, {max_f}] -> {target_f}")

print("\n" + "=" * 70)
print("Simulating 10 Peak Detections:")
print("=" * 70)

unique_values = set()
for i, peak in enumerate(test_peaks):
    mapped = apply_demo_mode_mapping(peak, demo_mode_enabled, demo_mode_bands, no_peak_value)
    timeline_y[i % 50] = mapped
    unique_values.add(mapped)
    status = "✓" if mapped in [no_peak_value] + [t for _, _, t in demo_mode_bands] else "✗"
    print(f"{status} Update {i:2d}: {peak:6.2f} MHz -> {mapped:6.2f} MHz (Timeline[{i % 50:2d}])")

print("\n" + "=" * 70)
print("Result Analysis:")
print("=" * 70)
unique_sorted = sorted(list(unique_values))
print(f"Unique values in timeline: {len(unique_sorted)} values")
for val in unique_sorted:
    count = np.sum(timeline_y == val)
    print(f"  {val:6.2f} MHz appears {count:2d} times in timeline")

expected_values = {no_peak_value} | {t for _, _, t in demo_mode_bands}
print(f"\nExpected values: {sorted(list(expected_values))}")
print(f"Actual unique values: {unique_sorted}")
print(f"Match: {set(unique_sorted) == expected_values}")

# Check if any values fall outside expected range
out_of_range = [v for v in unique_sorted if v not in expected_values]
if out_of_range:
    print(f"\n⚠️  WARNING: Values outside expected range: {out_of_range}")
else:
    print(f"\n✓ SUCCESS: All timeline values are within expected range!")
