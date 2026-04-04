# Example requests — `react-din`

Use when the work is the **public library**, **patch schema export**, or **docs/coverage** governance.

1. **Patch schema change**

   ```text
   Add an optional `metadata.labels` array to PatchDocument in the public schema; list react-din exports, schema JSON, and tests that must stay aligned with din-core.
   ```

2. **New public component**

   ```text
   Plan adding a mapped public component `PatchGraphMiniMap` with docs under docs/components, coverage manifest row, and a unit test stub.
   ```

3. **Breaking API**

   ```text
   We need to rename a prop on an exported container; assess semver impact, JSDoc, and validate:changes obligations.
   ```

4. **DIN Studio boundary**

   ```text
   This change only affects the interactive editor chrome, not the published package—confirm ownership is din-studio, not react-din.
   ```

5. **CI parity**

   ```text
   Produce the exact npm commands a contributor must run before merging a change that touches docs/components and project/COVERAGE_MANIFEST.json.
   ```
