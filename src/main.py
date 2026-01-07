import gpxpy
import srtm

with open('data/input/Katahdin.gpx', 'r')  as gpx_file:
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

# Initializw SRTM elevation data
elevation_data = srtm.get_data()

# Function to correct elevations
def correct_elevation(point):
    """Fetch correct elevation from SRTM data for a given point"""
    corrected = elevation_data.get_elevation(point.latitude, point.longitude)
    return corrected
# Correction Loop
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            original_elevation = point.elevation
            corrected_elevation = correct_elevation(point)

            if corrected_elevation is not None:
                print(f"Original: {original_elevation:.1f}m -> Corrected: {corrected_elevation:.1f}m")

output_path = 'data/output/corrected_sample.gpx'
with open(output_path, 'w') as output_file:
    output_file.write(gpx.to_xml())

print(f"\nCorrected GPX saved to {output_path}")
