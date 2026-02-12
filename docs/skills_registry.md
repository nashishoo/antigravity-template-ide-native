# Local Skill Registry

The local skill registry allows the Architect to discover skills located in arbitrary directories on your machine, not just within the project's `src/skills` folder.

## Configuration

The registry is defined in `.agent/skills.json` at the project root.

### Schema

```json
{
  "skills_dirs": [
    "/absolute/path/to/my-skills",
    "../relative/path/to/more-skills"
  ]
}
```

- **skills_dirs**: A list of paths to directories containing skills.
    - Each directory in this list is expected to contain subdirectories, where each subdirectory has a `SKILL.md` file.
    - Paths can be absolute or relative to the project root.

### Example structure

If you have a skills directory at `/Users/me/dev/my-skills` containing:

```
/Users/me/dev/my-skills/
  ├── data-science/
  │   ├── SKILL.md
  │   └── tools.py
  └── web-scraping/
      └── SKILL.md
```

You can add it to `.agent/skills.json`:

```json
{
  "skills_dirs": [
    "/Users/me/dev/my-skills"
  ]
}
```

The Architect will then discover `data-science` and `web-scraping` as available skills.
