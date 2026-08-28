export function formatMoment(value) {
  const moment = new Date(value);
  if (Number.isNaN(moment.getTime())) return String(value ?? "");
  // A named month removes the ambiguity an all-numeric locale ordering carries:
  // "8/9/2026" is two different days depending on who is reading it.
  return moment.toLocaleString(undefined, {
    day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit",
  });
}
