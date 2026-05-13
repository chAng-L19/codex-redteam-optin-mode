from __future__ import annotations

import re


def select_subphase(prompt: str, phase: str) -> str:
    if phase == "reverse":
        if re.search(r"\b(loader|stager|dropper|callback|payload)\b|加载链|释放|拉起子进程", prompt, re.I):
            return "loader"
        if re.search(r"\b(heap|rop|overflow|format string|primitive)\b|利用原语|溢出|ROP", prompt, re.I):
            return "exploitability"
        return "binary"
    if phase == "code-audit":
        if re.search(r"\b(entry|entrypoint|controller|handler|middleware)\b|入口|控制器|中间件", prompt, re.I):
            return "entrypoint"
        if re.search(r"\b(sink|dangerous function|query|exec|template)\b|危险函数|sink", prompt, re.I):
            return "leaf"
        return "route"
    if phase == "evasion":
        if re.search(r"\b(waf|cdn|header|smuggling|403|csp)\b|WAF|403|CSP", prompt, re.I):
            return "network"
        if re.search(r"\b(av|edr|defender|sandbox)\b|免杀|沙箱|对抗", prompt, re.I):
            return "host"
    return ""


def select_leaf_skill(prompt: str, phase: str, router: str) -> str:
    p = prompt
    if router == "auth-sec":
        if re.search(r"\b(jwt|token)\b|令牌|JWT", p, re.I):
            return "jwt-oauth-token-attacks"
        if re.search(r"\b(oauth|oidc)\b|单点|OIDC", p, re.I):
            return "oauth-oidc-misconfiguration"
        if re.search(r"\b(idor|bola)\b|对象授权|越权", p, re.I):
            return "idor-broken-object-authorization"
        return "authbypass-authentication-flaws"
    if router == "api-sec":
        if re.search(r"\b(graphql)\b|GraphQL", p, re.I):
            return "graphql-and-hidden-parameters"
        if re.search(r"\b(jwt|token|auth)\b|鉴权|令牌", p, re.I):
            return "api-auth-and-jwt-abuse"
        return "api-authorization-and-bola"
    if router == "injection-checking":
        if re.search(r"\bssrf\b|服务端请求伪造", p, re.I):
            return "ssrf-server-side-request-forgery"
        if re.search(r"\bsqli?\b|SQL 注入", p, re.I):
            return "sqli-sql-injection"
        if re.search(r"\bxss\b|跨站脚本", p, re.I):
            return "xss-cross-site-scripting"
        if re.search(r"\bssti\b|模板注入", p, re.I):
            return "ssti-server-side-template-injection"
        if re.search(r"\bcmdi\b|命令执行|命令注入", p, re.I):
            return "cmdi-command-injection"
        if re.search(r"\bxxe\b|XML 外部实体", p, re.I):
            return "xxe-xml-external-entity"
        return "deserialization-insecure"
    if router == "file-access-vuln":
        if re.search(r"\bupload\b|上传", p, re.I):
            return "upload-insecure-files"
        if re.search(r"\blfi\b|\btraversal\b|路径穿越", p, re.I):
            return "path-traversal-lfi"
        return "insecure-source-code-management"
    if router == "business-logic-vuln":
        if re.search(r"\brace\b|竞态", p, re.I):
            return "race-condition"
        return "business-logic-vulnerabilities"
    if router in {
        "active-directory-kerberos-attacks",
        "active-directory-acl-abuse",
        "active-directory-certificate-services",
        "ntlm-relay-coercion",
        "post-exploitation-playbook",
        "malware-loader-analysis",
        "weaponization-and-payloads",
        "windows-av-evasion",
    }:
        if router == "post-exploitation-playbook":
            if re.search(r"\bcredential|token|cookie|ssh key|kubeconfig\b|凭证|令牌|cookie", p, re.I):
                return "credential-access-operations"
            if re.search(r"\blinux\b|Linux", p, re.I):
                return "linux-privilege-escalation"
            if re.search(r"\bwindows\b|Windows", p, re.I):
                return "windows-privilege-escalation"
        if router == "windows-av-evasion":
            if re.search(r"\bwaf\b|WAF|403", p, re.I):
                return "waf-bypass-techniques"
            if re.search(r"\bcsp\b|CSP", p, re.I):
                return "csp-bypass-advanced"
            if re.search(r"\bsandbox\b|沙箱", p, re.I):
                return "sandbox-escape-techniques"
        return router
    if phase == "web":
        return "recon-for-sec"
    return "hack"
