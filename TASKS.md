# Tasks and Dates

How this workspace works alongside a task app (Notion, Todoist, Things, Linear, a paper
notebook). Fill in the second half with your own app's setup.

## The boundary

**The task app holds anything row-shaped with a live status**: tasks, projects, trackers,
content calendars, and every date you act on. **These files hold reasoning, decisions and
context.** A `CONTEXT.md` links to the project in the task app rather than copying its tasks,
because a copied task is a stale task.

Why the split works: a task app is good at surfacing what is due and bad at holding why. A
folder of Markdown is the opposite. Each does the job it is good at, and the link between them
is one line.

## Rules agents follow

- **Never copy a date into these files.** Link to the project instead. (See
  [CONVENTIONS.md](CONVENTIONS.md#dates).)
- **Task names are short actions**, verb first: "Draft Launch Email", not "the launch email
  thing".
- **A task body stays nearly empty.** A constraint or a step order that would otherwise be
  forgotten, nothing more. Reasoning goes in the domain's files, and the task can say where.
- **Search before creating.** Check the task or project does not already exist under another
  name.
- **Set targets before deadlines.** A due date is a target with slack, never the real deadline.

## My setup

*Replace this section.* Name your app, where tasks and projects live, and anything an agent
needs to write to it correctly: the project names, the fields that matter, how "done" is marked.
If your agent can reach the app directly (through an MCP server or an API), say so here.
