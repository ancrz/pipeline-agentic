<!-- Memory seed moved out of claude/Pragma.md (project-specific learnings). Copy into ~/.claude/agent-memory/Pragma/ if still relevant. -->

# Pragma Execution Memory

## Playwright E2E Patterns
- **Dual mobile/desktop elements**: When responsive designs render the same component in both mobile and desktop containers (e.g., UserMenu in `md:hidden` and `hidden md:flex`), Playwright strict mode will fail on `locator('[data-testid="..."]')`. Fix: use `.nth(1)` for desktop on default 1280px viewport, or `.nth(0)` for mobile.
- **Hidden file inputs**: `<input type="file" class="hidden">` elements fail `toBeVisible()`. Use `toBeAttached()` instead.
- **getByText strict mode**: Prefer `getByRole('heading', { name: '...' })` over `getByText('...')` to avoid matching paragraphs/subtitles containing the same text.
- **E2E project location**: `/scripts/e2e/` with its own `package.json` and `playwright.config.ts`. Run with `cd scripts/e2e && npx playwright test`.

## Key Patterns
- **SQL INSERT verification**: Always count columns vs ? placeholders after modifying INSERT statements. Use regex-based Python script to automate.
- **Alembic migrations**: Use proper `sa.Column()` with `import sqlalchemy as sa`, never `__import__`. `down_revision` must reference the actual latest migration head, not what a plan says -- always verify with `ls alembic/versions/`.
- **SQLite JSON fields**: When adding new JSON-stored columns to SQLModel, add `json.loads()` deserialization in all service methods that read rows directly (but NOT in methods that delegate to other methods which already handle it).
- **TypeScript type flow**: When schemas use `z.infer<typeof Schema>`, adding fields to the Zod schema automatically propagates to TypeScript types. No need to edit types.ts separately.
- **Frontend API pattern**: `config.apiUrl` is `/api` -- endpoints like `/public/track` resolve to `/api/public/track`. Never add `/api` prefix in endpoint strings.
- **DB_TYPE import**: Import from `..database.manager` not top-level. Pattern: `from ..database.manager import DB_TYPE`
- **Alembic head verification**: Always run `alembic history | head -5` in venv, not parse files manually. The plan's `down_revision` can be stale -- always verify.
- **Alembic revision ID collisions**: This project uses short hex-like IDs (e.g., `d4e5f6a7b8c9`). ALWAYS check `ls alembic/versions/` for filename collisions before creating a new migration. Use `uuid.uuid4().hex[:12]` for guaranteed unique IDs.
- **React unused imports**: Do NOT include `import React from "react"` in new TSX files -- React 18+ JSX transform doesn't require it. Including it causes TS6133.
- **Venv activation**: Backend Python must use `.venv/bin/activate` for imports and alembic commands. System Python lacks FastAPI/SQLModel.
- **batch_alter_table**: Required for ALL SQLite ALTER TABLE in Alembic migrations. SQLite doesn't support native ALTER COLUMN.
- **TouchButton variants**: Only supports `'primary' | 'secondary' | 'ghost' | 'outline'`. No `'danger'` variant. For destructive buttons use `variant="ghost" className="text-red-600"`.
- **DB namespace for banks**: BankService uses `"finance"` namespace, NOT `"payment_methods"`. Always verify namespace by checking existing methods in the service file before writing new ones.
- **defusedxml limitations**: `defusedxml.ElementTree` does NOT export `Element`, `SubElement`, `tostring` -- only patches parsing functions (`parse`, `fromstring`, `iterparse`). XML construction is safe. Use `defusedxml.defuse_stdlib()` for global monkey-patching instead of swapping imports.
- **Alembic autogenerate drift**: When SQLite DB has schema drift (VARCHAR vs DateTime, TEXT vs AutoString), `--autogenerate` picks up hundreds of spurious changes. Always hand-trim migrations to only include intended changes.
- **ruff not installed in venv**: This project's venv doesn't include ruff by default. Install with `pip install ruff` before linting.
- **asyncpg date/str type strictness**: asyncpg binary protocol requires exact Python type matching -- `datetime.date` for DATE columns, `str` for VARCHAR columns. `_adapt_params` no longer auto-converts 10-char YYYY-MM-DD strings to date objects (broke VARCHAR columns). Callers targeting actual DATE columns/DATE() expressions must pass `date.fromisoformat(date_str)` explicitly. Only `daily_closures.date` is a real DATE column in this schema.
- **Docker bind mount sync**: After editing files on host, container may serve stale copies. Run `docker compose restart <service>` to force bind mount refresh. Verify with `sha256sum` on both sides.
- **pytest in Docker**: `pytest` and `pytest-asyncio` are NOT in the backend Docker image by default. Must `pip install pytest pytest-asyncio` after every container restart/recreate. The `tests/` directory is now bind-mounted via `docker-compose.override.yml`.
- **Hardcoded SQL boolean literals**: `VALUES (..., 1, ...)` in INSERT statements won't be caught by `_BOOL_LITERAL_RE` regex (only catches `column = 0/1` patterns). Use `TRUE`/`FALSE` SQL keywords directly in VALUES clauses for boolean columns.
