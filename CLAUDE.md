# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running Code

```bash
python ejercicios_for_anidados.py
python documentacion/ejercicios/fase-N/archivo.py
```

## Project Overview

Curso "Python para Finanzas Cuantitativas" — **43 unidades (U00–U42) en 11 fases**. Desde setup profesional hasta DCF, LBO, modelos de opciones, machine learning y trading algorítmico. Meta: preparar para roles junior en JP Morgan IBD, Private Equity, Citadel y Jane Street. Idioma: español.

## Structure

- `ejercicios_for_anidados.py` — ejercicios sueltos de bucles anidados (legado, no tocar)
- `PLAN-MAESTRO-CURSO.md` — especificación completa del rediseño (guía para desarrollo)
- `documentacion/` — curso estructurado:
  - `README.md` — índice maestro y mapa del curso (43 unidades)
  - `PROGRESO.md` — checklist de 43 unidades en 11 fases
  - `GLOSARIO.md` — 200+ términos Python + Finanzas + OOP + Cuantitativo
  - `BIBLIOGRAFIA.md` — recursos, repos, libros y papers
  - `arbol-aprendizaje.html` — visualización jerárquica interactiva
  - `datos/precios_ejemplo.csv` — 252 filas OHLCV para ejercicios
  - `teoria/fase-N/` — notas teóricas por fase (0–10)
  - `ejercicios/fase-N/` — ejercicios y soluciones por fase
  - `proyectos/` — proyectos finales U41 (plataforma) y U42 (trading system)

## Learning Goal

Training to become a Python expert for quantitative finance at professional level. Target roles: IB analyst (DCF/LBO), Private Equity associate, Quant researcher. Progreso se marca en `PROGRESO.md`. 43 unidades desde fundamentos hasta ML y trading algorítmico.

## Efficiency Principle

Always reason and choose the option that **reaches the goal with the minimum resource cost** (tokens, tool calls, re-reads). Prefer:
1. Memory over re-reading a file or PDF already studied.
2. Grep/Glob over open-ended exploration when the target is known.
3. One precise tool call over several exploratory ones.

Never re-read a resource that is already summarized in the Knowledge Wiki.

## Knowledge Wiki System

All learned knowledge is stored in the auto-memory system at:
```
~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/
```
`MEMORY.md` is the index — always check it first before re-reading any document or PDF.

**Protocol:**
- **Before reading anything:** check `MEMORY.md`. If the topic is covered, use the memory.
- **After learning something new** (PDF, concept, decision, correction): save it immediately to a typed memory file and add a one-line entry to `MEMORY.md`.
- **Memory types:** `user` (who the user is), `feedback` (workflow corrections), `project` (goals/decisions), `reference` (where to find things).
- **Stale check:** if a memory names a file or function, verify it still exists before acting on it.

---

# Behavioral Guidelines (Andrej Karpathy Skills)

Behavioral guidelines to reduce common LLM coding mistakes.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Plan First, Then Execute, Then Verify

For non-trivial tasks, follow this cycle:

**Plan** → iterate with the user until the approach is clear. Don't write code until the plan is agreed.
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

**Execute** → implement the agreed plan. Minimum code, no extras.

**Verify** → always run the code (`python file.py`) or tests to prove it works. Verification improves output quality 2–3x. Never mark a task as done without executing it first.

---

## Meta-rule: Keep This File Lean

This CLAUDE.md must stay under ~2.5k tokens. Every line must earn its place. When adding a new rule, remove or compress something else. Monthly audit: delete anything stale.
