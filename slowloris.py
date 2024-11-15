#!/usr/bin/env python3
import argparse
import asyncio
import logging
import ssl
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import aiohttp
import statistics

@dataclass
class LoadTestConfig:
    host: str
    port: int = 80
    connections: int = 150
    duration: int = 60
    https: bool = False
    verbose: bool = False
    request_interval: float = 1.0

class LoadTester:
    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.results = []
        self.active_connections = 0
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            format="[%(asctime)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG if self.config.verbose else logging.INFO,
        )

    async def make_request(self, session: aiohttp.ClientSession, request_id: int) -> None:
        url = f"{'https' if self.config.https else 'http'}://{self.config.host}:{self.config.port}"
        
        try:
            start_time = datetime.now()
            async with session.get(url) as response:
                response_time = (datetime.now() - start_time).total_seconds()
                status = response.status
                self.results.append((status, response_time))
                
                if self.config.verbose:
                    logging.debug(f"Request {request_id}: Status {status}, Time {response_time:.3f}s")
                
        except Exception as e:
            logging.debug(f"Request {request_id} failed: {str(e)}")
            self.results.append((0, 0))  # Record failed requests

    async def run_load_test(self) -> None:
        connector = aiohttp.TCPConnector(limit=self.config.connections)
        timeout = aiohttp.ClientTimeout(total=10)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            start_time = datetime.now()
            request_id = 0
            
            while (datetime.now() - start_time).total_seconds() < self.config.duration:
                tasks = []
                for _ in range(self.config.connections):
                    task = asyncio.create_task(self.make_request(session, request_id))
                    tasks.append(task)
                    request_id += 1
                
                await asyncio.gather(*tasks)
                await asyncio.sleep(self.config.request_interval)
                
            self.print_results(start_time)

    def print_results(self, start_time: datetime) -> None:
        duration = (datetime.now() - start_time).total_seconds()
        successful_requests = len([r for r in self.results if r[0] == 200])
        failed_requests = len(self.results) - successful_requests
        
        response_times = [r[1] for r in self.results if r[1] > 0]
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            p95_response_time = statistics.quantiles(response_times, n=20)[-1]
        else:
            avg_response_time = median_response_time = p95_response_time = 0

        logging.info("\nLoad Test Results:")
        logging.info(f"Duration: {duration:.2f} seconds")
        logging.info(f"Total Requests: {len(self.results)}")
        logging.info(f"Successful Requests: {successful_requests}")
        logging.info(f"Failed Requests: {failed_requests}")
        logging.info(f"Requests/second: {len(self.results)/duration:.2f}")
        logging.info(f"Average Response Time: {avg_response_time:.3f}s")
        logging.info(f"Median Response Time: {median_response_time:.3f}s")
        logging.info(f"95th Percentile Response Time: {p95_response_time:.3f}s")

def main():
    parser = argparse.ArgumentParser(description="HTTP Load Testing Tool")
    parser.add_argument("host", help="Target host to load test")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port")
    parser.add_argument("-c", "--connections", type=int, default=150, help="Number of concurrent connections")
    parser.add_argument("-d", "--duration", type=int, default=60, help="Test duration in seconds")
    parser.add_argument("--https", action="store_true", help="Use HTTPS")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-i", "--interval", type=float, default=1.0, help="Request interval in seconds")
    
    args = parser.parse_args()
    
    config = LoadTestConfig(
        host=args.host,
        port=args.port,
        connections=args.connections,
        duration=args.duration,
        https=args.https,
        verbose=args.verbose,
        request_interval=args.interval
    )
    
    tester = LoadTester(config)
    asyncio.run(tester.run_load_test())

if __name__ == "__main__":
    main()
