# AgZen MBTA Subway Challenge

A Python command line program that uses the MBTA API to answer three
main questions:

1. Lists all subway routes (Light and Heavy Rail).
2. Finds the route with the most stops, route with the least stops, and the stops that connect two or more routes.
3. Finds a list of routes you could ride between any two subway stops. 

## Requirements

- Python 3.10 or newer
- An MBTA API key is optional

## Setup

Clone the repo.

```bash
git clone https://github.com/<your-username>/agzen-mbta-challenge.git
cd agzen-mbta-challenge
```

Create and activate a virtual envrionment.

```bash
# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
 
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

### API key (optional)

The program works both with and without a key. Without one, the API has a lower rate limit but since this program only makes a few request, that should not be an issue.

## Running the program

```bash
python main.py
```

The program prints the answers to Questions 1 and 2.

Example output:
 
```
Subway routes:
Red Line, Mattapan Line, Orange Line, Green Line B, Green Line C, Green Line D, Green Line E, Blue Line
 
Most stops: Green Line D (25 stops)
Fewest stops: Mattapan Line (8 stops)
 
Connecting stops:
Park Street: Red Line, Green Line B, Green Line C, Green Line D, Green Line E
Downtown Crossing: Red Line, Orange Line
Ashmont: Red Line, Mattapan Line
...

Start stop: Northeastern University
End stop: Harvard
Northeastern University to Harvard: Green Line E, Red Line
```

Stop names must match the MBTA's names exactly. For example, Kendall is Kendall/MIT.

## Running Tests

```bash
pytest
```

The tests use fake data and do not call the real API. 

## Design Decisions

### Question 1: Filtering with the API

I filter on the server with `/routes?filter[type]=0,1` instead of downloading all routes and filerting locally. I made this decision because of 3 reasons:

1. Less data is sent over the network. If I downloaded all routes, that would include bus routes as well, but we're only interested in light and heavy rail routes.
2. The filter is a documented API feature, so the API is meant to be used this way (https://api-v3.mbta.com/docs/swagger/index.html#/Route/ApiWeb_RouteController_index).
3. There is less code to write and test.

The main tradeoff I thought about is if we want to extend the program to include bus routes then we would need to write another request.


### Question 2: Counting stops and finding connections

The program fetches the stops for each subway route with `/stops?filter[route]=<route id>`. It builds a dictionary that maps each route name to its list of stop names and all 3 parts of Question 2 use this dictionary.

To find connecting stops, it flips the dictionary so each stop maps to the routes it is on. Then it only keeps the stops with two or more routes.


### Question 3: Finding a path

The program treats each route as a node in a graph. Two routes are connected if they share at least one stop. It then runs breadth first search from the routes that contain the start stop until it reaches a route that contains the end stop. 

BFS checks all paths with fewer transfers before paths with more transfers, so the result uses the fewest number of routes. It does not try to find the fewest stops, since the question asks for a list of routes.


#### Performance

- Building the graph compares every pair of routes, which is O(N^2) where N is the number of routes. With 8 routes, that's 64 checks. 
- BFS visits each route at most once, which is O(N + E) where E is the number of connections between routes.

#### Assumptions/Limitations

- Each Green Line branch (B, C, D, E) is its own route, since that is how the API models them. Stops like Kenmore show up as connecting several Green Line branches.
- Stops are matched by name, not by stop id. I thought this is a bit simpler and works better for the subway.
- Stop names in Question 3 are case sensitive so they must match exactly.
- The program gets fresh data on every run, it does not cache anything.