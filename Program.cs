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

    public Polygon Subdivide(int numPoints)
    {
        List<Point> newPoints = new List<Point>();
        Random rand = new Random();
        double minX = Points.Min(p => p.X);
        double maxX = Points.Max(p => p.X);
        double minY = Points.Min(p => p.Y);
        double maxY = Points.Max(p => p.Y);

        while (newPoints.Count < numPoints)
        {
            double x = minX + rand.NextDouble() * (maxX - minX);
            double y = minY + rand.NextDouble() * (maxY - minY);
            Point point = new Point(x, y);

            if (IsInsidePolygon(point))
            {
                newPoints.Add(point);
            }
        }

        return new Polygon(newPoints);
    }

    private bool IsInsidePolygon(Point point)
    {
        int n = Points.Count;
        bool result = false;
        int j = n - 1;
        for (int i = 0; i < n; i++)
        {
            if ((Points[i].Y > point.Y) != (Points[j].Y > point.Y) &&
                (point.X < (Points[j].X - Points[i].X) * (point.Y - Points[i].Y) / (Points[j].Y - Points[i].Y) + Points[i].X))
            {
                result = !result;
            }
            j = i;
        }
        return result;
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

        // Precompute areas of sub-polygons
        double[,] subPolygonAreas = new double[n, n];
        for (int i = 0; i < n; i++)
        {
            for (int j = i; j < n; j++)
            {
                List<Point> subPolygonPoints = Points.GetRange(i, j - i + 1);
                subPolygonAreas[i, j] = new Polygon(subPolygonPoints).Area();
            }
        }

        for (int i = 0; i < n; i++)
        {
            for (int j = i + 1; j < n; j++)
            {
                double area1 = subPolygonAreas[i, j];
                double area2 = totalArea - area1;

                double diff = Math.Abs(area1 - halfArea) + Math.Abs(area2 - halfArea);

                if (diff < minDiff)
                {
                    minDiff = diff;
                    bestPolygon1 = new Polygon(Points.GetRange(i, j - i + 1));
                    bestPolygon2 = new Polygon(Points.GetRange(j, n - j).Concat(Points.GetRange(0, i + 1)).ToList());
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

// PriorityQueue implementation
public class PriorityQueue<T>
{
    private List<(T Item, double Priority)> elements = new List<(T, double)>();

    public int Count => elements.Count;

    public void Enqueue(T item, double priority)
    {
        elements.Add((item, priority));
    }

    public T Dequeue()
    {
        var bestIndex = 0;

        for (var i = 0; i < elements.Count; i++)
        {
            if (elements[i].Priority < elements[bestIndex].Priority)
            {
                bestIndex = i;
            }
        }

        var bestItem = elements[bestIndex];
        elements.RemoveAt(bestIndex);
        return bestItem.Item;
    }
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
            Console.WriteLine(county.CountyName);
            List<Point> points = county.Boundary.Select(b => new Point(b.X, b.Y )).ToList();
            Polygon polygon = new Polygon(points);
            int prescincts = county.Prescints - 1;
            //int power = 0;
            //while (((1 << power) < prescincts) && (power < 8))
            //{
            //    polygon = polygon.Subdivide();
            //    power++;
            //}
            polygon = polygon.Subdivide(((2*prescincts) - points.Count + 2)/2);
            var pq = new PriorityQueue<Polygon>();
            pq.Enqueue(polygon, polygon.Area());
            while (prescincts > 0)
            {
                var item = pq.Dequeue();
                Console.WriteLine("{0}  {1}", prescincts, item.Points.Count);
                var (p1, p2) = item.Divide();

                if (p1 != null)
                    pq.Enqueue(p1, -p1.Area());
                if (p2 != null)
                    pq.Enqueue(p2, -p2.Area());
                prescincts--;
			}
            List<Polygon> subPolygons = new List<Polygon>();
            while (pq.Count > 0)
            {
                subPolygons.Add(pq.Dequeue());
			}

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



