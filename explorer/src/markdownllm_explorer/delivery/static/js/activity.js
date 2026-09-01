export function createActivityController({
  timeoutMs,
  sendTouch,
  onExpire,
  now = () => Date.now(),
  setTimer = (callback, delay) => setTimeout(callback, delay),
  clearTimer = timer => clearTimeout(timer),
  touchIntervalMs = 60000,
}) {
  let timer = null;
  let expired = false;
  let lastTouchAt = Number.NEGATIVE_INFINITY;

  function arm() {
    if (timer !== null) clearTimer(timer);
    timer = setTimer(expire, timeoutMs);
  }

  function expire() {
    if (expired) return;
    expired = true;
    timer = null;
    onExpire();
  }

  function recordActivity() {
    if (expired) return;
    const observed = now();
    arm();
    if (observed - lastTouchAt < touchIntervalMs) return;
    lastTouchAt = observed;
    Promise.resolve(sendTouch()).catch(() => {});
  }

  function start() {
    if (!expired) arm();
  }

  function stop() {
    if (timer !== null) clearTimer(timer);
    timer = null;
  }

  return {start, stop, recordActivity, expire, isExpired: () => expired};
}

export function installActivityLease({timeoutSeconds, sendTouch, onExpire, target = document}) {
  const controller = createActivityController({timeoutMs: timeoutSeconds * 1000, sendTouch, onExpire});
  const bindings = [
    ["pointerdown", {capture: true}],
    ["keydown", {capture: true}],
    ["touchstart", {capture: true, passive: true}],
    ["scroll", {capture: true, passive: true}],
  ];
  bindings.forEach(([event, options]) => target.addEventListener(event, controller.recordActivity, options));
  controller.start();
  return () => {
    bindings.forEach(([event, options]) => target.removeEventListener(event, controller.recordActivity, options));
    controller.stop();
  };
}
