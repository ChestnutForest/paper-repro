param(
    [switch]$RequireGitTracked
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$expectedSkills = @(
    'paper-repro-skill-source-policy',
    'paper-repro-arch-guide',
    'arxiv-paper-repro',
    'paper-repro-devlog',
    'paper-repro-commit-output'
)
$failures = New-Object System.Collections.Generic.List[string]
$utf8Strict = New-Object System.Text.UTF8Encoding($false, $true)

function Add-Failure([string]$Message) {
    $script:failures.Add($Message)
}

function Get-Text([string]$Path, [bool]$EnforceLf = $true) {
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Add-Failure "UTF-8 BOM found: $Path"
    }
    if ($EnforceLf -and [System.Text.Encoding]::ASCII.GetString($bytes).Contains("`r`n")) {
        Add-Failure "CRLF found; LF required: $Path"
    }
    try {
        return $utf8Strict.GetString($bytes)
    }
    catch {
        Add-Failure "Invalid UTF-8: $Path"
        return ''
    }
}

function Test-Frontmatter([string]$Path, [string]$ExpectedName) {
    $text = Get-Text $Path
    $lines = $text -split "`n"
    if ($lines.Count -lt 4 -or $lines[0] -ne '---') {
        Add-Failure "Missing YAML frontmatter: $Path"
        return $text
    }

    $end = -1
    for ($i = 1; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -eq '---') {
            $end = $i
            break
        }
    }
    if ($end -lt 2) {
        Add-Failure "Unclosed YAML frontmatter: $Path"
        return $text
    }

    $keys = New-Object System.Collections.Generic.List[string]
    $name = $null
    for ($i = 1; $i -lt $end; $i++) {
        if ($lines[$i] -match '^([A-Za-z0-9_-]+):') {
            $key = $Matches[1]
            $keys.Add($key)
            if ($key -eq 'name') {
                $name = ($lines[$i] -replace '^name:\s*', '').Trim()
            }
        }
    }

    $unexpected = @($keys | Where-Object { $_ -notin @('name', 'description') } | Select-Object -Unique)
    if ($unexpected.Count -gt 0) {
        Add-Failure "Non-portable frontmatter key in ${Path}: $($unexpected -join ', ')"
    }
    if ($name -ne $ExpectedName) {
        Add-Failure "Skill name mismatch in ${Path}: expected $ExpectedName, got $name"
    }
    if ('description' -notin $keys) {
        Add-Failure "Missing description in $Path"
    }
    return $text
}

$canonicalRoot = Join-Path $repoRoot '.agents\skills'
$claudeRoot = Join-Path $repoRoot '.claude\skills'
$canonicalFiles = @(Get-ChildItem -Recurse -File -Filter 'SKILL.md' -LiteralPath $canonicalRoot)
$claudeFiles = @(Get-ChildItem -Recurse -File -Filter 'SKILL.md' -LiteralPath $claudeRoot)

if ($canonicalFiles.Count -ne $expectedSkills.Count) {
    Add-Failure "Expected $($expectedSkills.Count) canonical skills, found $($canonicalFiles.Count)."
}
if ($claudeFiles.Count -ne $expectedSkills.Count) {
    Add-Failure "Expected $($expectedSkills.Count) Claude entrypoints, found $($claudeFiles.Count)."
}

foreach ($skill in $expectedSkills) {
    $canonical = Join-Path $canonicalRoot "$skill\SKILL.md"
    $adapter = Join-Path $claudeRoot "$skill\SKILL.md"
    $canonicalRelative = ".agents/skills/$skill/SKILL.md"
    $adapterRelative = ".claude/skills/$skill/SKILL.md"
    if (-not (Test-Path -LiteralPath $canonical -PathType Leaf)) {
        Add-Failure "Missing canonical skill: $canonical"
        continue
    }
    if (-not (Test-Path -LiteralPath $adapter -PathType Leaf)) {
        Add-Failure "Missing Claude entrypoint: $adapter"
        continue
    }

    if ($RequireGitTracked) {
        foreach ($relativePath in @($canonicalRelative, $adapterRelative)) {
            $trackedPath = & git -C $repoRoot ls-files -- $relativePath
            if ($LASTEXITCODE -ne 0 -or $trackedPath -ne $relativePath) {
                Add-Failure "Skill file is not Git tracked: $relativePath"
                continue
            }
            $headPath = & git -C $repoRoot ls-tree -r --name-only HEAD -- $relativePath
            if ($LASTEXITCODE -ne 0 -or $headPath -ne $relativePath) {
                Add-Failure "Skill file is not present in HEAD: $relativePath"
            }
            $status = & git -C $repoRoot status --short -- $relativePath
            if ($status) {
                Add-Failure "Skill file has uncommitted changes: $relativePath"
            }
        }
    }

    $canonicalText = Test-Frontmatter $canonical $skill
    $adapterText = Test-Frontmatter $adapter $skill
    $expectedReference = ".agents/skills/$skill/SKILL.md"
    if (-not $adapterText.Contains($expectedReference)) {
        Add-Failure "Claude entrypoint does not reference canonical skill: $adapter"
    }
    if (($adapterText -split "`n").Count -gt 20) {
        Add-Failure "Claude entrypoint duplicates too much content: $adapter"
    }

    foreach ($deprecated in @('paper-repro-mvp', 'present_files', '/mnt/user-data', 'create_file', 'str_replace', 'skill_refy.md')) {
        if ($canonicalText.Contains($deprecated)) {
            Add-Failure "Deprecated token '$deprecated' found in canonical skill: $canonical"
        }
    }
}

$requiredFiles = @(
    '.agents\skills\paper-repro-skill-source-policy\SKILL.md',
    '.agents\skills\paper-repro-arch-guide\SKILL.md',
    '.agents\skills\arxiv-paper-repro\assets\assumption-ledger-template.md',
    '.agents\skills\arxiv-paper-repro\references\debug-playbook.md',
    '.agents\skills\arxiv-paper-repro\references\english-cues.md',
    '.agents\skills\arxiv-paper-repro\references\llm-paper-checklist.md',
    '.agents\skills\arxiv-paper-repro\references\sanity-checks.md',
    '.agents\skills\paper-repro-commit-output\references\commit-workflow.md',
    'docs\arch-guide\README.md',
    'docs\arch-guide\ccaf-patterns.md',
    'docs\arch-guide\claude-code-playbook.md',
    'docs\arch-guide\coverage-rubric.md',
    'docs\skills\agent-skills-operations.md',
    'package.json',
    'package-lock.json',
    'scripts\validate-mermaid.mjs'
)
foreach ($relativePath in $requiredFiles) {
    $path = Join-Path $repoRoot $relativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Add-Failure "Missing required skill resource: $relativePath"
    }
    else {
        [void](Get-Text $path)
    }
}

$commitOutputPath = Join-Path $repoRoot '.agents\skills\paper-repro-commit-output\SKILL.md'
$commitOutputText = Get-Text $commitOutputPath
$requiredChatOutputRules = @(
    'CHAT_URL_ONE_PER_TEXT_BLOCK',
    'CHAT_URL_TERMINAL_IS_NOT_FINAL',
    'CHAT_URL_INCLUDE_ALL_COMMITTED_FILES'
)
foreach ($rule in $requiredChatOutputRules) {
    if (-not $commitOutputText.Contains($rule)) {
        Add-Failure "Missing chat URL output rule in paper-repro-commit-output: $rule"
    }
}

$docsToCheck = @('AGENTS.md', 'CLAUDE.md', 'README.md', 'docs\README.md', 'docs\skills\agent-skills-operations.md')
foreach ($relativePath in $docsToCheck) {
    $path = Join-Path $repoRoot $relativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Add-Failure "Missing related document: $relativePath"
        continue
    }
    $text = Get-Text $path $false
    foreach ($skill in $expectedSkills) {
        if (-not $text.Contains($skill)) {
            Add-Failure "Related document does not mention ${skill}: $relativePath"
        }
    }
}

if ($failures.Count -gt 0) {
    Write-Output 'Agent skill validation failed:'
    foreach ($failure in $failures) {
        Write-Output "- $failure"
    }
    exit 1
}

$mode = if ($RequireGitTracked) { ' Git-tracked mode passed.' } else { '' }
Write-Output "Agent skill validation passed: $($expectedSkills.Count) canonical skills and $($expectedSkills.Count) Claude entrypoints.$mode"
