Harbor-format coding-agent task that challenges coding agent to fix a Copy-on-Write (CoW) regression in pandas `Series.replace` / `DataFrame.replace`.

## What the agent must do

The agent is given a pandas source tree at `/app/pandas` and the instruction in [`instruction.md`](instruction.md). It must restore correct CoW behavior for list/dict-style replacement without breaking scalar `replace`, non-inplace paths, or existing CoW semantics.

Minimal reproduction (from the instruction):

```python
import pandas as pd

ser = pd.Series([1, 2, 3])
_ = ser[:]
ser.replace([2, 99], [20, 0], inplace=True)
view = ser[:]
ser.iloc[0] = 999
# expected under CoW: view.tolist() == [1, 20, 3]
```

A second case involves a multi-column DataFrame that upcasts one column; a third can raise `IndexError` on wider frames.

## Task layout

| Path | Purpose |
|------|---------|
| `instruction.md` | Agent prompt (Harbor canary GUID included) |
| `task.toml` | Harbor task metadata (timeouts, environment, etc.) |
| `environment/` | Dockerfile + pre-packaged pandas source (`pandas.tar.gz`) + build requirements |
| `solution/` | Oracle solution (`solve.sh` applies `folder.patch`) |
| `tests/` | Verifier (`test.sh` + `test_outputs.py`) that checks CoW tracking after list-like replace |

The environment ships a pandas tree that exhibits the bug. The oracle patch (derived from the upstream PR) re-registers blocks that `replace_list` actually returns and pops intermediate refs in reverse order so both the CoW leak and the `IndexError` disappear.

## Running the task

Requires the [Harbor](https://github.com/harbor-framework/harbor) CLI:

```bash
uv tool install harbor
# or: pip install harbor
```

From this directory (or after publishing to Harbor Hub):

```bash
harbor run --path . \
  --agent <your-agent> \
  --model <provider/model> \
  --n-concurrent 1
```

The verifier writes a reward to `/logs/verifier/reward.txt` (1 = pass, 0 = fail). The main assertion lives in `tests/test_outputs.py` and checks that a view taken after an inplace list-like `replace` no longer shares memory with the original.

## Notes

- Agent timeout: 18 000 s; verifier timeout: 2 400 s (see `task.toml`).
- The pandas tree is provided as a tarball inside the image; network is available during the environment build.
- The oracle only applies the targeted fix; it does not rewrite unrelated CoW or replace paths.
- This is an evaluation task, not a general-purpose pandas fork. Do not treat the shipped source as an upstream mirror.

## Upstream reference

- PR: https://github.com/pandas-dev/pandas/pull/66712  

