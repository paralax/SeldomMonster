To perform API penetration testing on local subnet devices, you will combine traditional internal network penetration testing techniques for discovery with API-focused methodologies to assess the security of discovered APIs. The goal is to evaluate what an attacker could do from within the internal network. [1, 2, 3]  

## Methodology Overview 
The process generally follows these steps: 

• Reconnaissance & Discovery: Identify all live hosts and running services within the local subnet. 
• Service & API Identification: Determine which services are APIs and if they are documented or undocumented. 
• Vulnerability Analysis & Exploitation: Test the identified APIs for security flaws based on established frameworks like the OWASP API Security Top 10. 
• Reporting: Document findings and provide remediation strategies. [4, 5, 6, 7, 8]  

## Key Tools 
• Network Discovery: 

	• Nmap: A free and open-source tool essential for scanning internal networks, discovering hosts, and identifying open ports and running services. 
	• Wireshark/Netdiscover: For detailed network traffic analysis and host discovery in a local area network (LAN) environment. 
    • nc: Allows TCP connections from the shell and connects stdin and stdout. 

• API/Web Application Testing: 

	• Burp Suite/OWASP ZAP: Industry-standard tools for intercepting, analyzing, and manipulating API traffic and web application requests. 
	• Postman/SoapUI: Platforms often used for API development that can be adapted for testing documented endpoints and sending well-formed requests. 
	• Metasploit: A framework that can be used for exploiting vulnerabilities found in services running on the network. [2, 4, 9, 10, 11, 12, 13, 14]  
    • curl: A simple command-line based HTTP interaction tool

General Steps for Pentesting Local Subnet APIs 

1. Gain Internal Access: You must have a presence inside the local network. This is typically achieved by deploying a test machine (physical or VM in bridged mode) that connects directly to the LAN, behaving like any other local device. 
2. Scope the Target:  Use  Nmap 
 to perform a comprehensive scan of the private IP address ranges (e.g., 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to map out all connected devices and their exposed ports/services 
. 
3. Identify Potential APIs: Look for common API-related ports or services advertised via protocols like WS-Discovery on port 5357 (common in Windows environments). Many local devices like IoT devices or internal servers use APIs for management. 
4. Analyze API Endpoints: Once an API is identified, use tools like Burp Suite to proxy traffic and look for undocumented endpoints through directory brute-forcing or analyzing application source code (e.g., single-page applications often contain API keys/endpoints in the client-side code). 
5. Test for Vulnerabilities: Focus on common API security flaws: 

	• Broken Object Level Authorization (BOLA): Can you access data or resources belonging to another user or device? 
	• Authentication/Authorization Flaws: Can you bypass login mechanisms or escalate privileges? 
	• Excessive Data Exposure: Does the API return more data than the client needs, potentially exposing sensitive information? 
	• Lack of Resource & Rate Limiting: Can you overload the API with requests (DoS) or brute-force credentials? 

6. Document and Report: Detail all vulnerabilities found, the potential business impact, and provide clear remediation advice to secure the local APIs and devices. [2, 4, 14, 15, 16, 17, 18, 19, 20, 21, 22]  

## API Penetration Testing with curl
You can manipulate HTTP requests with various curl flags to test for common API vulnerabilities. 
Test different HTTP Methods: Some APIs might allow unintended methods on specific endpoints.
    
    curl -X PUT 192.168.1.100

Send Data (POST requests): Test for injection vulnerabilities (like SQLi or OS command injection) by sending various payloads in the request body.

Send JSON data:

    curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "password"}' 192.168.1.100

Send data from a file (useful for large or complex payloads):

    curl -X POST -H "Content-Type: application/json" -d @payload.json 192.168.1.100

Handle Authentication: Pass cookies, API keys, or basic authentication credentials.
Using cookies:

    curl -b "session_id=abc123xyz" 192.168.1.100

Using headers (e.g., for an API token):

    curl -H "Authorization: Bearer <your_token>" 192.168.1.100

For more ideas see https://github.com/swisskyrepo/PayloadsAllTheThings 

## Wordlists

You have some files locally under the "wordlists" directory for testing and discovery:
- For header tests use the list here: wordlists/headers-fuzz.txt
- For HTTP directory fuzzing use the list here: wordlists/directory-list-2.3-small.txt 


## References 

[1] https://www.breachlock.com/resources/blog/why-network-penetration-testing-is-critical-for-security/
[2] https://www.youtube.com/watch?v=gfHNfw6pDxc
[3] https://www.getastra.com/blog/security-audit/internal-penetration-testing/
[4] https://medium.com/@vivekbhatt2002/using-nat-and-bridged-network-adapters-in-penetration-testing-a-practical-guide-for-ethical-53ebfd3d8c9e
[5] https://www.vikingcloud.com/blog/api-penetration-testing-an-in-depth-overview
[6] https://www.netspi.com/blog/executive-blog/application-pentesting/api-security-testing-the-overlooked-frontline/
[7] https://www.dcinnovationsinc.com/services/163-penetration-testing-services
[8] https://blog.securelayer7.net/shadow-apis-explained-risks-detection-and-prevention/
[9] https://www.akamai.com/glossary/what-are-api-vulnerabilities
[10] https://www.impart.ai/api-security-best-practices/api-pentesting
[11] https://plextrac.com/most-popular-penetration-testing-tools-in-2023/
[12] https://testguild.com/3-free-api-security-tools/
[13] https://portswigger.net/web-security/api-testing
[14] https://artificesecurity.com/what-is-internal-network-penetration-testing/
[15] https://docs.horizon3.ai/quickstart/internal/
[16] https://www.youtube.com/watch?v=k36mRyG7HPc
[17] https://evalian.co.uk/api-penetration-testing-what-why-how/
[18] https://www.pentestpad.com/port-exploit/port-5357-wsdapi-web-services-for-devices
[19] https://docs.cobalt.io/methodologies/internal-network/
[20] https://www.breachlock.com/products/pentesting-services/
[21] https://www.getastra.com/blog/security-audit/penetration-testing-phases/
[22] https://wesecureapp.com/blog/the-only-api-penetration-testing-checklist-you-need/