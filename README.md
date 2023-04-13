# DNS-Resolver-create-mydig-
This project involved implementing a DNS resolver tool called "mydig" that can find the IP address of a given domain name through DNS queries and comparing its performance with other DNS resolvers.

Read me 
Created "dig" - like command called "mydig" through python programming. To use it, simply provide the domain name as a command-line argument, and “mydig” will connect to one of the 25 root servers listed at https://www.iana.org/domains/root/servers to find the corresponding IP address. The DNSresolver method within mydig sends queries to the server and receives responses through recursive calls until the final IP address is found. I also implemented functionality to track the time taken to resolve the domain name by utilizing the sys, dns, and time libraries.

Use 
1. Make sure that you downloaded python and dnspython. 
2. Go to the file address 
3. Open CMD in the folder. 
4. Type ‘python mydig.py __domain-name__’ in CMD 
5. It will generate mydig_output.text including with the result that has similar work with dig”
