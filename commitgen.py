#!/usr/bin/env python3
"""
📝 CommitGen — Git Commit Message 生成器
生成看起来很专业的 commit message
"""

import random
import argparse

# Conventional Commits types
COMMIT_TYPES = [
    ("feat",     "✨", "新增功能"),
    ("fix",      "🐛", "修复 bug"),
    ("docs",     "📚", "文档变更"),
    ("style",    "💄", "代码格式（不影响功能）"),
    ("refactor", "♻️",  "重构（非新功能也非 bug 修复）"),
    ("perf",     "⚡", "性能优化"),
    ("test",     "✅", "测试相关"),
    ("chore",    "🔧", "构建/依赖/工具变更"),
    ("build",    "📦", "构建系统或外部依赖"),
    ("ci",       "👷", "CI 配置变更"),
    ("revert",   "⏪", "回滚 commit"),
    ("hotfix",   "🚑", "紧急修复"),
    ("security", "🔒", "安全相关"),
    ("i18n",     "🌐", "国际化"),
    ("release",  "🚀", "发布版本"),
]

# scopes (project modules)
SCOPES = [
    "auth", "api", "ui", "db", "core", "utils", "config",
    "router", "middleware", "auth", "user", "admin", "dashboard",
    "payment", "notification", "search", "cache", "queue",
    "session", "profile", "settings", "logger", "telemetry",
    "validator", "serializer", "migration", "seed", "test",
]

# subject templates by type
SUBJECTS = {
    "feat": [
        "add {scope} module with {feature}",
        "implement {feature} for {scope}",
        "introduce {feature} support in {scope}",
        "add ability to {action}",
        "create {scope} endpoint for {feature}",
        "add {feature} with fallback handling",
        "support {feature} in {scope} layer",
    ],
    "fix": [
        "handle null pointer in {scope} sync",
        "resolve race condition in {scope}",
        "fix memory leak in {scope} cleanup",
        "correct off-by-one error in {scope} pagination",
        "fix infinite loop when {condition}",
        "patch SSRF vulnerability in {scope} URL handler",
        "fix broken {scope} after {change} refactor",
        "handle empty response from {scope} API",
    ],
    "docs": [
        "update README with {feature} usage",
        "add API documentation for {scope}",
        "fix typos in {scope} guide",
        "document {feature} behavior",
        "update CONTRIBUTING.md",
        "add architecture decision record for {scope}",
    ],
    "style": [
        "reformatted {scope} with google-java-format",
        "fix indentation in {scope}",
        "remove trailing whitespace",
        "apply prettier to {scope}",
        "convert tabs to spaces in {scope}",
    ],
    "refactor": [
        "extract {scope} logic to separate module",
        "simplify {scope} error handling",
        "replace callback chain with async/await in {scope}",
        "consolidate duplicate {scope} validation",
        "replace manual parsing with schema validation",
        "decouple {scope} from core layer",
    ],
    "perf": [
        "optimize {scope} query with index hint",
        "reduce bundle size by {pct}%",
        "cache {scope} results in Redis",
        "lazy-load {scope} components",
        "parallelize {scope} processing",
        "avoid N+1 queries in {scope}",
    ],
    "test": [
        "add unit tests for {scope}",
        "increase {scope} coverage to {pct}%",
        "add e2e tests for {feature}",
        "mock external API in {scope} tests",
        "add regression test for {issue_num}",
    ],
    "chore": [
        "bump {dep} from {v1} to {v2}",
        "update .gitignore for {scope}",
        "clean up unused imports in {scope}",
        "remove deprecated {scope} code",
        "update Makefile targets",
    ],
    "build": [
        "upgrade webpack to v5",
        "add Dockerfile for production",
        "update Node.js to LTS 22",
        "switch bundler from rollup to esbuild",
    ],
    "ci": [
        "add GitHub Actions workflow for {scope}",
        "cache dependencies in CI pipeline",
        "add matrix testing for Node 20/22",
        "fail fast on lint errors",
    ],
    "revert": [
        "revert {scope} changes from {hash}",
        "rollback {feature} introduced in {hash}",
    ],
    "hotfix": [
        "patch production crash in {scope}",
        "disable {feature} causing OOM",
        "hotfix: pin {dep} to {v1}",
    ],
    "security": [
        "sanitize input in {scope} handler",
        "upgrade {dep} to fix CVE-2026-{cve}",
        "enforce TLS 1.2 minimum",
        "rotate API keys in {scope}",
    ],
    "i18n": [
        "add zh-CN translations for {scope}",
        "extract strings from {scope} to i18n keys",
        "fix RTL layout for Arabic locale",
    ],
    "release": [
        "v{version} — see CHANGELOG for details",
        "cut release v{version}",
    ],
}

FEATURES = [
    "rate limiting", "pagination", "retry mechanism", "batch processing",
    "webhook delivery", "audit logging", "dark mode", "SSO login",
    "CSV export", "real-time sync", "offline mode", "graceful degradation",
    "backpressure handling", "progressive loading", "lazy hydration",
    "soft delete", "bulk operations", "streaming responses", " Circuit breaker",
    "service mesh integration", "feature flags", "A/B testing",
]

ACTIONS = [
    "export data", "invite users", "rotate credentials",
    "archive old records", "batch upload files",
    "generate reports", "replay events",
]

CONDITIONS = [
    "timeout is 0", "response is empty", "token is expired",
    "cache is cold", "queue is full",
]

DANGERS = [
    "network partition", "disk full", "OOM killer",
    "cert expiry", "clock skew",
]

CHANGES = [
    "ORM migration", "schema update", "endpoint renaming",
    "v2 API rollout",
]

DEPS = ["express", "react", "lodash", "axios", "ws", "pg", "redis", "kafkajs", "zod"]
VERSIONS = ["4.18.2", "4.19.0", "18.2.0", "18.3.1", "5.0.0", "1.2.3", "2.0.1"]

ISSUE_NUMS = [f"#{random.randint(100, 9999)}" for _ in range(20)]

CVES = [f"{random.randint(10000, 99999)}" for _ in range(20)]

VERSIONS_REL = [f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}" for _ in range(20)]

GIT_HASHES = [f"{random.choice('0123456789abcdef')}{random.choice('0123456789abcdef')}{random.choice('0123456789abcdef')}{random.choice('0123456789abcdef')}{random.choice('0123456789abcdef')}{random.choice('0123456789abcdef')}{random.choice('0123456789abcdef')}" for _ in range(20)]


def fill(template, scope):
    return template.format(
        scope=scope,
        feature=random.choice(FEATURES),
        action=random.choice(ACTIONS),
        condition=random.choice(CONDITIONS),
        change=random.choice(CHANGES),
        danger=random.choice(DANGERS),
        dep=random.choice(DEPS),
        v1=random.choice(VERSIONS),
        v2=random.choice(VERSIONS),
        pct=random.randint(5, 80),
        issue_num=random.choice(ISSUE_NUMS),
        cve=random.choice(CVES),
        version=random.choice(VERSIONS_REL),
        hash=random.choice(GIT_HASHES),
    )


def genOne(useEmoji):
    ct = random.choice(COMMIT_TYPES)
    ct_name, ct_emoji, ct_desc = ct
    
    scope = random.choice(SCOPES)
    
    templates = SUBJECTS.get(ct_name, SUBJECTS["feat"])
    template = random.choice(templates)
    subject = fill(template, scope)
    
    prefix = f"{ct_emoji} " if useEmoji else ""
    header = f"{prefix}{ct_name}({scope}): {subject}"
    
    # 随机添加 body
    body_lines = []
    if random.random() < 0.5:
        n_bullets = random.randint(2, 4)
        for _ in range(n_bullets):
            action = random.choice([
                f"Add {random.choice(FEATURES)} to {scope}",
                f"Refactor {scope} for clarity",
                f"Update {scope} tests",
                f"Remove dead code in {scope}",
                f"Handle edge case when {random.choice(CONDITIONS)}",
                f"Bump {random.choice(DEPS)} version",
            ])
            body_lines.append(f"    - {action}")
    
    # 随机添加 footer
    footers = []
    if random.random() < 0.3:
        footers.append(f"    Addresses: {random.choice(ISSUE_NUMS)}")
    if random.random() < 0.2:
        footers.append(f"    Breaking: {random.choice(FEATURES)} behavior changed")
    if random.random() < 0.1:
        footers.append(f"    Refs: RFC {random.randint(1000, 9999)} Section {random.randint(1, 20)}")
    
    msg = header
    if body_lines:
        msg += "\n"
        msg += "\n".join(body_lines)
    if footers:
        msg += "\n"
        msg += "\n".join(footers)
    
    return msg


def main():
    parser = argparse.ArgumentParser(description="📝 CommitGen — Git Commit Message 生成器")
    parser.add_argument("-n", type=int, default=1, help="生成数量 (默认 1)")
    parser.add_argument("--type", type=str, default=None, help="指定 commit 类型 (feat/fix/docs/...)")
    parser.add_argument("--emoji", action="store_true", help="启用 Gitmoji 前缀")
    args = parser.parse_args()
    
    count = max(1, args.n)
    
    for i in range(count):
        if args.type:
            matching = [t for t in COMMIT_TYPES if t[0] == args.type]
            if not matching:
                print(f"❌ 未知 commit 类型: {args.type}")
                print(f"   可用: {', '.join(t[0] for t in COMMIT_TYPES)}")
                return
            ct = matching[0]
            scope = random.choice(SCOPES)
            templates = SUBJECTS.get(ct[0], SUBJECTS["feat"])
            template = random.choice(templates)
            subject = fill(template, scope)
            prefix = f"{ct[1]} " if args.emoji else ""
            print(f"{prefix}{ct[0]}({scope}): {subject}")
        else:
            print(genOne(args.emoji))
        if i < count - 1:
            print()


if __name__ == "__main__":
    main()
