using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using Newtonsoft.Json;

public class Point
{
    public double X { get; set; }
    public double Y { get; set; }

    public Point(double x, double y)
    {
        X = x;
        Y = y;
    }
}

public class Polygon
{
    public List<Point> Points { get; set; }

    public Polygon(List<Point> points)
    {
        Points = points;
    }

    public Polygon Subdivide()
    {
        List<Point> newPoints = new List<Point>();
        int n = Points.Count;

        for (int i = 0; i < n; i++)
        {
            Point p1 = Points[i];
            Point p2 = Points[(i + 1) % n];
            Point midpoint = new Point((p1.X + p2.X) / 2, (p1.Y + p2.Y) / 2);
            newPoints.Add(p1);
            newPoints.Add(midpoint);
        }

        return new Polygon(newPoints);
    }

    public List<Point> RemoveDuplicates(List<Point> points)
    {
        List<Point> uniquePoints = new List<Point>();
        HashSet<(double, double)> seen = new HashSet<(double, double)>();

        foreach (Point point in points)
        {
            if (!seen.Contains((point.X, point.Y)))
            {
                uniquePoints.Add(point);
                seen.Add((point.X, point.Y));
            }
        }
        uniquePoints.Add(uniquePoints[0]);  // Close the loop
        return uniquePoints;
    }

    public (Polygon, Polygon) Divide()
    {
        int n = Points.Count;
        double totalArea = this.Area();
        double halfArea = totalArea / 2.0;
        double minDiff = double.MaxValue;
        Polygon bestPolygon1 = null;
        Polygon bestPolygon2 = null;

        for (int i = 0; i < n; i++)
        {
            for (int j = i + 1; j < n; j++)
            {
                List<Point> polygon1Points = Points.GetRange(i, j - i + 1);
                polygon1Points.Add(Points[i]);
                List<Point> polygon2Points = new List<Point>();
                polygon2Points.AddRange(Points.GetRange(j, n - j));
                polygon2Points.AddRange(Points.GetRange(0, i + 1));

                polygon1Points = RemoveDuplicates(polygon1Points);
                polygon2Points = RemoveDuplicates(polygon2Points);

                Polygon polygon1 = new Polygon(polygon1Points);
                Polygon polygon2 = new Polygon(polygon2Points);
                double area1 = polygon1.Area();
                double area2 = polygon2.Area();

                double diff = Math.Abs(area1 - halfArea) + Math.Abs(area2 - halfArea);

                if (diff < minDiff)
                {
                    minDiff = diff;
                    bestPolygon1 = polygon1;
                    bestPolygon2 = polygon2;
                }
            }
        }

        return (bestPolygon1, bestPolygon2);
    }

    public double Area()
    {
        int n = Points.Count;
        double area = 0.0;

        for (int i = 0; i < n; i++)
        {
            double x1 = Points[i].X;
            double y1 = Points[i].Y;
            double x2 = Points[(i + 1) % n].X;
            double y2 = Points[(i + 1) % n].Y;
            area += x1 * y2 - y1 * x2;
        }

        return Math.Abs(area) / 2.0;
    }
}


public class County
{
    [JsonProperty("county")]
    public string CountyName { get; set; }
    public List<Point> Boundary { get; set; }
    public int Prescints { get; set; }
    public int Rep { get; set; }
    public int Dem { get; set; }
    public int Oth { get; set; }
}

public class State
{
    public string Name { get; set; }
    public List<County> Counties { get; set; }
    public int Districts { get; set; }
}


class Program
{
    static void Main()
    {
        // Read input JSON from file
        string inputJson = File.ReadAllText("counties.json");
        var state = JsonConvert.DeserializeObject<State>(inputJson);

        var outputJson = new
        {
            Name = state.Name,
            counties = new List<object>(),
            districts = state.Districts
        };

        foreach (var county in state.Counties)
        {
            List<Point> points = county.Boundary.Select(b => new Point(b.X, b.Y )).ToList();
            Polygon polygon = new Polygon(points);
            List<Polygon> subPolygons = polygon.Divide();
            Console.WriteLine(county.CountyName);
            var countyJson = new
            {
                county = county.CountyName,
                precincts = new List<object>(),
                rep = county.Rep,
                dem = county.Dem,
                oth = county.Oth
            };

            for (int i = 0; i < county.Prescints; ++i)
            {
                var precinctJson = new
                {
                    id = i + 1,
                    boundary = new List<object>()
                };

                foreach (var point in subPolygons[i].Points)
                {
                    precinctJson.boundary.Add(new { x = point.X, y = point.Y });
                }

                countyJson.precincts.Add(precinctJson);
            }

            outputJson.counties.Add(countyJson);
        }

        // Output JSON to file
        string jsonString = JsonConvert.SerializeObject(outputJson, Formatting.Indented);
        File.WriteAllText("output.json", jsonString);

        Console.WriteLine("County boundaries have been divided and written to output.json");
    }
}



