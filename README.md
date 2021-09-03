<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#payment-engine">Payment Engine</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#correctness">Correctness</a></li>
    <li><a href="#running-tests">Running Tests</a></li>
    <li><a href="#types-of-tests">Types of tests</a></li>
    <li><a href="#completeness">Completeness</a></li>
    <li><a href="#safety">Safety</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Payment Engine 

![Screenshot](Payment_engine.png)

The following is a Dummy payments engine that reads a series of transactions from a CSV, updates client accounts,
handles disputes and chargebacks, and then outputs the state of clients accounts as a CSV.

### Built With

* [Python3](https://www.python.org)



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

You will need Python3 in order to run this script.

1. Visit https://www.python.org and download the latest version for your OS.
2. Make sure Python and pip are accessible via command line.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/L271828R/payment_engine 
   ```
2. CD into payment_engine 
   ```sh
   cd payment_engine 
   ```
3. create a python virtual environment 
   ```sh
   python -m venv env
   ```
4. activate your virtual environment
   ```sh
   source env/bin/activate 
   ```
5. install dependencies via pip
   ```sh
   pip install -r requirements.txt
   ```
In step 5 the most notable install will be pytest, a library for running unit tests.
<!-- USAGE EXAMPLES -->
## Usage

1. run base example
   ```sh
   python payment_engine.py transactions.csv
   ```

## Correctness

This project uses pytest for running unit tests.
Tests are located in the tests folder.

## Running tests
Make sure you are at the root of the project
1. run all tests
   ```sh
   py.test
   ```

## Types of tests

1. happy path tests
2. negative scenarios
3. platform testing
4. precision testing 


## Completeness

I believe all transactions ( Deposits, Withdrawals, Disputes, Resolves and Chargebacks ) are accountend for.


## Safety

I am perhaps readiing the full input file as once. 
Python can handle large file sizes, but nonetheless this may pose a risk.

