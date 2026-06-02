const AUTH_API = "/api/v1/auth";

function formatValidationDetail(detail) {
  if (!Array.isArray(detail)) return null;
  return detail
    .map((item) => {
      const loc = Array.isArray(item.loc) ? item.loc.filter(Boolean).join(".") : "";
      const msg = item.msg || "";
      return loc ? `${loc}: ${msg}` : msg;
    })
    .filter(Boolean)
    .join("; ");
}

async function readErrorMessage(response) {
  try {
    const data = await response.json();
    if (typeof data.message === "string") return data.message;
    const fromDetail = formatValidationDetail(data.detail);
    if (fromDetail) return fromDetail;
    if (typeof data.detail === "string") return data.detail;
  } catch {
    /* ignore */
  }
  return response.statusText || "Ошибка запроса";
}

function showMessage(el, text, type) {
  if (!el) return;
  el.textContent = text;
  el.classList.remove("error", "success");
  el.classList.add("visible", type);
}

function hideMessage(el) {
  if (!el) return;
  el.classList.remove("visible", "error", "success");
  el.textContent = "";
}

async function registerUser(payload) {
  const res = await fetch(`${AUTH_API}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await readErrorMessage(res));
  return res.json();
}

async function loginUser(login, password) {
  const body = new URLSearchParams();
  body.set("username", login);
  body.set("password", password);
  body.set("grant_type", "password");

  const res = await fetch(`${AUTH_API}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json",
    },
    body: body.toString(),
  });
  if (!res.ok) throw new Error(await readErrorMessage(res));
  return res.json();
}

function storeTokens(data) {
  if (data.access_token) localStorage.setItem("access_token", data.access_token);
  if (data.refresh_token) localStorage.setItem("refresh_token", data.refresh_token);
  if (data.token_type) localStorage.setItem("token_type", data.token_type);
}
