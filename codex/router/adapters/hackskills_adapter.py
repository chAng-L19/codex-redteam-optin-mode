from __future__ import annotations


def hackskills_router_notes() -> dict[str, str]:
    return {
        "recon-for-sec": "Default web reconnaissance and methodology router.",
        "api-sec": "API-centric routing for OpenAPI, GraphQL, auth and object authorization flows.",
        "auth-sec": "Authentication, session, token and authorization boundary router.",
        "injection-checking": "Generic injection family router for SSRF, SQLi, XSS, SSTI, XXE and command injection.",
        "file-access-vuln": "Upload, download, traversal and file exposure router.",
        "business-logic-vuln": "Workflow, state machine, race condition and business abuse router.",
        "active-directory-kerberos-attacks": "Kerberos and ticket abuse router.",
        "active-directory-acl-abuse": "ACL / ownership / delegated permission abuse router.",
        "active-directory-certificate-services": "ADCS and certificate template abuse router.",
        "ntlm-relay-coercion": "NTLM relay and coercion router.",
        "post-exploitation-playbook": "Foothold triage, credential access and lateral decision router.",
        "malware-loader-analysis": "Loader, unpacking and operator tradecraft router.",
        "weaponization-and-payloads": "Payload shaping and delivery router.",
        "windows-av-evasion": "Windows defensive bypass and evasion router.",
    }
