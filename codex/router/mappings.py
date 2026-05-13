from __future__ import annotations


PHASE_DEFAULT_METHOD = {
    "web": "investigation-first",
    "ad": "investigation-first",
    "postex": "concentrate-forces",
    "reverse": "investigation-first",
    "code-audit": "investigation-first",
    "payload": "practice-cognition",
    "evasion": "practice-cognition",
    "general": "overall-planning",
}


PHASE_ESCALATION_METHOD = {
    "web": "contradiction-analysis",
    "ad": "contradiction-analysis",
    "postex": "workflows",
    "reverse": "overall-planning",
    "code-audit": "contradiction-analysis",
    "payload": "workflows",
    "evasion": "workflows",
    "general": "workflows",
}


PHASE_DEFAULT_ROUTER = {
    "web": "recon-for-sec",
    "ad": "active-directory-kerberos-attacks",
    "postex": "post-exploitation-playbook",
    "reverse": "malware-loader-analysis",
    "code-audit": "hack",
    "payload": "weaponization-and-payloads",
    "evasion": "windows-av-evasion",
    "general": "hack",
}


ROUTER_LEAF_GROUPS = {
    "recon-for-sec": [
        "recon-and-methodology",
        "api-recon-and-docs",
        "graphql-and-hidden-parameters",
    ],
    "api-sec": [
        "api-auth-and-jwt-abuse",
        "api-authorization-and-bola",
        "graphql-and-hidden-parameters",
    ],
    "auth-sec": [
        "authbypass-authentication-flaws",
        "jwt-oauth-token-attacks",
        "oauth-oidc-misconfiguration",
        "idor-broken-object-authorization",
    ],
    "injection-checking": [
        "ssrf-server-side-request-forgery",
        "sqli-sql-injection",
        "xss-cross-site-scripting",
        "cmdi-command-injection",
        "ssti-server-side-template-injection",
        "deserialization-insecure",
        "xxe-xml-external-entity",
    ],
    "file-access-vuln": [
        "upload-insecure-files",
        "path-traversal-lfi",
        "insecure-source-code-management",
    ],
    "business-logic-vuln": [
        "business-logic-vulnerabilities",
        "race-condition",
    ],
    "active-directory-kerberos-attacks": ["active-directory-kerberos-attacks"],
    "active-directory-acl-abuse": ["active-directory-acl-abuse"],
    "active-directory-certificate-services": ["active-directory-certificate-services"],
    "ntlm-relay-coercion": ["ntlm-relay-coercion"],
    "post-exploitation-playbook": [
        "credential-access-operations",
        "windows-privilege-escalation",
        "linux-privilege-escalation",
        "windows-lateral-movement",
        "linux-lateral-movement",
        "tunneling-and-pivoting",
    ],
    "malware-loader-analysis": [
        "malware-loader-analysis",
        "anti-debugging-techniques",
        "code-obfuscation-deobfuscation",
        "binary-protection-bypass",
        "vm-and-bytecode-reverse",
    ],
    "weaponization-and-payloads": [
        "weaponization-and-payloads",
        "persistence-and-c2",
        "reverse-shell-techniques",
    ],
    "windows-av-evasion": [
        "windows-av-evasion",
        "waf-bypass-techniques",
        "401-403-bypass-techniques",
        "csp-bypass-advanced",
        "sandbox-escape-techniques",
    ],
    "hack": [
        "hack",
        "auth-sec",
        "api-sec",
        "injection-checking",
        "file-access-vuln",
        "business-logic-vuln",
    ],
}
