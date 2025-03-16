# loopAI SDK changelog
## [Unreleased]
### Added
    - BroadCast Data API v1.0.0
    - wordpress adapter v1.2.0
    - telegram adabter beta-1.0.0
    - user segregation
    - project differentiation fix
    - cron runner
    - Project defined .env which can be overriden by loop's and loop step's .env
### Changed
    - JSON response format
    - update project filtering by loops on cancel
    - RSS extractor fix2
    - Featherless timeout set 120 sec and to requests
    - adapt content length in technews_service to 4000 bytes for deepseek
    - add ```json remover from the llm's response when json is expected (deepseek feature)
    - Optimize base64_logging
    - TextAdapter reads text and stores in BroadcastAdapter
### Fixed
    - file upload
    - max tokens count
    - broadcast adapter fields finding
    - deepseek response to dict() --- push 
    - fix alembic 2
    - fealtehrless_service failed response proccessing
    - change featherless time for waiting attempts
    - loop controller session handling, setting, cleanup broadcast
### Removed