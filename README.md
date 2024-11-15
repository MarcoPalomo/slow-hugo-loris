# slowloris.py - Simple slowloris in Python (optimized)

## What is Slowloris?
Slowloris is basically an HTTP Denial of Service attack that affects threaded servers. It works like this:

1. We start making lots of HTTP requests.
2. We send headers periodically (every ~15 seconds) to keep the connections open.
3. We never close the connection unless the server does so. If the server closes a connection, we create a new one keep doing the same thing.

This exhausts your servers thread pool and will not reply to other people.

:warning: This version provides legitimate load testing capabilities while being more efficient and providing better insights into the performance of your systems. Remember to only use this tool on systems you own or have explicit permission to test.

## Why `asyncio` and `aiohttp` ?

These two will help us getting a much better performance, handles concurrent connections efficiently and a proper connection pooling and resource management


## How to install and run?

You can clone the git repo or install using **pip**. Here's how you run it.

* `sudo pip3 install slowloris`
* `slowloris my-server.example.com`

That's all it takes to install and run slowloris.py.

If you want to clone using git instead of pip, here's how you do it.

* `git clone https://github.com/MarcoPalomo/slow-hugo-loris`
* `cd slow-hugo-loris`
* `python3 slowloris.py my-server.example.com`


## Configuration options
It is possible to modify the behaviour of slowloris with command-line
arguments. In order to get an up-to-date help document, just run
`slowloris -h`.

* host
* * Target host to load test
* -p, --port
* * Port of webserver, usually 80
* -c, --connections
* * Number of concurrent connections
* -d, --duration
* * Test duration in seconds
* -i, --interval
* * Request interval in seconds
* -v, --verbose
* * Increases logging (output on terminal)
* --https
* * Use HTTPS for the requests

## License
The code is licensed under the MIT License.
