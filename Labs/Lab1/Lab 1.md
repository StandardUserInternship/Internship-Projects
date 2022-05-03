# Lab 1
## Lab Assignment
This lab is made up of two parts that introduce two different networking libraries. 

### Lab Part 1 - HTTP Requests Crash Course
In general all that interns will need to understand about HTTP requests is that HTTP requests are how data is sent and received by websites. The most common requests are GET and POST, which are used to get data and send data respectively.

Here are some links with more information about HTTP requests:
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

Here are some links with information about the APIs in Python and the Requests library:
* https://realpython.com/python-requests/
* https://realpython.com/python-api/ 

Here is the official documentation for the Requests Library:
* https://docs.python-requests.org/en/latest/

Installing the requests library:
1. In the VS Code Terminal create a virtual environment
2. Run the command ‘pip install requests’

### Lab Assignment
Create a command line application that uses the requests library to send a Get request and a POST request to an api. The application should print out the data that it receives from each request, or the status code if the request fails.

Some APIs that can be used for this assignment include DnD, Cats, NASA, & Other APIs
A free API with POST requests enabled can be found [here](https://jsonplaceholder.typicode.com/).


### Requirements
One Python file that sends and receives data from an API.
* The file should:
  * Send a GET request to at least one API listed above
  * Send a POST request to an API
  * For both requests, the code should
    * Display any data to the user or save it to a file
    * Display the HTTP status code to the user through the terminal


## Lab Part 2 - A brief overview of Packets
A summary of packets and why they are important: From Cloudflare
A brief summary is that all data transmitted across a network has to be broken down into packets. TCP and UDP are different protocols for sending and receiving packets across a network. In this lab you’ll be interacting with packets directly, and to do that you’ll be using the Scapy library. 

### A Summary of Scapy
Scapy is a powerful Python library that allows you to interact with packets as they are transmitted. Specifically, Scapy can sniff packets being sent, read the contents of the packets, forge packets, and send packets all using Python. 

### Installing Scapy:
To install Scapy follow the instructions listed in the official documentation, or the general summary thats listed below:
Follow the installation instructions from Scapy’s website. Be aware of the platform specific instructions.
Install the following network analysis applications:
1. On Windows download npcap from the nmap website.
2. On Linux install TCPDump through the command line.
3. On OSX install libcap through homebrew on the command line.

Run the following command In the terminal for the virtual environment:
1. pip install scapy[basic] ( For MacOs use scapy\[basic\] )


### Lab Assignment
Create a python program that uses the Scapy library that can read transmitted network traffic. The network traffic that the program will read should be generated through the requests program that you made in Part 1.

Helpful Resources:
Scapy API Documentation
Sniff Function
Google

### Requirements
* One Python file that can read the network traffic being sent and received from the API requests. (Hint http traffic is on port 80 and https traffic is on port 443)
* The program should:
  * Display the content of the packets to the user through the terminal or by saving to a file.
  * Filter the traffic being read to only or primarily the packets related to the API requests. 
* Optional
  * This script should filter out irrelevant web traffic and only save the requests to and responses from the chosen API
