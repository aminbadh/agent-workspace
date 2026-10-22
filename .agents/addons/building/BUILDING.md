# Building: Overseer and Builders

How code gets built for any project this workspace plans. One session thinks, plans and keeps the docs true. Short-lived sessions build, one brief each. Long sessions that do everything are what this replaces: they mix strategy with diffs, lose the thread, and leave the docs behind the code.

A domain keeps only what is specific to it (its server, its reviewer, its demo pages) in its own `_working/`, and links here for the rest.

## Roles

- **Overseer.** A session started in this workspace. Thought partner and planner: it talks strategy with the user, owns the domain's plan, specs, `CONTEXT.md` and `DECISIONS.md`, writes each brief, and reviews what comes back. It reads code repos and never writes to them. It is **restartable**: everything it needs is in files, so a fresh overseer picks up from the domain's `CONTEXT.md`, its plan and the open briefs.
- **Builder.** A separate session started *inside the code repo* (in the background where the tool allows), so that repo's own instructions and settings load. One brief, its own branch (and worktree, where the tool makes one). It writes code, runs the checks, commits locally and stops. It never pushes, deploys, touches a server or edits the workspace.
- **Helpers.** Read-only subagents the overseer spawns for audits, research and review. They can run in parallel because they write nothing. They return a summary, not file dumps.
- **The user.** Decisions, pushes, deploys, anything that needs a login, an emailed code or root on a server. Each push or deploy is a separate go-ahead.

## The loop

1. **Orient.** Read the domain's `CONTEXT.md`, its plan and any open briefs. If the repo has moved since the docs were last reviewed, a read-only helper audits it first, so the brief's "Where it stands" is a fact and not a memory.
2. **Decide before briefing.** A brief that needs a decision nobody has made goes back to the user as a question. A builder that has to choose will choose, and that is how agents invent decisions.
3. **Brief.** Write `<domain>/_working/briefs/YYYY-MM-DD-<step>.md` from the template below. A builder sees no chat: anything it needs is in the brief or linked from it.
4. **Launch** the builder. In any tool, a builder is a separate session started **inside the code repo**, so the repo's own instructions load, given one line: `Execute the brief at ~/.links/workspace/<domain>/_working/briefs/<file>.md`. One brief per builder, each on its own branch (a worktree where the tool makes one). Start it in a new terminal or the tool's own background or cloud sessions, then come back to the overseer to review it. Not a subagent of the overseer: a subagent starts in the overseer's directory and does not load the repo's instructions.
   - **Claude Code**, from the overseer's shell, runs it in the background in its own worktree:
     ```bash
     cd ~/.links/projects/<repo> && claude --bg --name <step> "Execute the brief at ~/.links/workspace/<domain>/_working/briefs/<file>.md"
     ```
     Check a builder's real state with `claude agents --json` rather than trusting a "working" label.
   - **Codex, OpenCode and other tools:** open a new session in the repo (`cd ~/.links/projects/<repo>`, then start the tool there), make the brief's branch first if the tool does not (`git switch -c <step>`), and paste the one line above. The builder's final message is its report.
5. **Verify, in layers.** The builder shows command output for every check. A fresh reviewer then reads the branch diff against the brief and reports correctness and requirement gaps only, not style. **Give the reviewer paths, never the builder's report:** the brief's path, the repo and the branch. A pasted summary makes the reviewer grade the summary's framing instead of the code, which is how a review confirms what was never built. Then the overseer checks the acceptance list itself and runs the app for anything a person sees.
6. **Correct once.** Fixes go in a *Round 2* section appended to the same brief. If a second round is needed, write a fresh brief for a fresh builder instead of a third correction in the same session.
7. **Close.** Merge locally (`git merge --ff-only`). Update the plan, `CONTEXT.md` and `DECISIONS.md` in the same session, from the report's "Workspace facts this changes". Hand the user the push and the deploy as exact commands. Then end the builder's session and free its worktree.
8. **Restart the overseer** at natural breaks: a milestone, a planning session ending, or when the context feels heavy. Close it out by writing what is true into the files, not by compacting forever.

## Rules that keep it honest

- **One writer per area.** Two builders run at once only when their files *and* shared resources (a port, the database, a running API) do not overlap. Parallel writers make conflicting implicit choices.
- **Who updates what.** The builder keeps the repo's own docs true (its instructions file, README, docstrings) in its commits. The overseer alone edits the workspace. Repo docs cite workspace files by name, never copy them ([how another repo points at this one](#how-another-repo-points-at-this-one)).
- **Done means the checks passed, with output shown.** Not "tests pass", not a curl. Anything a user sees gets an end-to-end check, at phone width when the product is used on phones.
- **No spending before the user reviews.** Anything that costs money (paid API calls, imports that embed or transcribe, benchmarks) waits for the user's review of the free part. A brief splits into a free round and a paid round, never a dollar cap in place of consent.
- **Cheap helpers.** Audits and research run on smaller, cheaper models where the depth allows.
- **A claim that something is built names the module that implements it.** A plan or `CONTEXT.md` asserting what software does is the one kind of rot rereading never catches: the sentence stays coherent while the code is elsewhere. Naming the module makes checking it a search, and an unnamed claim visibly unverified.
- **No new state.** A brief is a dated, point-in-time file. The builder's report is its final message, not a file: the overseer copies only the outcome into the plan and `DECISIONS.md`, and commits already live in git.

## Setting up a repo

Once per code repo, so no brief has to remember it:

1. Its instructions file (`CLAUDE.md`, `AGENTS.md`) says **"Never push. The user pushes."** A background session in its own worktree may otherwise commit and push its branch on its own.
2. Its instructions file points at the workspace domain folder for context ([how another repo points at this one](#how-another-repo-points-at-this-one)).
3. If builders run in worktrees, the gitignored files they need (`.env`, local instructions) are listed for copying, since a fresh worktree has none of them: for Claude Code, in a `.worktreeinclude`. A builder working in the repo's own folder needs nothing here.
4. The repo is trusted once in an interactive session there, since most tools ask before working in a new folder and a background session may refuse to start instead of asking.
5. Reading `~/.links/workspace/` is allowed in the repo's settings, so a background builder never stalls on a permission prompt to read its brief.

## Paths across machines

Code repos need to reach this workspace for context, and the workspace may be cloned on more than one machine. A path written into a committed file therefore has to resolve on every machine, which rules out `/Users/<name>/...` and `/home/<name>/...`: each is dead text on the other box. Clone locations differ, and even folder names move, so the real path is not something a committed file can know.

The fix is one hidden namespace of symlinks in the home directory, identical on every machine, pointing at wherever things actually live there:

```
~/.links/workspace    this workspace
~/.links/projects     the folder holding code repos
```

Committed files reference `~/.links/workspace/<domain>/` and never the real path. `~` is resolved by the shell or the tool, the symlink by the filesystem, and the actual location behind it is free to change or differ per machine without touching a single document. The namespace is dotted so it stays out of a plain `ls ~`.

**Set it up once per machine**, from inside the workspace:

```bash
mkdir -p ~/.links
ln -sfn "$PWD" ~/.links/workspace
ln -sfn <the folder holding your code repos> ~/.links/projects
```

Once any file here writes a `~/.links/` path, the linter checks that `~/.links/workspace` exists and points at this workspace, and that every such path resolves, so a machine that never ran the setup says so out loud instead of failing quietly.

**Inside this workspace, none of that applies.** Use relative Markdown links ([CONVENTIONS.md](CONVENTIONS.md#linking)). `~/.links/` paths are strictly for reaching things that live *outside* it, and for other repos reaching in.

**Why symlinks:** a shell alias or environment variable is expanded only by an interactive shell, so no editor, agent, `git` or Python call ever sees one. A symlink is resolved by the filesystem, below every tool.

### How another repo points at this one

A code repo carries its own instructions file, committed and read on every machine. To give an agent working there the context that lives here, name the domain folder:

```markdown
## Context

Background, decisions and status for this project live in the workspace at
`~/.links/workspace/<area>/<domain>/`. Read its CONTEXT.md before planning work, and
DECISIONS.md before revisiting anything that looks settled.
```

Point at the folder, not a file list, so the reference survives the domain gaining a `_working/` document. And point at the domain, never at a copy: the workspace holds that context so the code repo does not have to, and two copies means one goes stale.

### Cite code repos by name, not by path

Going the other way, when a document here refers to a codebase, name the repo and say which machine has it: "the `shop-website` repo, the laptop only". Not a path.

Existence is per machine, not just location. A repo may be on one computer and not another, and no path scheme fixes a repo that is not there. A name is stable, an agent can find the repo from it, and the machine note explains why a search came up empty. Add a `~/.links/` entry for an individual repo only if something needs to reach it by path repeatedly.

## Brief template

```markdown
# Brief: <Step Name>

*Builder brief, YYYY-MM-DD. Serves <link to the plan item or spec>. Workflow: [BUILDING.md](<relative link>).*

## Goal
One paragraph: the observable end state, in terms a user or a check can see.

## Already decided (do not reopen)
Each with a link to the DECISIONS entry or spec that settled it.

## Where it stands
Dated facts from a fresh audit: files, current behaviour, what a previous builder found.

## Do
Numbered steps. "Look first" as step 1 when the work starts from a survey.

## Open questions: stop and report, do not choose
Anything the brief could not settle. Empty is fine; a guess is not.

## Constraints
Shared resources not to touch (ports, DB, a running API), money cap for paid calls, no push, no deploy, no workspace edits.

## Acceptance checks (show the output)
Commands, plus an end-to-end or visual check for anything a person sees.

## Report back
The standard report below.

## Out of scope
What a diligent builder would be tempted to do and must not.
```

## Standard report

Under 40 lines, as the builder's final message:

- **Status**: done, partial or blocked.
- **Branch and commits.**
- **Checks**: each one with trimmed output.
- **Choices this brief did not settle**, and what was chosen.
- **Found and left alone**: problems outside scope.
- **Workspace facts this changes**: anything a domain doc now says wrongly.
- **For the user**: exact commands or decisions, nothing done on their behalf.

## Why this shape

- Splitting writes across parallel agents produces conflicting implicit decisions; single-threaded writes with extra agents for review and search is the tested fix ([Cognition, Apr 2026](https://cognition.com/blog/multi-agents-working)). Coding has fewer truly parallel tasks than research ([Anthropic, multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system)).
- Delegation fails without an objective, an output format and boundaries: agents duplicate work or leave gaps (same source). The best specs name files and interfaces, say what is out of scope and end with an end-to-end check ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
- Builders one-shot too much and declare victory early; end-to-end checks and evidence in the report stop that ([long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
- Subagents return condensed summaries and keep the parent's context lean ([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)). A long-lived session re-sends its whole context every turn, which is why the overseer restarts from files ([costs](https://code.claude.com/docs/en/costs)).
- Background sessions, idle notices and worktree behaviour in Claude Code: [agent view](https://code.claude.com/docs/en/agent-view), [cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging), [subagents](https://code.claude.com/docs/en/sub-agents). Some of these are previews, so commands may change.
