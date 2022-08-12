# Estimating the value of π using Monte Carlo

Move the slider on the sidebar to change the number of points or click the random button.
If you are on a mobile device, click on the arrow on the top left of the screen to show
the sidebar. Detailed explanation below the graph.

![plot]()

[Monte Carlo methods](https://en.wikipedia.org/wiki/Monte_Carlo_method) are a broad class
of computational algorithms that rely on repeated random sampling to obtain numerical
results. The underlying concept is to use randomness to solve problems that might be
deterministic in principle.

Monte Carlo methods vary, but tend to follow a particular pattern:

1. Define a domain of possible inputs
2. Generate inputs randomly from a probability distribution over the domain
3. Perform a deterministic computation on the inputs
4. Aggregate the results

For example, consider a quadrant (circular sector) inscribed in a unit square. Given that
the ratio of their areas is π/4, the value of π can be approximated using a Monte Carlo
method:

1. Draw a square, then inscribe a quadrant within it
2. Uniformly scatter a given number of points over the square
3. Count the number of points inside the quadrant, i.e. having a distance from the origin
   of less than 1
4. The ratio of the inside-count and the total-sample-count is an estimate of the ratio
   of the two areas, π/4. Multiply the result by 4 to estimate π.

In this procedure the domain of inputs is the square that circumscribes the quadrant. We
generate random inputs by scattering grains over the square then perform a computation on
each input (test whether it falls within the quadrant). Aggregating the results yields
our final result, the approximation of π. 

These Monte Carlo methods for approximating π are very slow compared to other methods,
and do not provide any information on the exact number of digits that are obtained. Thus,
they are never used to approximate π when speed or accuracy is desired.

Text adapted from [Wikipedia](https://en.wikipedia.org/wiki/Monte_Carlo_method).