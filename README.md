# Agent Skills

A collection of reusable AI agent skills compatible with multiple platforms (opencode, Claude Code, Codex, Cursor, and other Copilot-compatible agents).

## Skills

### project-docs

Initialize and maintain a three-document project knowledge system (`AGENTS.md` + `PROJECT_STATE.md` + `DEVLOG.md`) that gives AI agents persistent project context across sessions.

- **Trigger phrases**: "init docs", "project-docs", "update project status"
- **Compatible with**: opencode, Claude Code, Codex

## Installation

Copy individual skill directories to your agent's skills folder:

### opencode
```
~/.config/opencode/skills/project-docs/
```

### Claude Code
```
~/.claude/skills/project-docs/
```

### Other agents
```
~/.agents/skills/project-docs/
```

## License

All skills are licensed under GPL-3.0. Each skill directory also contains its own `LICENSE` file.
