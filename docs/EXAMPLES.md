# Examples

## Normal mode

Prompt:

```text
写一个普通 React 页面
```

Behavior:
- no offensive doctrine injection
- handled as ordinary work

## Red-team mode

Prompt sequence:

```text
进入红队模式
程序启动后会释放文件并拉起子进程，帮我梳理执行链
```

Behavior:
- mode flips to `redteam-light`
- phase resolves to `reverse`
- response stays evidence-first and low-noise
