# LoopAI Application

## How to install (developer bundle)

Requirements: `git`, `curl`, Docker with the `docker compose` v2 plugin, and SSH access to the
`dantweb/loopai-*` GitHub repositories (or use `--force-http`).

```bash
git clone git@github.com:dantweb/loopai-sdk.git && cd loopai-sdk
./bin/install.sh --web-branch production --view-branch production --core-branch production
```

`./bin/install.sh` (also `make install`) does the whole setup and is safe to re-run:

1. clones `loopai-core`, `loopai-web`, `loopai-view` into `loopai_src/{core,web,view}` - existing
   checkouts are fast-forwarded to the requested branch (checkouts with uncommitted changes are left alone);
2. creates `.env`, `loopai_src/.env`, `loopai_src/view/vue/admin/.env` from the `.env.dist` files if
   missing (existing files are never overwritten, only missing keys are appended);
3. creates the external `shared_network`, builds and starts `db`, `redis`, `loopai_web`, `frontend`;
4. creates the databases, runs the web (alembic) and core migrations, populates agent roles/statuses,
   creates an admin user (`admin` / `Loopai_2025!` by default);
5. smoke-tests core, CLI, web (http://localhost:5050) and the admin frontend (http://localhost:8080).

### Parameters
```
--web-branch <branch>    Branch for the web repository   (default: production)
--view-branch <branch>   Branch for the view repository  (default: production)
--core-branch <branch>   Branch for the core repository  (default: production)
--all-same <branch>      Use the same branch for all repositories
--force-http             Clone over HTTPS instead of SSH
--fresh                  Wipe and re-clone existing checkouts (web/users is kept)
--no-docker              Only clone repositories and prepare .env files
--no-frontend            Do not build/start the Vue admin container
--admin-login <login>    Admin user to create (default: admin)
--admin-password <pass>  Admin password (default: Loopai_2025!)
```

Host ports are set in `./.env` (`LOOPAI_WEB_PORT=5050`, `LOOPAI_FRONTEND_PORT=8080`, `LOOPAI_DB_PORT=5432`,
`LOOPAI_REDIS_PORT=6379`, `LOOPAI_DEBUG_PORT=5678`). If db/redis/frontend/debug ports are busy the installer
picks free ones and saves them. The frontend API URL (`VUE_APP_API_BASE_URL`) is baked in at build time -
change it in `./.env` and run `make upp` if you change `LOOPAI_WEB_PORT`.

Python dependencies are installed in the `loopai_web` image; no virtualenv is needed inside the container.
Add API keys (`OPENAI_API_KEY`, ...) to `./.env` / `loopai_src/.env`.

### Day-to-day
```bash
make upp              # rebuild and start containers
make bash             # shell in loopai_web
make migrate          # web + core migrations
make run_core_tests   # core unit tests
make run_web_tests    # web unit tests
```

### hints
to run wp use post url string

## How to deploy

```
./bin/server_deploy.sh
```

## Run

```bash
  flask --app web/web_interface run
```

 in the backend container:

```bash
  cd view/vue/admin
  npm install
  npm run serve
```

### How to run loop from the command line for single user installation 

```bash
docker compose exec -e WEB_OR_CLI=cli loopai_web python3 app.py --loop <abs.path>/loop_config.yaml --user <userId> --loopId <loopId> [--projectId <projectId>]
```

<abs.path> - from the very root of the container (`/app/...`); `-e WEB_OR_CLI=cli` (or `WEB_OR_CLI=cli` in loopai_src/.env) is required
<userId> - user id from the database
<loopId> - loop id from the database
<projectId> - optional, loads the project's env

Notes for a minimal loop:
- `session.code_source` must point to a `.py` file that defines `PROMPT_TEMPLATES = {}` and `SYSTEM_CONTENT_TEMPLATES = {}`;
- every step needs `input: []` / `output: []` lists (may be empty);
- relative paths (e.g. `bash_script_path: script.sh`) resolve to `var/filesystem/<userId>/loops/<loopId>/filesystem/`.

Here is an example how to run a web-based loop from the command line or cronjob from inside the container. 
In the following example the execution of the loop and all the dependence and files is exactly same as if one runs this loop from the web:
```bash
 python3 web/command/cron_runner.py --loopId 17 --user 1
 
 ```

### How to run loop from the command line for multi-user installation
the production script runs the following command:
```bash
 docker compose exec -T -e RUNNING_CRON=True web python3 web/command/cron_runner.py --loopId 17 --user 1
```

## PostgreSQL DB repare tools

### How to make a backup of the database
```bash
python database_backup.py --env_file=.env
```

### How recreate table 'loops' from the filesystem
```bash
python web/command/populate_loops_script.py --user_id=<USER_ID> --project_id=<PROJECT_ID> --base_directory=<BASE_DIRECTORY>
```
example:
```bash
python web/command/populate_loops_script.py --user_id=1 --project_id=1 --base_directory=/app/var/users/1/loops
```


## Overview

This document provides an overview of potential applications leveraging the concept of loops defined in the `loops/*.yaml` folder. These applications demonstrate the versatility and potential of using loops in various domains, automating complex processes, enhancing efficiency, and providing valuable insights.

## Potential Applications

### 1. Automated Content Creation and Publishing

**Description**: A system that automatically generates, optimizes, and publishes content to a WordPress or other CMS platform based on predefined criteria and user inputs.

**Functionality**:
- Generate content ideas based on SEO trends and user preferences.
- Create drafts using GPT models, ensuring adherence to the content style guide.
- Optimize content for SEO using automated tools.
- Schedule and publish posts automatically.
- Monitor performance and adjust strategies based on traffic analysis.

### 2. Dynamic Personalization Engine

**Description**: An engine that personalizes website content in real-time based on user behavior and preferences.

**Functionality**:
- Track user interactions on the website.
- Analyze behavior patterns to understand user preferences.
- Dynamically update content and recommendations.
- Use machine learning models to predict future behavior and personalize content accordingly.

### 3. Intelligent Workflow Automation

**Description**: An automated workflow system that integrates various tools and services to streamline business processes.

**Functionality**:
- Automate repetitive tasks such as data entry, email responses, and report generation.
- Integrate with CRM, email, and other business tools.
- Use loops to define complex workflows and conditional logic.
- Provide analytics and insights on workflow efficiency.

### 4. Adaptive Learning Platform

**Description**: An e-learning platform that adapts to the learning pace and style of each student.

**Functionality**:
- Create personalized learning paths based on student performance.
- Use GPT models to generate educational content and assessments.
- Provide real-time feedback and suggestions for improvement.
- Track progress and adjust learning materials dynamically.

### 5. Smart Customer Support System

**Description**: An AI-powered customer support system that handles inquiries and resolves issues automatically.

**Functionality**:
- Use NLP to understand and respond to customer queries.
- Integrate with CRM to pull customer data and provide personalized responses.
- Automate common support tasks such as password resets and order tracking.
- Escalate complex issues to human agents with context and suggested solutions.

### 6. Automated Marketing Campaigns

**Description**: A system that automates the creation, execution, and optimization of marketing campaigns.

**Functionality**:
- Generate marketing copy and visuals using AI.
- Schedule and send emails, social media posts, and advertisements.
- Track campaign performance and adjust strategies in real-time.
- Use loops to define multi-step campaigns with conditional logic.

### 7. Predictive Maintenance System

**Description**: A system for predicting and preventing equipment failures in industrial settings.

**Functionality**:
- Collect data from sensors and IoT devices.
- Use machine learning models to predict potential failures.
- Automate maintenance scheduling and resource allocation.
- Provide detailed reports and insights on equipment health.

### 8. Real-time Collaboration Platform

**Description**: A platform that facilitates real-time collaboration and project management.

**Functionality**:
- Enable real-time document editing and communication.
- Integrate with project management tools to update tasks and milestones.
- Use AI to suggest improvements and identify bottlenecks.
- Automate notifications and status updates.

## Example YAML Loop Definition for Automated Content Creation

```yaml
loop:
  name: content_creation
  steps:
    - name: generate_idea
      action: gpt_model
      input:
        prompt: "Generate content ideas based on the latest SEO trends."
      output: ideas.yaml
    - name: create_draft
      action: gpt_model
      input:
        prompt: "Create a content draft based on the following idea: {ideas.yaml}"
      output: draft.md
    - name: optimize_seo
      action: seo_tool
      input:
        file: draft.md
      output: optimized_draft.md
    - name: schedule_post
      action: cms_publish
      input:
        file: optimized_draft.md
        schedule_time: "2024-06-07T09:00:00Z"
    - name: monitor_performance
      action: analytics_tool
      input:
        url: "http://example.com/{post_id}"
      output: performance_report.yaml
    - name: adjust_strategy
      action: gpt_model
      input:
        prompt: "Analyze the performance report and suggest strategy adjustments: {performance_report.yaml}"
      output: strategy.yaml

## command to test
make bash
cd core
python -m unittest discover tests.unit