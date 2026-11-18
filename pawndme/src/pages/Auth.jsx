import { useState } from "react";
import { ActionForm, Field } from "../components/PageControls";
import { api } from "../services/api";

const titles = {
  "/login": "Log In",
  "/register": "Sign Up",
  "/forgot-password": "Forgot Password",
  "/reset-password": "Reset Password",
  "/password-updated": "Password updated successfully",
};

export function isAuthPage(path) {
  return Object.hasOwn(titles, path);
}

export default function Auth({ path, query, onLogin }) {
  const [staff, setStaff] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState("");
  const params = new URLSearchParams(query);
  const register = path === "/register";
  const forgot = path === "/forgot-password";
  const reset = path === "/reset-password";
  const login = path === "/login";
  const loginLink = "#/login" + (params.has("next") ? `?${new URLSearchParams({ next: params.get("next") })}` : "");

  async function submit(data) {
    const body = Object.fromEntries(data);
    if ((register || reset) && body.password !== body.confirm_password) {
      throw new Error("Passwords do not match.");
    }
    delete body.confirm_password;
    if (reset) {
      body.uid = params.get("uid");
      body.token = params.get("token");
    }
    const response = await api(`/auth${path}/`, { method: "POST", body });
    if (forgot) setMessage(response.detail);
    else if (reset) location.hash = "/password-updated";
    else {
      onLogin(response);
      const next = params.get("next");
      location.hash = next?.startsWith("/") && !next.startsWith("//") ? next : "/";
    }
  }

  return (
    <section className="auth-page">
      <h1>{titles[path]}</h1>
      {path === "/password-updated" ? <a className="primary-btn" href={loginLink}>Back to Log In</a> :
        reset && (!params.get("uid") || !params.get("token")) ? (
          <p>This reset link is incomplete. <a href="#/forgot-password">Request a new link.</a></p>
        ) : message ? <p role="status">{message}</p> : (
          <ActionForm onAction={submit}>
            {register && <Field label="Full Name" name="full_name" autoComplete="name" required maxLength={150} />}
            {!reset && <Field label="Email" name="email" type="email" autoComplete="email" required />}
            {!forgot && <>
              <Field label="Password" name="password" type={showPassword ? "text" : "password"}
                minLength={login ? undefined : 8} autoComplete={login ? "current-password" : "new-password"} required />
              {(register || reset) && <Field label="Confirm Password" name="confirm_password"
                type={showPassword ? "text" : "password"} autoComplete="new-password" required />}
              <label className="show-password"><input type="checkbox" checked={showPassword}
                onChange={(event) => setShowPassword(event.target.checked)} /> Show password</label>
            </>}
            {register && <>
              <Field label="Account type" name="account_type" options={[["adopter", "Adopter"], ["shelter_staff", "Shelter staff"]]}
                onChange={(event) => setStaff(event.target.value === "shelter_staff")} />
              {staff && <>
                <Field label="Shelter name" name="shelter_name" required maxLength={100} />
                <Field label="Shelter city" name="shelter_city" required maxLength={100} />
              </>}
            </>}
            {login && <a className="auth-inline-link" href="#/forgot-password">Forgot Password?</a>}
            <button className="primary-btn">{forgot ? "Send Reset Link" : titles[path]}</button>
          </ActionForm>
        )}
      {login ? <p>Don’t have an account? <a href={`#/register${query ? `?${query}` : ""}`}>Sign up</a></p> :
        path !== "/password-updated" && <p><a href={loginLink}>← Back to Log In</a></p>}
    </section>
  );
}
