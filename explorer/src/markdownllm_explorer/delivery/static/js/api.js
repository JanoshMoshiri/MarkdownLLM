let capability = sessionStorage.getItem("mdllm-explorer-capability") || "";

export function captureCapability() {
  const params = new URLSearchParams(location.hash.slice(1));
  const supplied = params.get("cap");
  if (supplied) {
    capability = supplied;
    sessionStorage.setItem("mdllm-explorer-capability", supplied);
    params.delete("cap");
    const remainder = params.toString();
    history.replaceState(null, "", `${location.pathname}${remainder ? `#${remainder}` : ""}`);
  }
  return Boolean(capability);
}

export async function get(path, params = {}, signal) {
  const url = new URL(path, location.origin);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, value);
  });
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(new DOMException("Explorer request timed out.", "TimeoutError")), 10000);
  const onAbort = () => controller.abort(signal.reason);
  signal?.addEventListener("abort", onAbort, {once: true});
  let response;
  try {
    response = await fetch(url, {headers: {"X-Explorer-Capability": capability}, signal: controller.signal, cache: "no-store"});
  } catch (error) {
    if (controller.signal.reason?.name === "TimeoutError") { const timeoutError = new Error("Explorer did not respond within 10 seconds."); timeoutError.code = "request_timeout"; timeoutError.retryable = true; throw timeoutError; }
    throw error;
  } finally {
    clearTimeout(timeout); signal?.removeEventListener("abort", onAbort);
  }
  const payload = await response.json().catch(() => ({error: {code: "invalid_response", message: "Explorer returned an invalid response.", retryable: false}}));
  if (!response.ok) {
    const error = new Error(payload.error?.message || "Explorer request failed.");
    error.code = payload.error?.code || "request_failed";
    error.retryable = Boolean(payload.error?.retryable);
    throw error;
  }
  const data = payload.data;
  const meta = payload.meta || {};
  // HTTP pagination metadata has one canonical home.  The browser adapts it
  // into its internal page model without requiring duplicate wire fields.
  if (data && Array.isArray(data.items)) {
    return {...data, next_cursor: meta.next_cursor ?? null, partial: Boolean(meta.partial), observed_at: meta.observed_at};
  }
  if (data?.commits && Array.isArray(data.commits.items)) {
    return {...data, commits: {...data.commits, next_cursor: meta.next_cursor ?? null, partial: Boolean(meta.partial), observed_at: meta.observed_at}};
  }
  return data;
}

export async function touch() {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  try {
    const response = await fetch(new URL("/health", location.origin), {
      method: "HEAD",
      headers: {"X-Explorer-Capability": capability},
      signal: controller.signal,
      cache: "no-store",
    });
    return response.ok;
  } catch {
    return false;
  } finally {
    clearTimeout(timeout);
  }
}
