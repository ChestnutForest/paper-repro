import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.dirname(scriptDir);
const args = process.argv.slice(2);
const validateAll = args.includes("--all");
const requestedPaths = args.filter((arg) => arg !== "--all");

for (const arg of requestedPaths) {
  if (arg.startsWith("-")) {
    throw new Error(`Unknown option: ${arg}`);
  }
}

function run(command, commandArgs, options = {}) {
  const result = spawnSync(command, commandArgs, {
    cwd: repoRoot,
    encoding: "utf8",
    ...options,
  });
  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    const details = [result.stdout, result.stderr].filter(Boolean).join("\n").trim();
    throw new Error(`${command} exited with ${result.status}${details ? `\n${details}` : ""}`);
  }
  return result.stdout.trim();
}

function gitLines(commandArgs) {
  const output = run("git", commandArgs);
  return output ? output.split(/\r?\n/u).filter(Boolean) : [];
}

function normalizeRepositoryPath(candidate) {
  const absolute = path.resolve(repoRoot, candidate);
  const relative = path.relative(repoRoot, absolute);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error(`Path is outside the repository: ${candidate}`);
  }
  if (path.extname(relative).toLowerCase() !== ".md") {
    return null;
  }
  if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) {
    throw new Error(`Markdown file does not exist: ${candidate}`);
  }
  return relative.split(path.sep).join("/");
}

function collectMarkdownPaths() {
  if (requestedPaths.length > 0) {
    return requestedPaths;
  }
  if (validateAll) {
    return [
      ...gitLines(["ls-files", "--", "*.md"]),
      ...gitLines(["ls-files", "--others", "--exclude-standard", "--", "*.md"]),
    ];
  }
  return [
    ...gitLines(["diff", "--name-only", "--diff-filter=ACMR", "HEAD", "--", "*.md"]),
    ...gitLines(["ls-files", "--others", "--exclude-standard", "--", "*.md"]),
  ];
}

function countFilesByExtension(directory, extension) {
  let count = 0;
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      count += countFilesByExtension(entryPath, extension);
    } else if (path.extname(entry.name).toLowerCase() === extension) {
      count += 1;
    }
  }
  return count;
}

const manifestPath = path.join(
  repoRoot,
  "node_modules",
  "@mermaid-js",
  "mermaid-cli",
  "package.json",
);
if (!fs.existsSync(manifestPath)) {
  throw new Error("Mermaid CLI is not installed. Run `npm ci` at the repository root.");
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
const binRelative = typeof manifest.bin === "string" ? manifest.bin : manifest.bin?.mmdc;
if (!binRelative) {
  throw new Error("The installed Mermaid CLI package does not expose the mmdc executable.");
}
const cliEntry = path.resolve(path.dirname(manifestPath), binRelative);
const cliVersion = run(process.execPath, [cliEntry, "--version"]);

const markdownPaths = [
  ...new Set(collectMarkdownPaths().map(normalizeRepositoryPath).filter(Boolean)),
].sort();
const targets = markdownPaths
  .map((relativePath) => {
    const absolutePath = path.join(repoRoot, relativePath);
    const source = fs.readFileSync(absolutePath, "utf8");
    const blockCount = (source.match(/^```mermaid[ \t]*\r?$/gmu) ?? []).length;
    return { absolutePath, blockCount, relativePath };
  })
  .filter(({ blockCount }) => blockCount > 0);

const temporaryRoot = fs.mkdtempSync(path.join(os.tmpdir(), "paper-repro-mermaid-"));
let renderedBlocks = 0;

try {
  for (const [index, target] of targets.entries()) {
    const outputDirectory = path.join(temporaryRoot, String(index + 1).padStart(3, "0"));
    fs.mkdirSync(outputDirectory);
    const outputMarkdown = path.join(outputDirectory, "rendered.md");
    run(process.execPath, [cliEntry, "-i", target.absolutePath, "-o", outputMarkdown, "-q"]);
    if (!fs.existsSync(outputMarkdown)) {
      throw new Error(`Mermaid CLI did not create Markdown output for ${target.relativePath}`);
    }
    const svgCount = countFilesByExtension(outputDirectory, ".svg");
    if (svgCount !== target.blockCount) {
      throw new Error(
        `Rendered SVG count mismatch for ${target.relativePath}: expected ${target.blockCount}, got ${svgCount}`,
      );
    }
    renderedBlocks += svgCount;
    console.log(`PASS ${target.relativePath}: ${svgCount} diagram(s)`);
  }
} finally {
  const resolvedTemporaryRoot = path.resolve(temporaryRoot);
  const resolvedSystemTemp = path.resolve(os.tmpdir());
  if (
    path.dirname(resolvedTemporaryRoot).toLowerCase() !== resolvedSystemTemp.toLowerCase() ||
    !path.basename(resolvedTemporaryRoot).startsWith("paper-repro-mermaid-")
  ) {
    throw new Error(`Refusing to remove unexpected temporary path: ${resolvedTemporaryRoot}`);
  }
  fs.rmSync(resolvedTemporaryRoot, { force: true, recursive: true });
}

console.log(`Mermaid CLI ${cliVersion}: ${targets.length} file(s), ${renderedBlocks} diagram(s) rendered.`);
