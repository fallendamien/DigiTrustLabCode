# Executive Assistant Schedules

These are the intended recurring jobs for the pilot. They create drafts and
recommendations only; they never send, schedule, publish, or modify external
systems.

Timezone: `Asia/Kuala_Lumpur`

## Daily brief

- Cadence: weekdays
- Target time: 08:00 local time
- Skill: `skills/daily-brief/SKILL.md`
- Inputs: today's calendar, selected recent Gmail threads, `memory.md`
- Output: facts, priorities, preparation items, draft replies, approval queue

## Weekly review

- Cadence: Friday, within the scheduled morning run
- Target time: 08:00 local time (the thread supports one heartbeat schedule)
- Skill: `skills/daily-brief/SKILL.md` with weekly-review mode
- Inputs: the week's calendar, selected email action items, unresolved EA
  context, `memory.md`
- Output: completed items, open loops, next-week priorities, proposed memory
  updates

The Codex heartbeat runs the daily brief Monday through Thursday and switches
to weekly-review mode on Friday. The schedule is not evidence that a job has
run; each run must produce its own evidence and limitations section.
