import gpxpy
from elevation_sources import SRTMSource, USGSPointQuerySource
from visualization import create_elevation_profile

with open('data/input/YoungDrive.gpx', 'r')  as gpx_file:
    gpx = gpxpy.parse(gpx_file)

# 
print(f"Number of tracks: {len(gpx.tracks)}\n")

for track in gpx.tracks:
    print(f"Track name: {track.name}")
    for segment in track.segments:
        print(f"  Segment has {len(segment.points)} points")
        print(f"  First 5 points:")
        for point in segment.points[:5]:
            print(f"        Lat: {point.latitude:.6f}, Lon: {point.longitude:.6f}, Elevation: {point.elevation}m")

# Choose elevation source
source_choice = "usgs_point"

if source_choice == "srtm":
    elevation_source = SRTMSource()
elif source_choice == "usgs_point":
    elevation_source = USGSPointQuerySource()
else:
    raise ValueError(f"Unknown source: {source_choice}")
print(f"Using elevation source: {elevation_source.get_name()}\n")

# Function to correct elevations
def correct_elevation(point):
    """Fetch correct elevation for a given point"""
    return elevation_source.get_elevation(point.latitude, point.longitude)
# Correction Loop
for track in gpx.tracks:
    for segment in track.segments:
        point_count = 0
        for point in segment.points:

            if point_count >= 10:
                break

            original_elevation = point.elevation
            point.original_elevation = original_elevation
            corrected_elevation = correct_elevation(point)

            if corrected_elevation is not None:
                point.elevation = corrected_elevation
                print(f"Original: {original_elevation:.1f}m -> Corrected: {corrected_elevation:.1f}m")

            point_count += 1
# Calculate summary statistics
original_elevations = []
corrected_elevations = []
elevation_changes = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            if hasattr(point, 'original_elevation'): 
                original_elevations.append(point.original_elevation)
                corrected_elevations.append(point.elevation)
                elevation_changes.append(abs(point.elevation - point.original_elevation))

# Calculate statistics
avg_change = sum(elevation_changes) / len(elevation_changes)
max_change = max(elevation_changes)
large_changes = len([c for c in elevation_changes if c > 5])

print(f"\n=== Correction Summary ===")
print(f"Total points corrected: {len(elevation_changes)}")
print(f"Average elevation change: {avg_change:.2f}m")
print(f"Points with >5m change: {large_changes}")

# Calculate elevation gain/loss for the route
def calculate_elevation_gain_loss(elevations):
    gain = 0
    loss = 0
    for i in range(1, len(elevations)):
        diff = elevations[i] - elevations[i-1]
        if diff > 0:
            gain += diff
        else:
            loss += abs(diff)
    return gain, loss

original_gain, original_loss = calculate_elevation_gain_loss(original_elevations)
corrected_gain, corrected_loss = calculate_elevation_gain_loss(corrected_elevations)

print(f"\n=== Elevation Gain/Loss ===")
print(f"Original - Gain: {original_gain:.1f}m, Loss: {original_loss:.1f}m")
print(f"Corrected - Gain: {corrected_gain:.1f}m, Loss: {corrected_loss:.1f}m")
print(f"Difference - Gain: {abs(original_gain - corrected_gain):.1f}m, Loss: {abs(original_loss - corrected_loss):.1f}m")

create_elevation_profile(gpx)

output_path = 'data/output/corrected_sample.gpx'
with open(output_path, 'w') as output_file:
    output_file.write(gpx.to_xml())

print(f"\nCorrected GPX saved to {output_path}")
