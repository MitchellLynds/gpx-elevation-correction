import matplotlib.pyplot as plt
import math

def calculate_cumulative_distance(points):
    """Calculate cumulative distance along the track in kilometers"""
    distances = [0.0]

    for i in range(1, len(points)):

        lat1, lon1 = points[i - 1].latitude, points[i - 1].longitude
        lat2, lon2 = points[i].latitude, points[i].longitude

        # Haversine formula
        R = 6371 # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat/2)**2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c

        distances.append(distances[-1] + distance)

    return distances

def create_elevation_profile(gpx, output_path='data/output/elevation_profile.png'):
    """Create before and after elevation profile visualization"""

    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            points.extend(segment.points)

    # Calculate distances
    distances = calculate_cumulative_distance(points)

    # Extract elevations
    original_elevations = [p.original_elevation for p in points if hasattr(p, 'original_elevation')]
    corrected_elevations = [p.elevation for p in points]

    # Create the plot
    plt.figure(figsize=(12, 6))

    plt.plot(distances, original_elevations, label='Original GPS', alpha=0.7, linewidth=1.5, color='red')
    plt.plot(distances, corrected_elevations, label='Corrected', alpha=0.9, linewidth=2, color='blue')

    plt.xlabel('Distance (km)', fontsize=12)
    plt.ylabel('Elevation (m)', fontsize=12)
    plt.title('Elevation Profile: Original vs Corrected', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"/nVisualization saved to {output_path}")
    plt.close()