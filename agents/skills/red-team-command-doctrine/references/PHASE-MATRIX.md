# Phase Matrix

| Phase | Goal | Typical Router | Typical Leaf | Exit Signal |
|---|---|---|---|---|
| recon | build target picture | recon-for-sec | recon-and-methodology | enough evidence for one candidate path |
| web | prove one web attack path | auth-sec / api-sec / injection-checking | jwt-oauth-token-attacks / ssrf / sqli / xss | one reproducible path or ruled-out branch |
| ad | choose the quietest domain path | AD routers | kerberos / acl / adcs / relay | one viable domain path with evidence |
| postex | triage foothold and next hop | post-exploitation-playbook | credential-access-operations / privesc / lateral | next-hop or objective identified |
| reverse | recover execution chain | malware-loader-analysis | loader / anti-debug / obfuscation | execution chain or exploitability clarified |
| code-audit | prove one input-to-sink chain | auth-sec / api-sec / injection-checking / file-access-vuln | leaf vuln skill | one controlled path demonstrated |
| payload | shape delivery | weaponization-and-payloads | payload / persistence / reverse shell | delivery constraints matched |
| evasion | choose the lowest-noise bypass | windows-av-evasion | waf / 401-403 / csp / sandbox | bypass route selected or ruled out |
