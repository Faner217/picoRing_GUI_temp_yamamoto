#!/usr/bin/env python3
"""Quick test of demo mode mapping logic"""

def test_demo_mode_mapping():
    """Test the demo mode mapping function"""
    
    # Simulate demo bands from config
    demo_bands = [
        (27.25, 27.36, 27.3),   # Band 1
        (27.45, 27.55, 27.5),   # Band 2
        (27.62, 27.7,  27.65),  # Band 3
        (27.77, 27.86, 27.82),  # Band 4
    ]
    no_peak_value = 27.0  # Default when no peak
    
    def apply_demo_mode_mapping(peak_freq, demo_mode_enabled, demo_mode_bands, no_peak_value):
        """Apply demo mode mapping to quantize peak frequency to predefined bands."""
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
    
    # Test cases
    test_cases = [
        # (input_freq, expected_output, description)
        (27.3, 27.3, "Inside band 1 lower bound"),
        (27.31, 27.3, "Inside band 1"),
        (27.36, 27.3, "Inside band 1 upper bound"),
        (27.5, 27.5, "Inside band 2 center"),
        (27.65, 27.65, "Inside band 3 center"),
        (27.82, 27.82, "Inside band 4 center"),
        (27.0, 27.0, "No peak value (default)"),
        (27.4, 27.0, "Between bands -> no peak"),
        (27.87, 27.0, "Outside all bands -> no peak"),
        (26.5, 27.0, "Way outside bands -> no peak"),
    ]
    
    print("Testing demo mode mapping with demo_mode_enabled=True:")
    for input_freq, expected, description in test_cases:
        result = apply_demo_mode_mapping(input_freq, True, demo_bands, no_peak_value)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{status}: {description}")
        print(f"       Input: {input_freq} MHz -> Output: {result} MHz (expected {expected} MHz)")
    
    print("\nTesting with demo_mode_enabled=False (passthrough):")
    for input_freq, _, description in test_cases[:3]:
        result = apply_demo_mode_mapping(input_freq, False, demo_bands, no_peak_value)
        status = "✓ PASS" if result == input_freq else "✗ FAIL"
        print(f"{status}: Input {input_freq} MHz -> Output {result} MHz (unchanged)")

if __name__ == '__main__':
    test_demo_mode_mapping()
