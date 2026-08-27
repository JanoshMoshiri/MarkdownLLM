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
  return payload.data;
}
