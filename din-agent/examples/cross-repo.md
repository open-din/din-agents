# Example requests — cross-repo / routing stress

Use these to exercise **global routing**, **ownership ambiguity**, or **sibling coordination** (din-core ↔ react-din ↔ din-studio).

1. **New node end-to-end**

   ```text
   Plan a new synthesis node from patch JSON shape through react-din types to din-studio editor catalog and AI tools; who owns each layer and in what order should we land PRs?
   ```

2. **Schema + Studio**

   ```text
   We need a new field on patch nodes for `colorHint` used only in the studio UI—does this belong in din-core schema, react-din public schema, or studio-only types?
   ```

3. **Contract dispute**

   ```text
   A contributor put registry changes in react-din; tell me the correct repo and what to move where for patch node ID parity.
   ```

4. **MCP reads patches**

   ```text
   Expose canonical patch summaries over MCP for an external agent; touch din-studio MCP bridge—does din-core or react-din need changes for the same contract?
   ```

5. **Renamed interface**

   ```text
   Rename an existing published patch interface in Rust and propagate to schema export, docs, editor codegen tests, and fixtures—list all three repos and acceptance criteria.
   ```
