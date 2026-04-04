# Example requests — `din-studio`

Use for **editor workflows**, **surface manifests**, **MCP target**, and **AI/agent UI**.

1. **Editor node catalog**

   ```text
   Add editor support for node ID `midiPC` in nodeCatalog.ts; list COVERAGE_MANIFEST, feature doc, unit test, and TEST_MATRIX scenario updates.
   ```

2. **Visible workflow**

   ```text
   Change the asset library panel empty state copy and flow; what SURFACE_MANIFEST and BDD scenario IDs must be updated?
   ```

3. **MCP target**

   ```text
   Add a new MCP tool under targets/mcp that lists open patches; what tests under targets/mcp/tests must be added or updated?
   ```

4. **AI catalog sync**

   ```text
   After adding a node to the editor catalog, list changes needed in ui/ai/systemPrompt.ts and ui/ai/tools.ts per the agent-prompt-catalog skill.
   ```

5. **Full studio gates**

   ```text
   Give the full din-studio pre-merge checklist (lint through e2e) for a PR that changes both ui/editor and project/SURFACE_MANIFEST.json.
   ```
