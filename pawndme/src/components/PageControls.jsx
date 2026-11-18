import { useEffect, useState } from "react";
import { api } from "../services/api";

export function useApi(path, token, revision = 0) {
  const [state, setState] = useState({});
  useEffect(() => {
    if (!path) return;
    const controller = new AbortController();
    api(path, { token, signal: controller.signal }).then(
      (data) => setState({ path, token, revision, data }),
      (error) => {
        if (!controller.signal.aborted) {
          setState({ path, token, revision, error: error.message });
        }
      },
    );
    return () => controller.abort();
  }, [path, token, revision]);
  if (state.path !== path || state.token !== token || state.revision !== revision) return {};
  return state;
}

export function Load({ state, children }) {
  if (state.error) return <p role="alert" className="form-error">{state.error}</p>;
  if (!state.data) return <p role="status">Loading…</p>;
  return children(state.data);
}

export function ActionForm({ onAction, children, className = "page-form" }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    setBusy(true);
    setError("");
    try {
      await onAction(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className={className} onSubmit={submit}>
      <fieldset disabled={busy}>
        {children}
      </fieldset>
      {busy && <p role="status">Saving…</p>}
      {error && <p role="alert" className="form-error">{error}</p>}
    </form>
  );
}

export function Field({ label, options, multiline, ...props }) {
  return (
    <label className="field">
      {label}
      {options ? (
        <select {...props}>
          {options.map(([value, text]) => <option key={value} value={value}>{text}</option>)}
        </select>
      ) : multiline ? <textarea {...props} /> : <input {...props} />}
    </label>
  );
}

export const types = [["dog", "Dog"], ["cat", "Cat"], ["other", "Other"]];
export const sizes = [["small", "Small"], ["medium", "Medium"], ["large", "Large"]];
export const personalities = [["calm", "Calm"], ["active", "Active"], ["friendly", "Friendly"], ["shy", "Shy"]];
export const statuses = [["available", "Available"], ["reserved", "Reserved"], ["adopted", "Adopted"]];
export const any = (label, options) => [["", label], ...options];
