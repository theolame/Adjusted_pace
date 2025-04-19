class DataExtractor:
    def __init__(self, filepath):
        """
        Initialize the DataExtractor with the path to a .gpx or .fit file.

        Parameters:
            filepath (str): Path to the input GPX or FIT file.
        """
        self.filepath = filepath
        self.timestamps = []  # List of timestamps (in minutes from start)
        self.altitudes = []   # List of altitudes (in meters)
        self.speeds = []      # List of speeds (in m/s)
        self.distances = []   # List of cumulative distances (in meters)

    def extract(self):
        """
        Extract data from the specified file (.fit or .gpx).

        Returns:
            tuple: Four lists containing timestamps, altitudes, speeds, and distances.
        """
        # Choose extraction method based on file extension
        if self.filepath.endswith(".fit"):
            self._extract_from_fit()
        elif self.filepath.endswith(".gpx"):
            self._extract_from_gpx()
        else:
            raise ValueError("Unsupported file format.")
        
        return self.timestamps, self.altitudes, self.speeds, self.distances

    def _extract_from_fit(self):
        """
        Extract timestamp, altitude, speed, and distance data from a FIT file.

        Returns:
            None: Populates instance variables with extracted data.
        """
        from fitparse import FitFile
        fitfile = FitFile(self.filepath)

        for record in fitfile.get_messages("record"):
            data = {field.name: field.value for field in record}
            ts = data.get("timestamp")

            # Capture the initial timestamp for offset calculation
            if ts and not self.timestamps:
                start_time = ts

            # Store timestamp and distance if available
            if ts and data.get("distance") is not None:
                self.timestamps.append((ts - start_time).total_seconds() / 60)
                self.distances.append(data["distance"])

            # Get altitude (use enhanced altitude if available)
            alt = data.get("altitude") or data.get("enhanced_altitude")
            if ts and alt is not None:
                self.altitudes.append(alt)

            # Get speed
            if ts and data.get("speed"):
                self.speeds.append(data["speed"])

    def _extract_from_gpx(self):
        """
        Extract timestamp, altitude, speed, and distance data from a GPX file.

        Returns:
            None: Populates instance variables with extracted data.
        """
        import gpxpy
        from utils import haversine

        with open(self.filepath, "r") as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        total_distance = 0.0

        for track in gpx.tracks:
            for segment in track.segments:
                points = segment.points
                for i in range(1, len(points)):
                    pt1, pt2 = points[i - 1], points[i]

                    # Calculate time offset in minutes
                    self.timestamps.append((pt2.time - points[0].time).total_seconds() / 60)
                    self.altitudes.append(pt2.elevation)

                    # Compute distance between points using haversine formula
                    d = haversine(pt1.latitude, pt1.longitude, pt2.latitude, pt2.longitude)
                    total_distance += d
                    self.distances.append(total_distance)

                    # Compute speed in m/s
                    time_diff = (pt2.time - pt1.time).total_seconds()
                    speed = d / time_diff if time_diff > 0 else 0
                    self.speeds.append(speed)
