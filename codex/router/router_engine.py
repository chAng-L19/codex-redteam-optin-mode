from __future__ import annotations

import re

from .mappings import PHASE_DEFAULT_ROUTER


def select_router(prompt: str, phase: str) -> str:
    p = prompt
    if phase == "web":
        if re.search(r"\b(jwt|oauth|oidc|session|login|auth|token|bola|idor)\b|鉴权|登录|会话|令牌|越权", p, re.I):
            return "auth-sec"
        if re.search(r"\b(api|graphql|swagger|openapi|json)\b|接口|文档", p, re.I):
            return "api-sec"
        if re.search(r"\b(upload|download|path|file|lfi|traversal)\b|上传|下载|文件|路径", p, re.I):
            return "file-access-vuln"
        if re.search(r"\b(race|logic|workflow)\b|业务逻辑|竞态|流程缺陷", p, re.I):
            return "business-logic-vuln"
        if re.search(r"\b(ssrf|sqli|xss|ssti|cmdi|xxe|deserialization)\b|注入|模板|命令执行", p, re.I):
            return "injection-checking"
        return "recon-for-sec"

    if phase == "ad":
        if re.search(r"\b(adcs|cert|certificate)\b|证书服务|模板", p, re.I):
            return "active-directory-certificate-services"
        if re.search(r"\b(acl|genericall|writeowner|writedacl)\b|委派写|权限边", p, re.I):
            return "active-directory-acl-abuse"
        if re.search(r"\b(ntlm|relay|responder)\b|中继|NTLM", p, re.I):
            return "ntlm-relay-coercion"
        return "active-directory-kerberos-attacks"

    if phase == "postex":
        return "post-exploitation-playbook"

    if phase == "reverse":
        return "malware-loader-analysis"

    if phase == "code-audit":
        if re.search(r"\b(jwt|oauth|oidc|session|login|auth|token|bola|idor)\b|鉴权|登录|会话|令牌|越权", p, re.I):
            return "auth-sec"
        if re.search(r"\b(api|graphql|swagger|openapi|json)\b|接口|文档", p, re.I):
            return "api-sec"
        if re.search(r"\b(upload|download|path|file|lfi|traversal)\b|上传|下载|文件|路径", p, re.I):
            return "file-access-vuln"
        if re.search(r"\b(race|logic|workflow)\b|业务逻辑|竞态|流程缺陷", p, re.I):
            return "business-logic-vuln"
        if re.search(r"\b(ssrf|sqli|xss|ssti|cmdi|xxe|deserialization)\b|注入|模板|命令执行", p, re.I):
            return "injection-checking"
        return "hack"

    if phase == "payload":
        return "weaponization-and-payloads"

    if phase == "evasion":
        return "windows-av-evasion"

    return PHASE_DEFAULT_ROUTER.get(phase, "hack")
