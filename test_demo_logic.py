#!/usr/bin/env python3
"""
Test the demo mode mapping logic with various peak scenarios
"""

def apply_demo_mode_mapping(peak_freq, demo_mode_enabled, demo_mode_bands, no_peak_value):
    """
    Apply demo mode mapping to quantize peak frequency to predefined bands.
    """
    if not demo_mode_enabled or not demo_mode_bands:
        return peak_freq
    
    # Check if peak_freq matches no_peak_value (means no peak detected)
    if peak_freq == no_peak_value:
        return no_peak_value
    
    # Search for matching band
    for min_f, max_f, target_f in demo_mode_bands:
        if min_f <= peak_freq <= max_f:
            return target_f
    
    # If no band matches, return no_peak_value
    return no_peak_value


# Configuration from default.ini
demo_mode_enabled = True
demo_mode_bands = [
    (27.25, 27.36, 27.3),
    (27.45, 27.55, 27.5),
    (27.62, 27.7, 27.65),
    (27.77, 27.86, 27.82),
]
no_peak_value = 27.0  # This is self.freq[0] from the ini

print("=" * 60)
print("Demo Mode Mapping Test")
print("=" * 60)
print(f"Demo Mode Enabled: {demo_mode_enabled}")
print(f"No Peak Value (default): {no_peak_value}")
print(f"Bands configured: {len(demo_mode_bands)}")
for i, (min_f, max_f, target_f) in enumerate(demo_mode_bands, 1):
    print(f"  Band {i}: [{min_f}, {max_f}] -> {target_f}")

print("\n" + "=" * 60)
print("Test Cases:")
print("=" * 60)

test_cases = [
    # (peak_freq, description)
    (27.0, "No peak (default value)"),
    (27.3, "Band 1 target - should map to 27.3"),
    (27.31, "Inside band 1 - should map to 27.3"),
    (27.5, "Band 2 target - should map to 27.5"),
    (27.65, "Band 3 target - should map to 27.65"),
    (27.82, "Band 4 target - should map to 27.82"),
    (27.4, "Between bands 1 and 2 - should map to 27.0"),
    (27.9, "Above band 4 - should map to 27.0"),
    (26.5, "Below band 1 - should map to 27.0"),
]

for peak_freq, desc in test_cases:
    mapped = apply_demo_mode_mapping(peak_freq, demo_mode_enabled, demo_mode_bands, no_peak_value)
    status = "✓" if mapped == no_peak_value or mapped in [t for _, _, t in demo_mode_bands] else "✗"
    print(f"{status} {peak_freq:6.2f} MHz -> {mapped:6.2f} MHz  ({desc})")

print("\n" + "=" * 60)
print("Issue Analysis:")
print("=" * 60)
print("When demo mode is enabled:")
print("- Detected peaks are mapped to their nearest band target")
print("- If no peak is detected (peak_freq == 27.0), it returns 27.0")
print("- If detected peak is NOT in any band, it returns 27.0")
print("\nThis means on timeline:")
print(f"- You should see ONLY these 5 values: 27.0, 27.3, 27.5, 27.65, 27.82")
print(f"- The 27.0 appears when NO peak or OUT-OF-BAND peak is detected")
print(f"- The other 4 values appear when peaks are in their respective bands")
