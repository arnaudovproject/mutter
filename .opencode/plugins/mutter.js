/**
 * Mutter plugin for OpenCode — registers bundled skills and injects minimal routing context.
 * Skills are shared with the Claude / Codex plugin tree under mutter-claude/skills.
 */

import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

let _bootstrapCache = undefined;

export const MutterPlugin = async () => {
  const mutterSkillsDir = path.resolve(__dirname, "../../mutter-claude/skills");

  const getBootstrapContent = () => {
    if (_bootstrapCache !== undefined) return _bootstrapCache;

    const templateClaude = path.join(__dirname, "../../mutter-claude/templates/CLAUDE.md");
    let base = "";
    if (fs.existsSync(templateClaude)) {
      base = fs.readFileSync(templateClaude, "utf8").trim();
    }

    const toolMapping = `**Harness: OpenCode**
- List and load skills with OpenCode's native **skill** tool (e.g. load the \`scan\` or \`task\` skill from this plugin).
- Prefer **incremental** reads via \`.mutter/index/\` and active task/plan paths — never load the whole repository into context.
- For official docs before web search, open **one** section of \`.mutter/memory/official-tech-docs-roadmap.md\` when that file exists in the project.`;

    _bootstrapCache = base
      ? `## Mutter (OpenCode)\n\n${base}\n\n${toolMapping}\n`
      : `## Mutter (OpenCode)\n\n${toolMapping}\n`;

    return _bootstrapCache;
  };

  return {
    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(mutterSkillsDir)) {
        config.skills.paths.push(mutterSkillsDir);
      }
    },

    "experimental.chat.messages.transform": async (_input, output) => {
      const bootstrap = getBootstrapContent();
      if (!bootstrap || !output.messages.length) return;
      const firstUser = output.messages.find((m) => m.info.role === "user");
      if (!firstUser || !firstUser.parts.length) return;

      if (firstUser.parts.some((p) => p.type === "text" && p.text.includes("## Mutter (OpenCode)"))) return;

      const ref = firstUser.parts[0];
      firstUser.parts.unshift({ ...ref, type: "text", text: `\n${bootstrap}\n` });
    },
  };
};
