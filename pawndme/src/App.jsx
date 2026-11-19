import { useEffect, useState } from "react";
import Header from "./components/Header";
import Hero from "./components/Hero";
import FeaturedPets from "./components/FeaturedPets";
import Categories from "./components/Categories";
import HowItWorks from "./components/HowItWorks";
import Footer from "./components/Footer";
import Wave from "./components/Wave";
import Auth, { isAuthPage } from "./pages/Auth";
import { Account, AnimalEditor } from "./pages/Account";
import { Catalog, Favorites, PetProfile } from "./pages/Pets";
import { api } from "./services/api";

import "./App.css";
import "./pages.css";

const tokenKey = "pawndme-token";
const currentRoute = () => location.hash.slice(1) || "/";

export default function App() {
  const [route, setRoute] = useState(currentRoute);
  const [session, setSession] = useState(() => ({ token: localStorage.getItem(tokenKey) }));
  const [sessionError, setSessionError] = useState("");
  const [path, query] = route.split("?");
  const { token, user } = session;
  const account = { token: user ? token : null, user, loginLink: `#/login?${new URLSearchParams({ next: route })}` };

  useEffect(() => {
    const update = () => setRoute(currentRoute());
    window.addEventListener("hashchange", update);
    return () => window.removeEventListener("hashchange", update);
  }, []);

  useEffect(() => {
    if (path === "/about" && query === "section=how-it-works") {
      document.getElementById("how-it-works")?.scrollIntoView();
    } else {
      window.scrollTo({ top: 0, behavior: "instant" });
    }
  }, [path, query]);

  useEffect(() => {
    if (!token || user) return;
    const controller = new AbortController();
    api("/auth/me/", { token, signal: controller.signal }).then(
      (user) => setSession({ token, user }),
      (error) => {
        if (controller.signal.aborted) return;
        if (error.status === 401) clearSession();
        else setSessionError(error.message);
      },
    );
    return () => controller.abort();
  }, [token, user]);

  function clearSession() {
    localStorage.removeItem(tokenKey);
    setSession({});
    setSessionError("");
  }

  async function logout() {
    try {
      await api("/auth/logout/", { token, method: "POST" });
    } catch (error) {
      if (error.status !== 401) throw error;
    }
    clearSession();
    location.hash = "/";
  }

  function login(nextSession) {
    localStorage.setItem(tokenKey, nextSession.token);
    setSession(nextSession);
    setSessionError("");
  }

  const auth = isAuthPage(path);
  const pet = path.match(/^\/pets\/(\d+)$/);
  const edit = path.match(/^\/account\/animals\/(new|\d+)$/);
  let page;
  if (auth) page = <Auth key={route} path={path} query={query} onLogin={login} />;
  else if (token && !user && !sessionError) page = <p className="container section" role="status">Loading account…</p>;
  else if (path === "/") page = <><Hero /><FeaturedPets account={account} /><Wave /><Categories /><Wave /><HowItWorks /></>;
  else if (path === "/about") page = <><Hero /><HowItWorks /></>;
  else if (path === "/pets") page = <Catalog query={query} account={account} />;
  else if (pet) page = <PetProfile key={pet[1]} id={pet[1]} account={account} />;
  else if (path === "/favorites") page = <Favorites account={account} />;
  else if (path === "/account") page = <Account account={account} logout={logout} />;
  else if (edit) page = <AnimalEditor key={edit[1]} id={edit[1] === "new" ? null : edit[1]} account={account} />;
  else page = <section className="container inner-page"><h1>Page not found</h1><a href="#/">Back to Home</a></section>;

  return (
    <>
      <Header key={path} path={path} user={user} simple={auth} />
      <main>{sessionError && !user && !auth && <p className="container form-error" role="alert">{sessionError}</p>}{page}</main>
      {!auth && <Footer />}
    </>
  );
}
