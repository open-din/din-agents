# Example requests — `din-core`

Use when the work is primarily **Rust patch authority**, registry parity, or runtime/FFI.

1. **New node in the registry**

   ```text
   Add a new patch node type `gainReductionMeter` with stereo in/out and document it in the node registry; list crates, schema, and parity tests that must change.
   ```

2. **Migration behavior**

   ```text
   Plan a patch migration that renames an interface field on `stepSequencer` while preserving round-trip tests and interface metadata in fixtures.
   ```

3. **FFI surface**

   ```text
   Assess extending din-ffi to expose a new graph introspection call and what breaks react-din or WASM consumers.
   ```

4. **Quality gates only (brief)**

   ```text
   Summarize the exact din-core pre-merge checks for a PR that touches `din-patch` document serialization only.
   ```

5. **Canonical fixture alignment**

   ```text
   Update canonical_patch.json to include a minimal graph with midiCC and osc; what registry and schema edits are required?
   ```
