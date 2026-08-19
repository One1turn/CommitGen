# 📝 CommitGen — Git Commit Message 生成器

> 不知道写什么 commit message？让 CommitGen 帮你生成一个看起来很专业的。

## 安装

```bash
git clone https://github.com/One1turn/CommitGen.git
cd CommitGen
```

## 使用

```bash
# 随机生成
python commitgen.py

# 指定类型
python commitgen.py --type feat

# 指定数量
python commitgen.py -n 5

# 指定 Gitmoji 风格
python commitgen.py --emoji
```

## 示例

```
$ python commitgen.py --emoji

✨ feat(auth): add OAuth2 flow with refresh token rotation

    - Implement PKCE flow for public clients
    - Add token rotation with reuse detection
    - Store encrypted refresh tokens in Redis
    - Add integration tests for token lifecycle

    Addresses: #142
    Breaking: refresh token format changed, old tokens invalidated
    Refs: RFC 6749 Section 6

$ python commitgen.py -n 3

🐛 fix: handle null pointer in user profile sync
💄 style: reformatted UserService.java with google-java-format
🔧 chore: bump express from 4.18.2 to 4.19.0
```

MIT License
