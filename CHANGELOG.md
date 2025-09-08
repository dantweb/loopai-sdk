# loopAI SDK changelog
## [v2.7.0-rc1]
### Added
    - BroadCast Data API v1.0.0
    - wordpress adapter v1.2.0
    - telegram adabter beta-1.0.0
    - user segregation
    - project differentiation fix
    - cron runner
    - Project defined .env which can be overriden by loop's and loop step's .env
    - More session-related variables are moved to the session_manager - t2
    - Added Http adapter to the core
    - FileSystem Adapter and Gpt2Code_Executor
    - Temperature config through the YAML
    - Agents
    - Root executor - executes just on the host, while bash executor does it in docker
### Changed
    - JSON response format
    - update project filtering by loops on cancel
    - RSS extractor fix2
    - Featherless timeout set 600 sec and to requests
    - adapt content length in technews_service to 4000 bytes for deepseek
    - add ```json remover from the llm's response when json is expected (deepseek feature)
    - Optimize base64_logging
    - TextAdapter reads text and stores in BroadcastAdapter
    - Remove tokens limitatiton in Featherless Service and increase timeout 300
    - HTTP adapter returns json from rss, html and json or other content as it is
    - Bash_executor docker sync
    - Better BroadcastAdapter and BroadcastModel
### Fixed
    - file upload
    - max tokens count
    - broadcast adapter fields finding
    - deepseek response to dict() --- push 
    - fix alembic 2
    - fealtehrless_service failed response proccessing
    - change featherless time for waiting attempts
    - loop controller session handling, setting, cleanup broadcast
    - update session manager minor fix
    - step env handling 1
    - file_operation 
    - gpt2code_chunk executor
    - temperature management for o3-mini models
### Removed