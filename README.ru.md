# startup-team

> **Команда из 16 ролей продукта и разработки в виде субагентов — для Claude Code, Codex CLI и Gemini CLI.**

[English ▶ README.md](README.md)

К каждой роли можно обратиться по английскому slug-у, локализованному имени, короткому алиасу или слэш-команде. Неоднозначные запросы проходят через LLM-роутер, который классифицирует и отправляет ровно одной роли.

Ядро плагина **не зависит от языка**. Все локализованные строки лежат в `i18n/`.

---

## Установка

Команды установки отличаются для разных CLI. Выбери ту, которая подходит.

### Claude Code

Через marketplace:

```
/plugin marketplace add sysanalitics/startup-team
/plugin install startup-team@startup-team
```

Или напрямую из этого git-репозитория:

```
/plugin marketplace add https://github.com/sysanalitics/startup-team
/plugin install startup-team
```

Локальная разработка (склонировать репозиторий и указать на папку):

```
git clone https://github.com/sysanalitics/startup-team
/plugin marketplace add ./startup-team
/plugin install startup-team
```

Проверка:

```
/plugin
```

После установки появятся 18 слэш-команд (`/team`, `/role` и по `/<slug>` для каждой роли), 17 субагентов (16 ролей + `team-router`) и 152 skills, доступных этим субагентам.

### Codex CLI

Открой менеджер плагинов и найди `startup-team`:

```
/plugins
startup-team
```

Затем выбери **Install Plugin**.

Codex автоматически обнаружит те же папки `agents/`, `commands/` и `skills/`, что и Claude Code. Различия в именах инструментов учитываются в bootstrap-файлах (`AGENTS.md` читается в начале сессии, и в нужных skills прописан Codex-маппинг).

### Gemini CLI

Установка как расширения Gemini прямо из этого репозитория:

```
gemini extensions install https://github.com/sysanalitics/startup-team
```

Обновление:

```
gemini extensions update startup-team
```

Gemini подгружает `GEMINI.md` в начале сессии — там активируется каталог ролей и поведение резолвера.

---

## Что внутри

- **16 субагентов ролей** в `agents/<slug>.md` — у каждого свой подобранный набор skills (workflow, named patterns, источники, блоки handoff).
- **1 роутер** `agents/team-router.md` — классифицирует свободные запросы относительно таксономии из 16 ролей.
- **18 слэш-команд** в `commands/` — `/team`, `/role` и прямой `/<slug>` для каждой роли.
- **152 skills** в `skills/<slug>/<skill-name>/SKILL.md` (16 ролей) плюс 10 кросс-ролевых skills в `skills/shared/`.
- **Языконезависимая метаинформация** в `data/roles.json` и **локализованные строки** в `i18n/<lang>/roles.json`.

```
startup-team/
├── .claude-plugin/plugin.json
├── README.md                              # английский (основной)
├── README.ru.md                           # русский перевод (этот файл)
├── CLAUDE.md                              # bootstrap для Claude Code
├── AGENTS.md                              # bootstrap для Codex CLI + правила для контрибьюторов
├── GEMINI.md                              # bootstrap для Gemini CLI
├── LICENSE
├── agents/
│   ├── team-router.md
│   └── <16 субагентов ролей>.md
├── commands/
│   ├── team.md
│   ├── role.md
│   └── <16 прямых слэш-команд>.md
├── data/
│   └── roles.json                         # slugs + family + ownership (английский)
├── i18n/
│   ├── README.md                          # i18n-контракт
│   ├── en/roles.json
│   └── ru/roles.json
└── skills/
    ├── shared/<10 shared skills>/SKILL.md
    └── <16 ролей>/<каждая со своими skills, interaction-map.md, sources.md>
```

## 16 ролей

| slug | family | владение |
|---|---|---|
| system-analyst | analysis | Требования, спецификации, API и интеграционные контракты, контракты данных. |
| business-analyst | analysis | Бизнес-процессы, бизнес-правила, impact-анализ, критерии приёмки. |
| product-analyst | analysis | Продуктовые метрики, эксперименты, воронки, дашборды, проверка гипотез. |
| product-owner | product | Бэклог, приоритизация, состав работ, операционная связка с командой поставки, приёмка. |
| product-manager | product | Стратегия, discovery, дорожная карта, продуктовые результаты, north-star метрика. |
| project-manager | delivery | Сроки, бюджет, ресурсы, зависимости, риски, коммуникации поставки. |
| system-architect | architecture | Архитектура системы, компоненты, интеграции, NFR, архитектурные решения. |
| ui-ux-designer | design | Потоки пользователя, IA, wireframes, прототипы, UI, дизайн-система, передача в разработку. |
| tech-lead | engineering | Инженерное направление, стандарты кода, технический менторинг, кросс-командные технические решения. |
| backend-go-developer | engineering | Go-сервисы, конкурентность, обработка ошибок, слой данных на Go. |
| python-developer | engineering | Python-сервисы, data/ML-смежный backend, асинхронный Python. |
| frontend-developer | engineering | TypeScript/React UI, состояние, доступность, веб-производительность. |
| mobile-developer | engineering | iOS / Android / кросс-платформенные приложения, mobile UX, выпуск в стор. |
| fullstack-developer | engineering | Сквозная поставка фичи через web-стек. |
| ml-engineer | engineering | ML-модели, конвейеры обучения, feature stores, inference-сервисы. |
| qa-engineer | quality | Стратегия тестов, автоматизация, триаж дефектов, quality gates, нагрузочное тестирование. |

Канонический список — в `data/roles.json`. Локализованные имена и алиасы — в `i18n/<lang>/roles.json`.

---

## Как пользоваться

### Прямая слэш-команда (ты знаешь, кто нужен)

```
/system-analyst опиши контракт API для размещения заказа
/qa-engineer составь стратегию тестирования для нового чекаута
/backend-go-developer реализуй идемпотентного продьюсера Kafka
```

### Универсальная `/role` с любым идентификатором (slug, имя, алиас)

```
/role system-analyst design the order placement contract
/role системный аналитик опиши контракт заказа        # ru имя
/role гофер реализуй идемпотентного продьюсера Kafka  # ru алиас
/role PM нужна метрика удержания                      # короткий алиас
```

`/role` загружает `data/roles.json` плюс `i18n/<active-locale>/roles.json`, нормализует токен роли и матчит его с slug / именем / алиасами. На неизвестное имя резолвер печатает список 16 ролей в активной локали и просит выбрать — он **не** падает молча на роутер.

### Свободная формулировка через `/team` (не знаешь, кто нужен)

```
/team мы видим медленный чекаут, нужно понять причину
/team стоит ли инвестировать в мобильное приложение?
/team как измерить, работает ли онбординг?
```

Субагент `team-router` классифицирует запрос относительно каталога и отправляет ровно одной роли по правилам из `agents/team-router.md`. Tie-breakers:

- продуктовая неоднозначность → `product-manager` (роль-менеджер по умолчанию, настраивается через `data/roles.json.manager_role`).
- неоднозначность поставки → `project-manager`.
- техническая неоднозначность без явного стека → `tech-lead`.
- иначе: один уточняющий вопрос.

Роутер сам никогда не выдаёт результат.

---

## Интернационализация

Ядро плагина не зависит от языка:

- `data/roles.json` — источник истины для slug-ов, families и ownership-описаний (английский).
- `i18n/<lang>/roles.json` хранит локализованные имена и алиасы для одного языка.
- В `agents/`, `commands/` и `skills/` в этой сборке **нет локализованных строк** — только английский контент, ссылающийся на i18n через процедуру в `commands/role.md`.

Активная локаль читается из `data/roles.json.default_locale` (сейчас `en`); может быть переопределена окружением или подсказкой в запросе. Если языкового пака нет — резолвер падает на `i18n/en/roles.json`.

См. `i18n/README.md` — контракт i18n и инструкция, как добавить новый язык.

## Как решает резолвер

```
ввод пользователя ──► есть slug?            да → вызвать agents/<slug>.md
                       │ нет
                       ▼
                   совпадение с именем
                   в i18n/<lang>/roles.json? да → вызвать agents/<slug>.md
                       │ нет
                       ▼
                   совпадение с алиасом
                   в i18n/<lang>/roles.json? да → вызвать agents/<slug>.md
                       │ нет
                       ▼
              команда была /role?           да → распечатать список 16 ролей, спросить пользователя
                       │ нет (была /team)
                       ▼
              team-router классифицирует     ── один из исходов:
                                                диспетчеризация на конкретную роль
                                                | product-manager (продуктовая неоднозначность)
                                                | project-manager (неоднозначность поставки)
                                                | tech-lead (техническая неоднозначность)
                                                | уточняющий вопрос
```

## Жёсткие правила

- Slug-и — ASCII kebab-case, никогда не локализуются.
- Роутер никогда не играет роль и не выдаёт результат.
- Запрос решается ровно одной ролью за ход.
- Добавление новой роли: сначала в `data/roles.json`, потом во все `i18n/<lang>/roles.json`, потом создать `agents/<slug>.md` и `skills/<slug>/`.
- Добавление нового языка: создать `i18n/<lang>/roles.json` с зеркалом slug-ов из `data/roles.json`. Больше ничего менять не нужно.
- Локализация — только представление. Роутер и каждый skill классифицируют по английскому ownership-тексту.

## Дисциплина skills

Каждый skill роли следует жёсткой структуре: Purpose, Use When, Do Not Use When, Inputs, Workflow, Outputs, Named Patterns (Good/Bad пары), Boundaries, Sources (Priority 1/2/3), Handoff. У shared skills добавляется секция Role Modes — как именно каждая потребляющая роль использует skill.

Файлы skills — 100–250 строк сфокусированного контента. Code skills несут идиоматические примеры; method skills — workflow с принимаемыми решениями; lead skills — материал по review и стандартам.

## Шпаргалка по структуре

```
agents/<slug>.md                     # системный промт роли + маршрутизация по skills
skills/<slug>/SKILL-NAME/SKILL.md    # один skill этой роли
skills/<slug>/interaction-map.md     # карта связей роли с весами
skills/<slug>/sources.md             # консолидированные источники роли
skills/shared/<name>/SKILL.md        # кросс-ролевой skill (с Role Modes)
data/roles.json                      # список slug, ownership, роль-менеджер, локаль по умолчанию
i18n/<lang>/roles.json               # локализованные имена + алиасы для языка
commands/<slug>.md                   # прямой шорткат /<slug>
commands/role.md                     # универсальный шорткат /role <любой идентификатор>
commands/team.md                     # точка входа роутера /team <свободный запрос>
```

---

## Лицензия

MIT — см. [LICENSE](LICENSE).
