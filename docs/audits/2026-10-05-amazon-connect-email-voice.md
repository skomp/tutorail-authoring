# Course quality audit: `amazon-connect-email-voice`

Audited 2026-10-05 against `tutorail-authoring:course-quality` v0.4.0 and its rubric
(`skills/course-quality/references/rubric.md`).

Bundle under audit:
`skomp/tutorail-bundles`, `amazon-connect-email-voice/`
(branch `worktree-amazon-connect-email-voice`, HEAD `b737857`).

Read-only. No file in the bundle or the repository was created, edited, staged or deleted,
and no git command that changes state was run. SHA-1 checksums of every bundle file were
taken at the start and at the end of the audit and are identical.

**Status after this audit (2026-10-05).** The bundle was not yet delivered, so the plain
defects were fixed before its first pull request, in `skomp/tutorail-bundles` commit
`216d564`: proposals 1, 2, 3, 4, 5, 7, 8, 9, 11 and 12, and the gap half of proposal 6
(lesson 08 now explains what AI agents would add). Still open for the author, tracked in
skomp/tutorail-bundles#33: proposal 10 (lesson 06's `cdk diff` demonstration), and the two
thin coverage halves of proposal 6 ("what bills per email", "what never to put into an
attribute"). The scores below are the audit as run, on HEAD `b737857`, before the fixes.

Every finding below is a **proposal**. Applying any of them is the `tutorail-authoring`
skill's job, after the author says yes.

Format: the same shape as the reports in `docs/audits/2026-09-13/`.

---

## The rubric (printed as required)

### Scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises (course-level, counted once per gap) |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised (course-level) |

### Two elements settled by the rubric, not by me

- **A branch point** (the lesson offers the learner a choice of paths) scores **evidence, 0**.
- **A tutor-addressed element scores teaching, +2, when the learner must decide or construct
  in response.** Grammatical person does not change what the learner does. Most of lessons
  03–08 are written to the tutor ("Have them…", "Ask the learner…"); they are scored by what
  the learner does.

### Rows a reader answers and a script never scores

- a `design_refs` entry that does not answer the question its lesson raises;
- a lesson that introduces a type or concept nothing later uses;
- a symbol or term a lesson uses and no lesson introduces (first use; "bound only in
  `DESIGN.md`" kept apart from "bound nowhere");
- whether the lesson file equips the tutor to end a turn with one concrete action (graded on
  the file, for every lesson);
- a lesson far outside the course's usual size, in either direction;
- a must-cover topic that only an optional lesson teaches — **a question, permanently, not a
  score**.

### The invariant no structural check can reach

> A course carrying optional lessons must be completable by a learner who declines every offer.

All of these are answered in writing in section 6.

### Scoring conventions I applied (so the author can argue with them)

- This course's `## Suggested progression` is written in **two house styles**: hard-wrapped
  paragraphs of imperative sentences (lessons 00, 01, 02, 06, 07, 08) and numbered steps
  (03, 04, 05). I scored **each distinct learner act** — normally one imperative sentence,
  split where one sentence carries two acts of different kinds — in both styles. Even so,
  the paragraph lessons enumerate more finely than the numbered ones, so the within-course
  comparison is itself bent by house style. Section 6.5 says where that shows.
- Every `## Completion conditions` bullet is scored. A condition that **re-checks** work
  already scored in the progression scores **0**; "the learner can explain …" scores **+2**.
- `## Constraints` and `## Theory` lines are scored **only** where they impose a learner act
  that appears nowhere in the progression. Two such lines exist, both in lesson 04
  (`:198-199` and `:99-101`).
- **Contingent instructive failures are not scored.** A block of the form "*Instructive
  failure, if the learner reaches for it: …*" or "If they say X, …" happens only when the
  learner makes that mistake; it is the course's safety net, not a task every learner does.
  Scoring it as teaching would bank points a correct learner never earns. They are listed
  under each lesson as "not scored", so the author can see them. A **planned** failure — one
  the progression tells every learner to provoke ("meet the third instructive failure on
  purpose") — is scored.
- Optional repetitions the lesson itself offers ("if you have the time", "Optionally, …")
  are scored **+1** as practice.
- The supplied tools (`tools/load_customers.py`, `tools/scenarios.py`) are run, not written;
  running one scores **0**.

**Totals are comparable within this course, never against another course.**

---

## 1. The course and its total

| | |
|---|---|
| Bundle id | `amazon-connect-email-voice` |
| Title | Amazon Connect: an Email-and-Voice Contact Centre as Code |
| Main-path lessons | 9 |
| Optional lessons | 0 (no `optional_lessons:` key in `tutorial.yaml` — read directly) |
| Lesson rows scored | 9 |
| `supplies:` entries | 15 — 12 manifest-scope, 3 lesson-scope (lessons 04 and 05) |
| `DESIGN.md` anchors | 5 |
| Coverage list | present, 6 topics (`COURSE.md:90-109`) |
| Validator | `validate_bundle.py` (tutorail runner, marketplace copy): **PASS**, 25 checks ran, 4 n/a |

**Arithmetic**

```
  lesson 00-instance-and-first-agent         27
  lesson 01-first-email-contact              35
  lesson 02-hours-queues-routing-profiles    35
  lesson 03-flow-logic-for-email             17
  lesson 04-lambda-enrichment                30
  lesson 05-following-a-contact              17
  lesson 06-a-phone-line                     30
  lesson 07-voice-menu-and-caller-lookup     22
  lesson 08-one-agent-two-channels           14
  --------------------------------------------
  sum of lessons                            227
  − unserved objectives (1 × −3)             −3   (COURSE.md:108 "ai agents and q in connect")
  − unserved anchors    (0 × −3)              0
  − required_for gates  (0 × −3)              0
  --------------------------------------------
  COURSE TOTAL                              224
```

Re-added: 27 + 35 = 62; + 35 = 97; + 17 = 114; + 30 = 144; + 17 = 161; + 30 = 191;
+ 22 = 213; + 14 = 227; − 3 = **224**. Each lesson's figure below is the visible sum of its
own rows, re-added independently with a script over the tables in section 2 (all nine agree).

**No `required_for` gate exists**, so the rubric's −3 row does not fire and its warning is not
printed. I keyed that off the absence of an `optional_lessons:` key in `tutorial.yaml`
(`:1-151`), not off the evidence script's `0 optional`.

**The validator is green and the course still has real defects** (section 5, proposals 1–4):
a lesson 08 test that the supplied script cannot set up as written, a lesson 04 observation
no step produces, an experiment the supplied loader refuses, and a design decision with no
step. No structural check can see any of them.

---

## 2. The per-lesson table

| Lesson | Score | Objectives served | Toil found | Closing action |
|---|---:|---|---|---|
| `lessons/00-instance-and-first-agent.md` — Instance and first agent | **27** | 7 of 7 | none | pass |
| `lessons/01-first-email-contact.md` — First email contact | **35** | 7 of 7 | none | pass |
| `lessons/02-hours-queues-routing-profiles.md` — Hours, queues and routing profiles | **35** | 7 of 7 | none | pass |
| `lessons/03-flow-logic-for-email.md` — Flow logic for email | **17** | 6 of 6 | none | pass |
| `lessons/04-lambda-enrichment/LESSON.md` — Lambda enrichment | **30** | 6 of 6 | none | **fail** (`:198-199`) |
| `lessons/05-following-a-contact/LESSON.md` — Following a contact | **17** | 6 of 6 | none | pass |
| `lessons/06-a-phone-line.md` — A phone line | **30** | 7 of 7 | none | pass |
| `lessons/07-voice-menu-and-caller-lookup.md` — Voice menu and caller lookup | **22** | 7 of 7 | none | pass |
| `lessons/08-one-agent-two-channels.md` — One agent, two channels | **14** | 6 of 6 | none | pass |

No lesson scores at or below zero, so the rubric requires no what-is-this-for question. The
closing-action fail is carried into section 6.4. Full element breakdowns follow for all nine,
because no figure is obvious from its row.

### `lessons/00-instance-and-first-agent.md` — 27

| file:line | Sentence (or the act it names) | Score |
|---|---|---:|
| `:242-245` | "Start with your own setup, which the bundle cannot do for you. Install the CDK CLI …, create a virtualenv in the workspace, activate it, and install the development requirements …" | 0 (learner's setup: network and toolchain) |
| `:245-252` | "Then choose your **region**." … "Set the region **once, in your AWS configuration** …, never in the code." | +2 |
| `:252` | "Run `cdk bootstrap` for that account and region." | 0 (account setup) |
| `:252-254` | "Confirm that `cdk synth` succeeds on the empty skeleton before you add anything …" | 0 |
| `:256-258` | "Choose your alias before you write it down. Pick the prefix, say the full alias aloud, and check it against the rules in *Theory*." | +2 |
| `:260` | "Write the instance in `CoreStack`: `CONNECT_MANAGED`, your alias, and the attributes." | +2 |
| `:260-261` | "Decide `InboundCalls` and `OutboundCalls` and be ready to say why." | +2 |
| `:261` | "Add the three outputs." | +1 |
| `:261-264` | "Before deploying, write the test: … assert that the template declares the instance with the identity mode you meant." | +1 |
| `:264` | "Run the tests and `cdk synth`." | 0 |
| `:266-267` | "Deploy `ConnectCore` and wait for the instance to become usable …" | 0 |
| `:267-268` | "Then change the alias in your code — locally only — and run `cdk diff ConnectCore`. Read what CDK says will happen to the instance." | +2 |
| `:269-270` | "Do the same thought experiment for the identity mode." | +1 |
| `:273-275` | "Before you write the user, predict. … Which of the two decides what contacts the agent will be offered? Say your answer and your reason …" | +2 |
| `:275-277` | "… look at both defaults … Revise your prediction against what you saw." | +2 |
| `:279-282` | "Find the two default ARNs … and put them in `RoutingStack` as clearly named constants with a comment that says where they came from …" | +1 |
| `:282-283` | "Write the `CfnUser` in `RoutingStack`, reading the instance ARN from the core stack it receives." | +2 |
| `:283-284` | "Decide how the password reaches the user without becoming a literal in your code or a value in the repository …" | +2 |
| `:286-288` | "… ask yourself the stack-split question out loud: what does `cdk destroy ConnectRouting` do to your contact centre now?" | +2 |
| `:288` | "Deploy `ConnectRouting`." | 0 |
| `:290-293` | "Log in as the agent at the CCP URL … Change your status from **Offline** to **Available**." | +1 |
| `:298-300` | "`ConnectCore` is deployed and declares one `AWS::Connect::Instance` …" | 0 |
| `:301-303` | "`ConnectRouting` is deployed and declares the agent user …" | 0 |
| `:304` | "No password, account id or region is a literal in the code …" | 0 |
| `:305` | "The `cdk-synth` validator passes." | 0 |
| `:306-307` | "The `pytest` validator passes, and `tests/` contains a test …" | 0 |
| `:308-309` | "The `instance-live` validator passes." | 0 |
| `:310-311` | "You have logged in to the CCP as the agent and set the status to **Available**, and you say so …" | 0 |
| `:312-315` | "You can explain, without notes: why the alias and identity mode can never change; … which of the security profile and the routing profile decides …" | +2 |

Sum: 0+2+0+0+2+2+2+1+1+0+0+2+1+2+2+1+2+2+2+0+1+0+0+0+0+0+0+0+2 = **27**.

Not scored (contingent): none. The two strongest elements are `:267-268` (the permanence of
the alias is met safely, in a `cdk diff`, before it can cost an instance) and `:273-277`
(predict, look, revise).

### `lessons/01-first-email-contact.md` — 35

| file:line | Sentence (or the act it names) | Score |
|---|---|---:|
| `:206-209` | "In the Connect console, open your instance's **Email** page, choose **Create service role**, then **Add domain** … Read back the domain …" | 0 (console-only, in the learner's account; serves `:36-37`) |
| `:211-216` | "List the instance's storage configurations … If either already exists, you have a decision to make before you write code …" | +2 |
| `:218-220` | "Write the bucket and the two storage configurations in `CoreStack`. Decide one bucket or two, the prefixes, the encryption, the CORS rule …, and what happens to the bucket's contents at teardown." | +2 |
| `:220` | "Write the `CfnEmailAddress` and its two outputs." | +2 |
| `:220-222` | "Deploy `ConnectCore`. If the address or a storage configuration fails to create, read the CloudFormation event message …" | 0 |
| `:224-228` | "Draw the flow. … Add **Set working queue** … then **Transfer to queue**, and send every error and at-capacity branch to a block that ends the contact. Save it, then use **Export flow** …" | +2 |
| `:230-232` | "Open the file. Search it for `arn:` and look at every hit … Replace each ARN with a placeholder …" | +2 |
| `:232-234` | "The BasicQueue ARN is another looked-up value you do not own; you know from lesson `00-…` what to call that …" | +1 |
| `:234-235` | "Write a test that reads `flows/inbound-email.json` and fails if it contains an ARN." | +1 |
| `:237-238` | "Write the `CfnContactFlow` in `RoutingStack`: read the file, pass it through `Fn.sub` with the map …" | +2 |
| `:238-239` | "Add the `InboundEmailFlowId` output, and check after deploying that its value really is an id and not the flow's name." | +1 |
| `:240` | "Now stop, and predict: deploy only this, send an email to your address, and what happens?" | +2 |
| `:240-245` | "Deploy `ConnectRouting`, send a short email … look for the contact in the admin website's contact search … and tell the tutor what you found." | +1 |
| `:247-249` | "Write the association as an `AwsCustomResource` …: `AssociateFlow` … on create and update, `DisassociateFlow` on delete, and a policy limited to those calls." | +2 |
| `:249-250` | "… find out from the API's behaviour and record what you learned." (id or ARN as `ResourceId`) | +2 |
| `:250-251` | "Deploy `ConnectRouting`." | 0 |
| `:253-256` | "Before you send again, check your routing profile … Does it enable email? Does it work BasicQueue on the email channel?" | +2 |
| `:256-258` | "… you can see it happen by sending an email now." | 0 |
| `:258-261` | "… discuss with the tutor whether to change the default profile by hand as recorded, temporary state, or to bring the course's own routing profile forward. Either way, write down what you did." | +2 |
| `:263-266` | "Read your account's SES status … with `aws sesv2 get-account` … If it is `false`, … verify your own mailbox's address …" | +2 |
| `:268-269` | "Send the email again. Accept the contact in the CCP, read it, and reply. Confirm the reply reaches your mailbox." | +1 |
| `:271-275` | "… meet the third instructive failure on purpose. Open your **deployed** flow …, make a small visible change … Deploy `ConnectRouting` without changing the file … Now make any small change to `flows/inbound-email.json`, deploy again, and look a second time." | +2 |
| `:275-276` | "Explain to the tutor what happened, and why the first deploy did not remove your edit and the second did." | +2 |
| `:276-277` | "Leave the deployed flow equal to the file, and delete the scratch copy …" | 0 |
| `:281-283` | "`ConnectCore` declares the message bucket, two `AWS::Connect::InstanceStorageConfig`s …" | 0 |
| `:284-287` | "`ConnectRouting` declares the inbound flow …" | 0 |
| `:288` | "`flows/inbound-email.json` contains no ARN, and a test in `tests/` fails if it ever does." | 0 |
| `:289` | "The `cdk-synth` and `pytest` validators pass." | 0 |
| `:290-293` | "The `email-routed` validator passes. …" | 0 |
| `:294` | "The reply you sent from the CCP has reached your mailbox, and you say so to the tutor." | 0 |
| `:295-298` | "You can explain, without notes: what would have happened to an email if the association were missing; the two places a routing profile must name the email channel; …" | +2 |

Sum: 0+2+2+2+0+2+2+1+1+2+1+2+1+2+2+0+2+0+2+2+1+2+2+0+0+0+0+0+0+0+2 = **35**.

Not scored (contingent): none. The lesson builds **three planned failures** into its
progression (`:240-245`, `:256-258`, `:271-275`), each met before its fix — the highest
density of planned instructive failures in the course.

### `lessons/02-hours-queues-routing-profiles.md` — 35

| file:line | Sentence (or the act it names) | Score |
|---|---|---:|
| `:179` | "Write `CfnHoursOfOperation` with a schedule that is open now, and say what time zone it is in." | +2 |
| `:180` | "Write `CfnQueue` for the course queue with those hours." | +1 |
| `:180-182` | "Write `CfnRoutingProfile` with the course queue as its default outbound queue, and with media concurrencies and queue configs as you judge they should be." | +2 |
| `:182` | "Move your user onto it, and delete the Basic Routing Profile constant." | +1 |
| `:182-183` | "If you changed the default profile by hand in lesson `01-…`, put it back." | 0 |
| `:183-184` | "Add the `CourseQueueId` output." | +1 |
| `:186-189` | "… draw the change on a scratch flow that holds real values … Whether the designer will import a file that still carries `${...}` placeholders is something to find out, not assume." | +2 |
| `:189-190` | "Set the working queue to your new course queue, export, and replace the ARN with `${CourseQueueArn}`." | +1 |
| `:190-191` | "Update the `Fn.sub` map so it fills the placeholder from your queue, and remove the BasicQueue entry." | +1 |
| `:191-193` | "Extend your tests: the routing profile has an email concurrency and a queue config …, and the user's routing profile is the one the stack declares." | +1 |
| `:193-194` | "Deploy `ConnectRouting`, go Available, send an email, and accept it." | 0 |
| `:196-197` | "Remove email from one of the two places it must appear in the routing profile — your choice which — deploy, and send an email …" | +2 |
| `:198` | "Predict before you look: is the email lost, refused, or something else?" | +2 |
| `:198-199` | "Find the contact and say where it is and why you were not offered it." | +2 |
| `:199-200` | "Then put the routing profile right, deploy, and watch the waiting email be offered to you." | 0 |
| `:200-201` | "Do it once more with the *other* place, if you have the time …" | +1 (optional repetition) |
| `:203-204` | "Before you add any check to the flow, predict: if you change the course hours so that now is *closed*, and send an email, what happens?" | +2 |
| `:204-206` | "Change the schedule in code …, deploy, send an email, and see what the agent is offered. Explain to the tutor what you observed and what it says about what hours do on their own." | +2 |
| `:208-211` | "Add the decision. Decide first, and say it to the tutor: what should an email that arrives out of hours get?" | +2 |
| `:212-214` | "… add **Check hours of operation** — decide whether it checks the working queue's hours … or names the hours itself through a `${HoursArn}` placeholder …" | +2 |
| `:214-216` | "… and on each branch a **Set contact attributes** that sets `route_reason` on the current contact …" | +2 |
| `:216` | "Lead the **Error** branch somewhere you can recognise." | +1 |
| `:217` | "Export, placeholder every ARN, update the map, extend your tests, and deploy." | +1 |
| `:219-221` | "With the hours still closed, send an email, accept it, and find `route_reason` on the contact in its record, through contact search …" | 0 |
| `:221-222` | "Then change the schedule back …, deploy, send another email, and find `route_reason` again." | 0 |
| `:222` | "Each time, tell the tutor what you expect before you look." | +1 |
| `:222-223` | "Leave the hours set to the schedule you actually mean, and record it." | +1 |
| `:227-230` | "`ConnectRouting` declares an `AWS::Connect::HoursOfOperation`, …" | 0 |
| `:231-233` | "The agent user's routing profile is the stack's own; …" | 0 |
| `:234-235` | "The flow contains **Check hours of operation** …" | 0 |
| `:236-237` | "The `cdk-synth` and `pytest` validators pass, with tests that assert …" | 0 |
| `:238-240` | "The `email-routed` validator passes for an email sent during hours …" | 0 |
| `:241-244` | "The `email-routed` validator also passes for an email sent while the hours were changed to closed …" | 0 |
| `:245-248` | "You can explain, without notes: what a queue's hours do when no flow checks them; …" | +2 |

Sum: 2+1+2+1+0+1+2+1+1+1+0+2+2+2+0+1+2+2+2+2+2+1+1+0+0+1+1+0+0+0+0+0+0+2 = **35**.

`:222` is scored +1 rather than +2: by that point the learner built the branch that sets
`route_reason`, so the prediction applies what they wrote rather than deciding anything new.

### `lessons/03-flow-logic-for-email.md` — 17

| file:line | Sentence (or the act it names) | Score |
|---|---|---:|
| `:207-211` | "**Decide the rule.** … which attribute, which operator, which value, and what happens to `Urgent` and `URGENT`. … the learner either lists the variants they accept or decides that only one spelling counts — and records which." | +2 |
| `:211` | "Write down the `route_reason` values for every path, including out-of-hours." | +1 |
| `:212-214` | "**Write the guard test.** A pytest test that reads `flows/inbound-email.json` and fails if the text contains `arn:aws:`. Run the suite: it should pass on the current file …" | 0 (lesson 01 `:234-235` already wrote this test; see proposal 5) |
| `:214-217` | "A second assertion worth adding: every `${Name}` in the file is a key in the substitution map the stack passes to `Fn.sub` …" | +1 |
| `:218-219` | "**Add the priority queue** in `ConnectRouting` with output `PriorityQueueId`, add it to the routing profile on the email channel, add `PriorityQueueArn` to the placeholder map." | +1 |
| `:219-220` | "Extend the template tests: two queues, the routing profile lists both, the output exists." | +1 |
| `:220-221` | "Deploy the routing stack; the flow is unchanged so far." | 0 |
| `:222-225` | "**Draw the branch** … a Check contact attributes block on the subject; on the match, Set contact attributes (`route_reason`) and Set working queue (priority); on No match, the same pair for the default path. Make sure the out-of-hours path sets its `route_reason` too." | +2 |
| `:231-233` | "**Add the acknowledgement** with Send message: plain text, From = System email address, To = Customer endpoint address, … Link to contact decided and recorded. Wire both Success and Error onward to routing." | +2 |
| `:233-235` | "Ask before they place it: which flow does the outbound email contact it creates run, and what would happen if this block were in that flow?" | +2 |
| `:239-240` | "**Export and replace.** Export the flow, write it over `flows/inbound-email.json`, and run the tests before replacing anything." | 0 |
| `:241-245` | "… The guard test fails. The learner replaces each with its placeholder … until the suite passes and `cdk synth` succeeds." | +1 |
| `:245` | "Deploy." | 0 |
| `:246-249` | "**Test both ways.** The learner sends two emails … one whose subject matches the rule, one that does not. … The tutor runs `email-routed` after each." | 0 |
| `:249-251` | "Then the learner reads `route_reason` and the queue for each contact … and confirms they differ in the way the rule predicts." | +1 |
| `:251-252` | "Optionally, a third email with the keyword in a different case shows the case rule they chose actually holds." | +1 (optional repetition) |
| `:256-258` | "`cdk-synth` passes, and `pytest` passes with: …" | 0 |
| `:259-260` | "`ConnectRouting` is deployed and publishes `PriorityQueueId`; …" | 0 |
| `:261-264` | "Two test emails sent by the learner during hours: … the learner shows the queue and `route_reason` of both contacts from the contact record …" | 0 |
| `:265-267` | "The learner received the automatic acknowledgement in their own mailbox, or can name the evidence for why it was not delivered …" | 0 |
| `:268` | "The out-of-hours path sets `route_reason` too; the learner points to it in the exported JSON." | 0 |
| `:269-271` | "The learner can explain: why a branch on an attribute nothing set takes No match silently; why Send message must not sit in the Default outbound flow; what a Play prompt block does to an email contact; and why the export may not contain an ARN." | +2 |

Sum: 2+1+0+1+1+1+0+2+2+2+0+1+0+0+1+1+0+0+0+0+0+2 = **17**.

Not scored (contingent): `:226-230` (branching on a user-defined `EmailSubject` that nothing
set) and `:236-238` (a Play prompt "to say thank you"). Both are this lesson's two richest
teaching moments and both fire only if the learner makes the mistake; objective `:47-48`
("Recognise three instructive failures …") is nonetheless served, by the explanation at
`:269-271`. Had both been scored at +2 the lesson would read 21. That gap, and the
numbered-step house style, are most of why this lesson sits at half of lessons 01 and 02.

### `lessons/04-lambda-enrichment/LESSON.md` — 30

| file:line | Sentence (or the act it names) | Score |
|---|---|---:|
| `:205-210` | "**Shape the contract in tests first.** The learner writes pytest tests for the handler before the handler, with hand-built fake events … an email event for a known sender in mixed case …; an email event for an unknown sender returns `{}`; … every value returned is a `str` …; a lookup failure raises." | +2 |
| `:209-212` | "… a **voice** event with an E.164 `CustomerEndpoint.Address` finds a phone record; … The voice test must pass in this lesson …" | +2 |
| `:219-220` | "**Write the handler** until the tests pass. Keep normalisation in one function the tests can call directly." | +2 |
| `:220` | "Add the contact-id log line." | +1 |
| `:221-222` | "**Add the table and the function** to `ConnectRouting`, with the outputs, read-only access, and a timeout below 8 seconds." | +1 |
| `:222-223` | "Template tests: the table's key schema, the function's timeout, the outputs." | +1 |
| `:224` | "**Add the grants.** The integration association first, alone." | +2 |
| `:224-225` | "Ask the learner to predict what happens when a contact reaches the block with only that." | +2 (see proposal 2: nothing lets them check it) |
| `:225-226` | "Then the Lambda permission, scoped to the instance ARN." | +2 |
| `:226` | "Template tests for both, including that the permission carries a source ARN." | +1 |
| `:227` | "**Load the customers.** Deploy, then run `tools/load_customers.py` against the table." | 0 (supplied tool, run) |
| `:227-231` | "Then the learner adds **their own** record with the loader's `--add-endpoint <their address> --tier gold --name "<their name>"`. …" | 0 |
| `:232-234` | "**Wire the flow.** … the AWS Lambda function block (synchronous, timeout, `STRING_MAP`), then Set contact attributes copying the three values, then a Check contact attributes on `tier`. Gold sets `route_reason=tier-gold` and the priority queue." | +2 |
| `:234-236` | "The Error branch goes somewhere the learner chooses and defends …" | +2 |
| `:236-237` | "Export, replace the function ARN with `${LookupFunctionArn}`, add it to the placeholder map, let the guard test confirm, deploy." | +1 |
| `:198-199` (Constraints) | "The learner decides, and records, which wins when a gold customer sends an urgent subject." | +2 (a learner act no progression step carries; see 6.4 and proposal 4) |
| `:99-101` (Theory) | "Treat it as something to find out on your own instance: return a display name with a space, and read what the contact record and the flow log show. Record the result." | +2 (a learner act no progression step carries; see proposal 3) |
| `:240-242` | "**Test the happy paths.** The learner emails from their own mailbox: … The tutor runs `lambda-enriches`." | 0 |
| `:242-245` | "Then the learner removes their record with `--remove-endpoint`, emails again, and the contact takes the unknown-customer path. Re-add the record afterwards …" | 0 |
| `:246-249` | "**Break it on purpose.** The learner designs a failure switch … They choose, and say what each costs …" | +2 |
| `:250-252` | "With the switch on, an email takes the Error branch, and the learner finds the evidence: the function's CloudWatch log shows the invocations (count them — Connect retries), and the contact shows the Error path's `route_reason`." | +1 |
| `:252-253` | "Then the switch goes **off**, and one more email proves the happy path is back." | 0 |
| `:257-262` | "`cdk-synth` passes. `pytest` passes, including: …" | 0 |
| `:263-265` | "`ConnectRouting` publishes `LookupFunctionName` and `CustomersTableName`. …" | 0 |
| `:266-268` | "`lambda-enriches` passes for an email the learner sent from their own address …" | 0 |
| `:269-270` | "An email from an address not in the table took the unknown-customer path …" | 0 |
| `:271-273` | "With the failure switch on, an email took the Error branch; …" | 0 |
| `:274-277` | "The learner can explain: why the handler branches on `Channel` and not on `CustomerEndpoint.Type`; why a nested response fails only at run time; which of the two grants CloudFormation does not create; …" | +2 |

Sum: 2+2+2+1+1+1+2+2+2+1+0+0+2+2+1+2+2+0+0+2+1+0+0+0+0+0+0+2 = **30**.

Not scored (contingent): `:213-215` (a nested response), `:216-218` (an email-only
normaliser), `:238-239` (a skipped Error branch). If the author rules that the Constraints
line `:198-199` and the Theory line `:99-101` are not elements, this lesson reads **26** and
the course **220**.

### `lessons/05-following-a-contact/LESSON.md` — 17

| file:line | Sentence (or the act it names) | Score |
|---|---|---:|
| `:169-170` | "**Check the Lambda log line.** … find a contact id in the lookup function's log, or add the line, redeploy, confirm tests pass." | 0 |
| `:171-172` | "**Run the scenarios as the code stands.** The learner runs `tools/scenarios.py` and notes the three ids." | 0 (supplied tool, run) |
| `:172-173` | "They then try to explain A. Contact search finds it and the record shows its queue and attributes. Then they look for its flow log." | +2 |
| `:174-176` | "*Instructive failure, by design if logging is not yet on:* … Ask why, and whether turning logging on now will produce A's log." | +2 (planned: lesson 00 `:224` forbids setting `ContactflowLogs`, so every learner meets it) |
| `:179-183` | "**Enable both halves.** `ContactflowLogs` on the instance in `ConnectCore` (… check the diff says so before deploying), and a Set logging behavior block at the top of the inbound email flow …" | +2 |
| `:184-185` | "**Run the scenarios again.** New ids for A, B and C …" | 0 |
| `:187-188` | "the record: `describe-contact` (channel, initiation method, `QueueInfo`) and `get-contact-attributes` …" | +2 |
| `:189-190` | "the flow log: searched in `/aws/connect/<alias>` by the contact id … read in timestamp order, block by block;" | +2 |
| `:191` | "the Lambda log for the same contact id, if the contact reached the Lambda block." | +2 |
| `:192-193` | "Then a short written explanation: branch taken, queue reached (matched to `CourseQueueId` or `PriorityQueueId`), and the attribute that decided it, with the citation beside each." | +2 |
| `:199-202` | "**Look at the acknowledgement.** … The learner finds what the flow log shows for the Send message block, and confirms the contact was routed regardless …" | +1 |
| `:206-208` | "Flow logging is on: … Both are deployed. The guard test and the rest of the test suite pass." | 0 |
| `:209` | "The lookup Lambda logs the contact id on every invocation." | 0 |
| `:210-219` | "**`contact-explained`** (manual) is satisfied. For **each** of A, B and C …" | 0 (re-checks `:186-193`) |
| `:220-221` | "The learner can explain why the first run's contacts have no flow log and never will, and why the agent workspace is not the routing record." | +2 |

Sum: 0+0+2+2+2+0+2+2+2+2+1+0+0+0+2 = **17**.

Not scored: `:194-196` and `:197-198` (contingent: opening the flow file first; relying on the
workspace); `:182-183` "let them find the second half rather than naming it" (contingent on
enabling one half); `:222-228` (an instruction to the tutor that asks nothing of the learner).

### `lessons/06-a-phone-line.md` — 30

| file:line | Sentence (or the act it names) | Score |
|---|---|---:|
| `:204` | "Start with the decision, not the code. Ask the learner where the number goes and why." | +2 |
| `:214-217` | "Have them look up their own country in the AWS page "Region requirements for ordering and porting phone numbers", and tell you what it asks for." | +2 |
| `:218-220` | "Then name the three costs: the international call, the latency, and the daily charge. Point at `COURSE.md`, *When you are finished*, now …" | 0 (the tutor names and points) |
| `:222` | "Write the `CfnPhoneNumber` and the two outputs …" | +2 |
| `:222-224` | "… and a test in `tests/` that asserts on the core template: … and `ConnectRouting` contains no `AWS::Connect::PhoneNumber`." | +1 |
| `:224-225` | "Have them confirm `InboundCalls` is on in the instance attributes." | 0 |
| `:225-227` | "Then deploy `ConnectCore` (read the diff first). Look at the `PhoneNumber` output … note that a US number dialled from abroad needs the international prefix …" | 0 |
| `:229-234` | "Now the flow. … The flow is: Set logging behavior; a Play prompt with text-to-speech (a short greeting they write); the same Check hours of operation …; Set working queue …, then Transfer to queue; on the out-of-hours branch, a Play prompt that says they are closed, then Disconnect / hang up." | +2 |
| `:234-235` | "Wire every Error branch somewhere deliberate." | +1 |
| `:235-237` | "If the email flow sets `route_reason`, set it here on each path too, with the values they used for email …" | +1 |
| `:239-242` | "Before they export, ask what would happen if they had pointed the number at `flows/inbound-email.json`. Have them answer from the channel tables of the blocks that flow contains …" | +2 |
| `:246-248` | "Export the flow. Save it as `flows/inbound-voice.json`, replace every ARN with a placeholder …, and grep the file for `arn:aws` until the result is empty." | +1 |
| `:248-250` | "Load it in `ConnectRouting` through `Fn.sub` exactly as the email flow is loaded, as a `CfnContactFlow`, and publish `InboundVoiceFlowId`." | +1 |
| `:250-251` | "Add a test that the voice flow's content contains no literal ARN and that the flow is of type `CONTACT_FLOW`." | +1 |
| `:253-256` | "Write the association `AwsCustomResource`. Have them read the request syntax … Decide which form of each identifier to pass …" | +2 |
| `:256-258` | "… ask them to explain what goes wrong without `onUpdate` when the flow is replaced, and without `onDelete` when the routing stack is destroyed." | +2 |
| `:260-262` | "Now let them ring the number before they touch the routing profile. … They should hear the greeting, and then wait." | 0 |
| `:262-265` | "Have them find the evidence before the fix. The flow log shows the transfer to queue succeeded. The contact search … shows a voice contact waiting. The routing profile … lists `EMAIL` only." | +1 (applies lesson 05's method) |
| `:265-268` | "Then add both halves: a `VOICE` media concurrency of 1 (have them try 2 in a synth or a test first and read what the CloudFormation reference says about the range), and a `VOICE` queue configuration for the course queue." | +2 |
| `:268` | "Add a test for each half." | +1 |
| `:268` | "Have them say why one half without the other still fails." | +2 |
| `:270-271` | "Deploy `ConnectRouting`, set the agent Available, and call again. The workspace offers the call, the agent accepts it …" | 0 |
| `:271-272` | "Note the delay. That is the latency from `#instance-choices`, and they should name it." | +1 |
| `:272-274` | "Hang up, close the contact, and look at the contact record …" | 0 |
| `:274` | "Then ask the tutor to run the checks." | 0 |
| `:276-278` | "If time allows, show the out-of-hours branch on demand …" | +1 (optional repetition) |
| `:282-286` | "`cdk-synth` passes, and `pytest` passes with tests that assert: …" | 0 |
| `:287-288` | "`ConnectCore` publishes `PhoneNumber` and `PhoneNumberId`. …" | 0 |
| `:289-293` | "The learner has called the number. … The `call-routed` validator passes. …" | 0 |
| `:294-297` | "The learner can explain, without notes: why the number is in `ConnectCore` and what a replacement would do to it; …" | +2 |
| `:298-299` | "The learner knows where the teardown is … and that the number bills daily until it is released." | 0 |

Sum: 2+2+0+2+1+0+0+2+1+1+2+1+1+1+2+2+0+1+2+1+2+0+1+0+0+1+0+0+0+2+0 = **30**.

Not scored (contingent): `:205-212` — the `cdk diff ConnectRouting` replacement
demonstration fires only "If they say `ConnectRouting`". It is the lesson's best-designed
instructive failure, and a learner who answers correctly at `:204` skips it entirely; the
lesson does not say whether they should still see it (section 6.4, note). `:242-244` (an
optional console association "If they want to see it").

### `lessons/07-voice-menu-and-caller-lookup.md` — 22

| file:line | Sentence (or the act it names) | Score |
|---|---|---:|
| `:184-185` | "Ask them for their own number in E.164 and have them write it down, without spaces and with the country code." | +2 |
| `:185-187` | "Then ask what string they think Connect will put in `CustomerEndpoint.Address` when they call the US number from their phone. Do not answer it." | +2 |
| `:189-193` | "Draw the lookup first, before the menu. … add the AWS Lambda function block: the lookup function, synchronous, response validation `STRING_MAP`, a timeout below 8 seconds. Then add a Set contact attributes block that copies `customer_id`, `tier` and `display_name` onto the contact." | +1 (repeats lesson 04 for voice) |
| `:193-194` | "Wire the Lambda's Error and Timeout branches to Set working queue on the course queue with `route_reason` set to a lookup-failure value." | +1 |
| `:194-195` | "Export, replace the ARNs, deploy, and call **before** adding the learner's own record." | 0 |
| `:196-198` | "Have them open the Lambda's log for that invocation, find `Details.ContactData.CustomerEndpoint.Address` and `Channel`, and compare the number with what they wrote down." | +2 |
| `:200` | "Now add their record: `tools/load_customers.py --add-endpoint <their E.164> --tier gold --name "<their name>"`." | 0 |
| `:201-203` | "Before calling again, have them read what the loader stored … and what the function will compute from the logged address. Are the two strings the same?" | +2 |
| `:210-213` | "After the copy, add Check contact attributes on `tier`. For `gold` …, a Play prompt with text-to-speech greets them with `$.Attributes.display_name`, sets `route_reason` …, Set working queue to the priority queue, then the hours check and Transfer to queue." | +2 |
| `:217-219` | "Get customer input with a text-to-speech prompt that names the keys, DTMF conditions for the keys they chose, and a Set timeout of a few seconds. Each condition sets its own `route_reason` and working queue." | +2 |
| `:219-222` | "… have them wire Timeout straight back into the same Get customer input block, deploy, call as an unknown caller …, and press nothing for about half a minute." | 0 (the planned failure; the teaching is the next row) |
| `:222-223` | "Ask what a caller who had put the phone down would cost, and who would help them." | +2 |
| `:223-225` | "Then build the bounded retry with the Loop block (two plays is plenty), and after it route to the course queue with a `no-input` reason. Wire Default … into the same retry, and Error to the course queue." | +2 |
| `:226-227` | "Export, deploy, and test each path: key 1, key 2, a wrong key, and silence. After each test call, look at the contact record's attributes and confirm the `route_reason` matches the path." | +1 |
| `:229-231` | "Check the routing profile has a `VOICE` queue configuration for the priority queue." | +1 |
| `:233-235` | "Finally, put the learner's gold record back … and make the call the validators read … Then ask the tutor to run the checks." | 0 |
| `:239-244` | "`cdk-synth` passes, and `pytest` passes with tests that assert: …" | 0 |
| `:245-250` | "A call from the learner's own number … is recognised by the same Lambda … The `lambda-enriches` and `call-routed` validators pass." | 0 |
| `:251-253` | "The learner has shown, by test calls, that a menu choice changes the queue, and that a caller who presses nothing reaches the agent …" | 0 |
| `:254-257` | "The learner can explain, without notes: why the Timeout branch must not loop unbounded or drop the caller; why there is one Lambda and where normalisation lives; what string Connect sent as their caller ID …" | +2 |

Sum: 2+2+1+1+0+2+0+2+2+2+0+2+2+1+1+0+0+0+0+2 = **22**.

Not scored (contingent): `:203-207` (the normalisation fix, "If they are not [the same]"),
`:213-215` (greeting the no-match branch by name).

### `lessons/08-one-agent-two-channels.md` — 14

| file:line | Sentence (or the act it names) | Score |
|---|---|---:|
| `:164-166` | "Have the learner show the routing profile as it is deployed, `aws connect describe-routing-profile` and its queue list, and say for each channel what its concurrency and cross-channel behaviour are now." | 0 |
| `:166-170` | "Then ask the two questions … "You are on a call and an email arrives. Are you offered it?" … Let them answer from what they read." | +2 |
| `:172-175` | "Have them choose an email concurrency, a `BehaviorType` for `VOICE` and one for `EMAIL`, and a priority and delay for each queue and channel pair. Ask them to defend each choice in one sentence." | +2 |
| `:179-180` | "Write it in CDK: an explicit `CrossChannelBehavior` on each `MediaConcurrency`, and one `QueueConfig` per queue and channel pair." | +2 |
| `:180-182` | "Add tests in `tests/` that assert on the routing template: …" | +1 |
| `:182-183` | "Deploy `ConnectRouting` and check with `describe-routing-profile` that the account now holds what the code says." | 0 |
| `:185-189` | "Now design the test, and make sure it is not a one-contact test. … The test needs **one call and two emails waiting together** before the agent is Available:" | +1 (the lesson then prescribes the design) |
| `:191-195` | Steps 1–3: agent not Available; "Create the two emails …"; "Call the number … and stay on the line in queue." | 0 |
| `:197-201` | "Before step 4, the **prediction**. The learner says, in order, what the agent will be offered … For each step they name the property of the routing profile that decides it …" | +2 |
| `:203-205` | Step 4: "Set the agent Available. Accept, work and close each offered contact in turn, and note the order …" | 0 |
| `:207-208` | "Compare the observation with the prediction. If they match, ask the learner to explain *why* from the profile, step by step." | +2 |
| `:220-225` | "End the lesson, and the course, by pointing at teardown. … the learner removes their own records from the table with `tools/load_customers.py --remove-endpoint <endpoint>` …" | 0 |
| `:229-232` | "`cdk-synth` passes, and `pytest` passes with tests that assert …" | 0 |
| `:233-234` | "The deployed routing profile matches the code. …" | 0 |
| `:235-241` | "`concurrency-observed`, a manual condition: …" | 0 (re-checks `:197-208`) |
| `:242-243` | "The learner defends their concurrency numbers and behaviours in a sentence each, for this contact centre, and can say what they would change for a team of agents." | +2 |
| `:244-245` | "The learner knows the teardown order …" | 0 |

Sum: 0+2+2+2+1+0+1+0+2+0+2+0+0+0+0+2+0 = **14**.

Not scored (contingent): `:175-177` (looking for a priority on the queue construct),
`:208-213` (a prediction that differed), `:215-218` (a second run "If the first run was
simple"). The second-run design at `:215-218` — change one property, predict again, test
again — is the strongest evidence the lesson can produce, by its own account ("Two
predictions that differ by one property, both correct, make the strongest evidence"). Scored
it would add about +4. It is contingent on the first run being "simple", which an
all-defaults learner will very likely meet; the author may want to make it unconditional
(proposal 9).

---

## 3. Goal gaps

Every per-lesson learning objective (59 across 9 lessons), every `COURSE.md` coverage topic
(6) and every `DESIGN.md` anchor (5) was checked against **what the lessons make the learner
do**, never against `design_refs` citations and never against `topic_candidates` word
overlap.

**One gap, −3.**

- **`COURSE.md:108-109` — "ai agents and q in connect — what generative self-service and
  agent assist would add to a flow like yours. Explained, not built." — −3.**
  How I decided: "Explained, not built" means a lesson should at least *teach* it, and a
  learner element should exercise the explanation. I searched every lesson for Q in Connect,
  generative AI, self-service and agent assist. The only mentions are
  `lessons/03-flow-logic-for-email.md:114-115` ("templates need an Amazon Q in Connect
  knowledge base, which this course does not build") — a reason for a constraint, not an
  explanation of what Q would add — and `:302-303`, an `## Optional deeper paths` bullet on
  message templates. Neither generative self-service nor agent assist appears in any lesson,
  any `## Concepts to teach`, or any completion condition. The author may argue this back on
  the reading that the coverage list is a *question-scope boundary* ("The tutor treats a
  question on any of these as in scope", `COURSE.md:92-93`) rather than a promise to teach;
  I rejected that because the same section opens "Topics this course owes you"
  (`COURSE.md:92`), and owing a topic nobody teaches is the gap this row exists to price.

**Checked and ruled served — the close calls, with reasoning:**

- **`cost and teardown` (`COURSE.md:95-98`) — served, thinly.** Daily number rental, inbound
  per-minute charges and the international call are taught (`06:85-98`) and checked
  (`06:298-299`); teardown is exercised (`08:220-225`). **"what bills per email" appears in no
  lesson** — no lesson names the email channel's pricing. Compound topic, most halves served,
  so not a −3; proposal 6 closes the thin half.
- **`personal data in contacts` (`COURSE.md:106-107`) — served, thinly.** Encryption and
  retention are learner decisions at `01:218-220` ("Decide … the encryption … and what happens
  to the bucket's contents at teardown"), and personal data is handled deliberately at
  `04:227-231`, `05:117-119`, `07:105-107`. **"encryption with KMS"** is only an optional
  deeper path (`04:304-305`) and **"what never to put into an attribute"** appears nowhere.
  Not a −3; proposal 6.
- **`security profiles and least privilege` (`COURSE.md:104-105`) — served.** The "why it is
  not what decides which contacts they get" half is the centre of lesson 00 (`:273-277`,
  `:312-315`); the "what it should and should not grant" half is served by the Agent-only
  constraint and the two-login design (`00:236-237`, `00:173-183`), with the full permission
  review left as an optional path (`00:344-346`).
- **`ses sandbox` (`COURSE.md:102-103`) — served** by `01:263-266`.
- **`phone number regulation` (`COURSE.md:99-101`) — served** by `06:214-217`.
- **`#deliberately-unresolved` (`DESIGN.md:136-146`) — served**, by two of its three items:
  rule precedence (`04:198-199`, a learner decision with no step — proposal 4) and agent
  concurrency (`08:172-175`). The third item, the custom email domain, is "explained and never
  built" and appears only as an optional path (`01:332-333`); the anchor describes a
  deliberate omission, so the omission honours it.
- The other four anchors — `#instance-choices`, `#stack-split`, `#flow-round-trip`,
  `#lambda-contract` — are each served by lessons doing what they describe
  (`00:245-258`, `06:214-217`; `00:286-288`, `01:247-249`, `06:204`; `01:230-238`, `01:271-276`;
  `04:205-212`, `07:189-208`).
- **All 59 per-lesson objectives are served**; the breakdowns in section 2 carry the element
  for each. The closest call: `03:47-48` ("Recognise three instructive failures …") — two of
  the three failures are contingent and unscored, but the explanation condition `03:269-271`
  names all three, so the learner is made to produce each.

**Gaps listed: 1. Subtracted: −3. This agrees with section 1.**

---

## 4. The toil inventory

**Confirmed toil sites: none.**

The scanner reported 3 candidates. **The scanner is a candidate generator over a fixed verb
list, and its silence or its noise is evidence about the verb list, not about the course.**
This inventory comes from opening all nine lessons and reading every progression act,
completion condition, constraint and theory instruction — 227 scored rows (that the row
count equals the course's sum is a coincidence; both were re-counted by script) — against the
rubric's toil test, and from reading the three supplied lesson files and the twelve
manifest supplies.

The structural fact that shapes it: **this bundle already supplies everything it could
reasonably ship.** The CDK app skeleton (`app.py`, both empty stacks, `cdk.json`,
requirements, `tests/conftest.py`, `README.md`, `.gitignore`), the two check scripts, the seed
data and its loader (lesson 04) and the scenario generator (lesson 05) are all `supplies:`
entries, and both lesson-scope `describe` lines say why ("writing seed data teaches nothing";
"Writing an API client to fake inbound email teaches nothing about tracing"). The project
skeleton tiebreak of 2026-09-13 therefore never fires: there is no skeleton step to rule on.

**Candidates I examined and rejected, so the next reader does not re-litigate them:**

- `lessons/00-instance-and-first-agent.md:242-245` (`install` fired) — "Start with your own
  setup, which the bundle cannot do for you. Install the CDK CLI (it is an npm package and
  needs the Node.js you already have), create a virtualenv in the workspace, activate it, and
  install the development requirements with `pip install -r requirements-dev.txt`."
  **Rejected: could not have been supplied** — the CDK CLI, a virtualenv and installed
  packages need the network and the toolchain. The same paragraph's `cdk bootstrap` (`:252`)
  needs the learner's account. The lesson even says so in its first clause. Scored 0.
- `lessons/04-lambda-enrichment/LESSON.md:56` (`copy` fired) — "Copy returned values onto the
  contact with **Set contact attributes** so they survive into the contact record, and branch
  on `tier`." **Rejected: not a file copy.** It is a learning objective about a flow block;
  the copy is the concept being taught (`04:110-123`).
- `lessons/07-voice-menu-and-caller-lookup.md:47` (`copy` fired) — "Copy the Lambda's result
  onto the contact as attributes, greet a known caller by `display_name` …". **Rejected** for
  the same reason.

Also examined by hand, not flagged by the scanner:

- `lessons/01-first-email-contact.md:206-209` — the console step (Create service role, Add
  domain). **Rejected: could not have been supplied** — it is console-only in the learner's
  account, and the lesson says there is no documented CloudFormation or API form (`:67-74`).
- `lessons/00-instance-and-first-agent.md:279-282` — looking up the default ARNs.
  **Rejected:** account-specific values, unshippable; and the smell is the teaching (`:151-160`).
- `lessons/03-flow-logic-for-email.md:212-214` — re-writing the ARN guard test that lesson 01
  `:234-235` already required. Deterministic, and the bundle could ship a generic test, but
  this course makes the learner write every test (`03:184-186`, constraints throughout).
  **Not toil: a duplicated instruction.** Scored 0 as a re-run; proposal 5 reconciles it.
- `lessons/04-lambda-enrichment/LESSON.md:227` and `lessons/05-following-a-contact/LESSON.md:171`
  — running the supplied loader and scenario script. The course already removed the toil here;
  running the tool scores 0.

**No element in this course is charged −2.**

---

## 5. Proposals

Each names a concrete action. All are refusable.

**Proposal 1 — make lesson 08's test setup match the supplied script. (Highest-value finding.)**
`lessons/08-one-agent-two-channels.md:28-29` and step 2 at `:192-193` say to "Create the two
emails (with `tools/scenarios.py`, or by sending them by hand)". The supplied script creates
**three** contacts, always: A, B and C (`lessons/05-following-a-contact/scenarios.py:29-51`,
loop at `:99`), and by design two of them land in the **priority** queue (A by `tier-gold`,
B by `subject-urgent`) and one in the course queue (`ANSWERS.md:12-14`). A learner who takes
the first option has one call and **three** emails waiting across two queues, which is not the
setup the prediction (`:197-201`) or the manual condition `concurrency-observed`
(`:235-236`, "one call and two emails waiting at the same time") is written for. Either:
- (a) change `:28-29` and `:192` to "send two emails by hand from your mailbox" and drop the
  script option; or
- (b) keep the script and say so honestly: "`tools/scenarios.py` creates three email contacts,
  two of them routed to the priority queue; predict for all four contacts", and widen
  `:235-236` to match; or
- (c) give `scenarios.py` an option (for example `--only A,C`) — that is a supplied-file change
  through `tutorail-authoring`, and it must keep lesson 05's default behaviour.

(a) is the smallest and keeps the test as designed.

**Proposal 2 — let the learner observe the single-grant failure lesson 04 asks them to predict
and record.** `lessons/04-lambda-enrichment/LESSON.md:224-226` adds the integration
association "first, alone", asks the learner to predict "what happens when a contact reaches
the block with only that", and then immediately adds the permission — in step 4, two steps
before the flow calls the function (step 6, `:232`). Nothing reaches the block while only one
grant exists. Yet `:138-139` says "find out on your own instance which grant fails how, and
record it", and `## On completion, persist` requires "What the learner observed when only one
of the two grants existed" (`:288`). Move the permission after the wiring: step 4 adds the
association only; step 6 wires the flow, deploys, sends one email and reads the Error path;
then a new step adds the permission. That turns `:224-225` from an unverifiable guess into the
lesson's best planned failure.

**Proposal 3 — reconcile the `display_name` experiment with the supplied loader.**
`lessons/04-lambda-enrichment/LESSON.md:99-101` tells the learner to "return a display name
with a space, and read what the contact record and the flow log show. Record the result", and
`:287` persists it. The supplied `tools/load_customers.py` refuses a name with a space
(`lessons/04-lambda-enrichment/load_customers.py:104-107`, regex `^[A-Za-z0-9_-]+$`), every
seed `display_name` is hyphenated (`customers.json`), and `DESIGN.md:120-122` already rules
"`display_name` carries no spaces until a live walk-through confirms otherwise". No step says
how to produce a spaced name. Either drop `:99-101` and `:287` (the design decision is already
made), or add one sentence saying how to run the experiment without the loader (for example,
the failure-switch handler from step 8 returning a fixed spaced name once), and make it a step.

**Proposal 4 — give the precedence decision a step.** `lessons/04-lambda-enrichment/LESSON.md:198-199`
(Constraints): "The learner decides, and records, which wins when a gold customer sends an
urgent subject." `DESIGN.md:140-143` and lesson 05 (`:226-228`) both depend on it, and the
persist list asks for it (`:285-286`). No progression step contains it. Add to step 6
(`:232-237`), before the Check contact attributes on `tier` is drawn: "**Decide** first, and
say it to the tutor: when an urgent subject comes from a gold customer, which `route_reason`
wins, and where in the flow does that put the tier check relative to the subject check?" That
also fixes the closing-action row for this lesson (section 6.4).

**Proposal 5 — stop asking lesson 03 to write a test lesson 01 already required.**
`lessons/01-first-email-contact.md:234-235` ("Write a test that reads
`flows/inbound-email.json` and fails if it contains an ARN") and its completion condition
`:288` already create the guard. `lessons/03-flow-logic-for-email.md:212-214` asks for it again
("**Write the guard test.** …") and the constraint `:199-200` says "the test is written before
the export it guards". Change step 2 to "**Run the guard test** from lesson
`01-first-email-contact` … then add a second assertion: every `${Name}` …", and change `:199-200`
to "A pytest test in `tests/` asserts this (written in lesson `01-first-email-contact`)". Also
consider tightening lesson 01's test from `arn:` to the same `arn:aws:` string lesson 03 uses,
so one test serves both.

**Proposal 6 — close the gap and the two thin coverage halves.**
- *ai agents and q in connect* (−3): either (a) add one item to an existing explanation
  condition — `lessons/08-one-agent-two-channels.md:242-243` is the natural home, as the course
  closes: "… and can say what generative self-service or agent assist in Amazon Q in Connect
  would add to this contact centre, and why the course does not build it" — with two sentences
  of Theory to support it; or (b) move the topic out of the coverage list into the
  "Deliberately **not** taught" paragraph (`COURSE.md:111-115`) next to "Lex bot authoring".
  Either recovers the −3.
- *what bills per email*: one Theory sentence in lesson 01 (beside `:60-65`) naming that email
  contacts are billed per message, and one clause in `06:294-297` or `08:244-245`.
- *what never to put into an attribute*: one constraint in lesson 03 or 04, for example
  "`route_reason` and the copied lookup values are routing data; never copy an email body, a
  subject or anything a customer typed into a user-defined attribute", with its reason.

**Proposal 7 — remove learner-facing references to the course spec.**
`lessons/03-flow-logic-for-email.md:295` ("The SPEC allows the rule to match the subject *or*
the sender") and `lessons/04-lambda-enrichment/LESSON.md:138` ("The SPEC expects a missing grant
to show up as a failed block at run time …") cite `SPEC.md`, which no lesson or `COURSE.md`
introduces to the learner (section 6.3). Restate each in the lesson's own words, for example
"The rule may match the subject or the sender" and "Expect a missing grant to show up …".

**Proposal 8 — run the supplied scripts the way their own docstrings do.**
`lessons/07-voice-menu-and-caller-lookup.md:105` and `:200`, and
`lessons/08-one-agent-two-channels.md:223`, write `tools/load_customers.py --add-endpoint …`
with no interpreter. The bundle file has mode `644`
(`lessons/04-lambda-enrichment/load_customers.py`), and its own docstring writes
`python3 tools/load_customers.py` (`:4-13`). Write `python3 tools/load_customers.py …` in all
three places, as lesson 04 effectively does.

**Proposal 9 — make lesson 08's second prediction unconditional, or say when it is skipped.**
`lessons/08-one-agent-two-channels.md:215-218` runs a second, one-property-different prediction
"If the first run was simple". The lesson calls it the strongest evidence it can produce. Either
make it a numbered part of the test for every learner, or state the condition for skipping it
("if your first prediction already exercised priority or cross-channel behaviour"). Without it,
lesson 08 is the course's lowest-scoring lesson at 14 while carrying its capstone objective.

**Proposal 10 — say what lesson 06 does when the learner places the number correctly.**
`lessons/06-a-phone-line.md:204-212`: the `cdk diff` replacement demonstration happens only "If
they say `ConnectRouting`". A learner who answers "`ConnectCore`" never sees what a replacement
does to a number, which objective `:37-38` asks them to explain. Add one sentence: "If they
answer `ConnectCore`, still have them run the `Prefix` change and `cdk diff` against
`ConnectCore`, read the replacement line, and revert — **do not deploy it**."

**Proposal 11 — align the setup check's description with the script.** `tutorial.yaml:57`
says `toolchain-present` "Checks that Python, Node, the CDK CLI and AWS credentials … are
available"; `supplies/checks-toolchain.py:5-7` and `:57-58` report the CDK CLI as "not yet"
rather than failing, which `lessons/00-instance-and-first-agent.md:26-28` describes correctly.
Change the `describe` to "Checks that Python, Node.js and AWS credentials and a region for one
account are available; the CDK CLI and Python packages are installed in lesson 00".

**Proposal 12 — declare the validators lesson 05's completion conditions use.**
`lessons/05-following-a-contact/LESSON.md:206-208` requires "The guard test and the rest of the
test suite pass" after a `ConnectCore` deploy and a flow re-export, but its frontmatter declares
only `validators: [contact-explained]` (`:5`). Add `cdk-synth` and `pytest`, as every other
code-changing lesson does.

---

## 6. The questions only a reader can answer

### 6.1 A `design_refs` entry that does not answer the question its lesson raises

All 16 `design_refs` resolve (validator check 1). Read against what each lesson raises:

- **`lessons/05-following-a-contact/LESSON.md:4` → `#lambda-contract` — partial.** The question
  lesson 05 raises of the Lambda is *why does it log the contact id?* (`:31-35`, `:86-89`).
  `#lambda-contract` (`DESIGN.md:104-134`) says nothing about logging; the requirement lives
  only in lesson 04's constraint `:187-189`. Lesson 05's own subject — tracing a contact,
  flow-log design — has no anchor at all; lesson 05's persist block (`:234-238`) has the tutor
  append one. Proposal-sized: add a bullet "**The function logs the contact id** on every
  invocation, with what it looked up and found, never the whole event" to `#lambda-contract`.
- **`lessons/08-one-agent-two-channels.md:4` → `#stack-split` — near-vacuous.** It answers only
  "Nothing in this lesson touches `ConnectCore`" (`:156-157`). Not wrong.
- **`lessons/02-hours-queues-routing-profiles.md:4` and `lessons/03-flow-logic-for-email.md:4`
  → `#flow-round-trip` only.** The references answer the placeholder questions those lessons
  raise. Their central questions — what hours do on their own, the `route_reason` vocabulary
  that `03:279-281` calls "the course-wide record" — have no anchor. Not a defect in the
  references; noted because a tutor loading only the cited anchor learns nothing about either.

No reference points at an anchor that contradicts its lesson.

### 6.2 A lesson that introduces a type or concept nothing later uses

**None found.** Checked and cleared: `Ref` versus `GetAtt` (`00:185-189`) → used in `01:99-105`,
`02:108-115`, `06:250`; agent workspace versus CCP (`00:166-168`) → `05:121-126`, `06:152-156`;
`route_reason` (`02:130-136`) → every later lesson; the failure switch (`04:246-253`) → used in
its own completion condition, and terminal by design; `Change routing priority / age`
(`08:110-113`) → introduced as a contrast, which is its use; SES spam and virus verdicts
(`03:64-65`) → only an optional path (`03:292-294`), a one-clause mention rather than a
concept the course asks anything of. CORS (`01:83-85`) is used only in lesson 01, which is the
lesson that needs it.

### 6.3 A symbol or term a lesson uses and no lesson introduces

The evidence script's short-symbol candidates, sorted by hand on the 2026-09-13 boundary
(parameter of the concept being taught versus an identifier the learner brought):

- `US` (`06:180`) — introduced at `06:75-85` in the same lesson. Not a finding.
- `d-` (`00:86`) — a literal prefix in an AWS naming rule, stated in the sentence that uses it.
  Not a symbol under the row.
- `S3` (`01:79`) — an AWS service the course assumes (`tutorial.yaml:96-101`). Not a symbol.

By hand, beyond the script:

- **Bound nowhere (for the learner): "the SPEC"** — first use
  `lessons/03-flow-logic-for-email.md:295` ("The SPEC allows the rule …"), again at
  `lessons/04-lambda-enrichment/LESSON.md:138`. `SPEC.md` ships inside the bundle by this
  repository's decision, but no lesson and no part of `COURSE.md` tells the learner it exists
  or what it is. Proposal 7.
- **Bound only in `DESIGN.md`: none found.** Checked: `E.164` (first lesson use `04:147`,
  defined inline there); `DID` (first use `06:39`, defined at `06:75-76` in the same lesson's
  Theory); `ACW` (`08:65`, defined in the same sentence); "long-lived stack" / "churning stack"
  (first use `00:16-17`, defined there); `<learner-prefix>` (`00:43`, defined `00:84-85`);
  `$.External` (`04:112`); CCP (`00:166`). Each is introduced in a lesson at or before first use.

The sort above is the reader's. No script draws the parameter/identifier line.

### 6.4 Does each lesson equip the tutor to end a turn with one concrete action?

Graded on the files. Answered for every lesson in the section 2 table; repeated here.

- **00 — pass.** First action named concretely (`:242-244`, install the CDK CLI, create a
  virtualenv, `pip install -r requirements-dev.txt`). Decisions are marked as decisions and
  settled before the act they govern ("Choose your alias before you write it down", `:256`;
  "Decide `InboundCalls` and `OutboundCalls`", `:260-261`; "Decide how the password reaches the
  user", `:283-284`). The paragraph at `:242-254` carries seven acts, each in its own sentence
  and in order, so the tutor can take them one at a time without having to split a sentence.
- **01 — pass.** First action: the Email page console step (`:206-209`). Decisions are marked and
  routed to the tutor (`:214-216`, `:258-261`). Note for the author: the option at `:259-260` to
  "bring the course's own routing profile forward" anticipates lesson 02's work with no guidance
  on how much of it; the decision is marked, so this is a pass, but it is the most open decision
  in the course.
- **02 — pass.** First action: "Write `CfnHoursOfOperation` …" (`:179`). "Decide first, and say it
  to the tutor" (`:208`) is the model of condition 2.
- **03 — pass.** Step 1 is a marked decision ("Decide the rule", `:207`), settled before step 2's
  concrete action.
- **04 — fail.** Condition 2. The decision "which wins when a gold customer sends an urgent
  subject" sits only in `## Constraints`, `:198-199` — "The learner decides, and records, which
  wins when a gold customer sends an urgent subject." — with no home in the progression. A tutor
  following the steps reaches the end of step 8 with that decision still open, and the
  closing action becomes an open design question. Also, step 4's prediction (`:224-225`) has no
  observation to close on (proposal 2). Proposal 4 repairs the row.
- **05 — pass.** First action: open the function's most recent log stream and find a contact id
  (`:31-35`, `:169-170`).
- **06 — pass, with a note.** The lesson opens on a question (`:204`, where the number goes), a
  marked decision; the first concrete artifact action is named (`:222`, "Write the
  `CfnPhoneNumber` and the two outputs"). The opening branch has only one arm written: a learner
  who answers correctly gets no instruction about the `cdk diff` demonstration (proposal 10).
- **07 — pass.** First action: write down your own number in E.164 (`:184-185`).
- **08 — pass.** First action: `aws connect describe-routing-profile` (`:164-166`). Decisions
  (`:172-175`) are made and defended before the CDK is written.

### 6.5 A lesson far outside the course's usual size

**No size outlier.** Lessons run 256–352 lines (`05`: 256, `08`: 276, `02`: 284, `07`: 291,
`03`: 303, `04`: 307, `06`: 331, `01`: 333, `00`: 352) and share one section structure. Scored
rows per lesson: 29, 31, 34, 22, 28, 15, 31, 20, 17.

**Score outliers, and why.** 03 (17), 05 (17) and 08 (14) sit at about half of 01 and 02 (35).
Three causes, none of them a size defect:
- **house style** — 03, 04 and 05 use numbered steps that pack several acts into one step, so
  they enumerate more coarsely than the paragraph lessons; 04 still reaches 30 because its
  steps are dense with decisions;
- **contingent failures not scored** — 03 carries two, 08 three; scored, 03 would read about 21
  and 08 about 18–22;
- **05 is evidence-heavy by design** — a tracing lesson whose core is one explanation, built once
  per contact; its four +2 rows at `:187-193` are the lesson.

Lesson 08 is the course's capstone and its lowest score; proposal 9 is where to look.

### 6.6 A must-cover topic that only an optional lesson teaches

**Not applicable — the course has no optional lessons.** No coverage topic is taught only by an
`## Optional deeper paths` bullet either, except the gap already priced in section 3 (Q in
Connect, `03:302-303`).

### 6.7 The completability invariant

> **Can a learner who declines every offer still finish this course?**

**Not applicable — no optional lessons declared.** Checked against the lessons, not only the
manifest: `tutorial.yaml` has no `optional_lessons:` key; no lesson declares `optional: true`
(validator check 20, and read directly); no lesson in `lessons:` calls itself optional in its
prose. The nine `## Optional deeper paths` sections are discussion prompts, not lessons, and no
main-path completion condition depends on one. Prose and manifest agree, so the total in
section 1 needs no restatement.

### 6.8 Dynamic evidence

No dry-run harness was run against this bundle for this audit, and none of the lesson
contents has been walked against a live Amazon Connect instance by me. Several lesson claims
are explicitly marked by the author as unverified (`ANSWERS.md:49-58`; `01:249-250`;
`04:98-101`; `05:82-84`; `07:109-114`). Nothing here rests on dynamic evidence.

---

## Note on the audit brief

- The brief's facts checked against the bundle: 9 lessons, approved spec in `SPEC.md` inside the
  bundle, Amazon Connect with CDK in Python — all correct.
- `audit.py` loaded the bundle without error. Its three toil candidates are all rejected
  (section 4); its three short-symbol candidates are all cleared (section 6.3).
