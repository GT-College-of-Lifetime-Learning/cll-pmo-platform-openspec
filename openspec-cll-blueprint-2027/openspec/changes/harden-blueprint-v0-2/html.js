// HTML escaping tagged template function
// D3: Escape by default; allow raw only via raw() for trusted fragments
// All data-derived text inserted into the DOM SHALL be HTML-escaped

// Simple HTML escape map using String.fromCharCode to avoid quote issues
const htmlEscape = {
  "&": String.fromCharCode(38, 97, 109, 112, 59),  // &
  "<": String.fromCharCode(38, 108, 116, 59),      // <
  ">": String.fromCharCode(38, 103, 116, 59),      // >
  '"': String.fromCharCode(38, 113, 117, 111, 116, 59),  // "
  "'": String.fromCharCode(38, 97, 112, 111, 115, 59),  // &apos;
  "/": String.fromCharCode(38, 47, 59),             // &#x2F;
};

// Escape HTML special characters in a string
function escapeHtml(unsafe) {
  if (typeof unsafe !== "string") {
    return unsafe;
  }
  return unsafe.replace(/[&<>"'/]/g, (c) => htmlEscape[c] || c);
}

// Tagged template function that escapes interpolations by default
// Usage: h`${value}` escapes the value, h.raw`${value}` includes raw HTML
function h(strings, ...values) {
  // Interpolate escaped string parts and escaped values
  const result = strings.reduce((acc, string, i) => {
    // Escape the string part (the literal parts between interpolations)
    acc.push(escapeHtml(string));
    // If there's a value after this string, escape it too
    if (i < values.length) {
      acc.push(escapeHtml(values[i]));
    }
    return acc;
  }, []);
  return result.join("");
}

// Allow marking a string as trusted (raw HTML - not escaped)
// Usage: h.raw`${value}` includes the value as-is HTML
h.raw = function (strings, ...values) {
  // Raw template: strings are included as-is, values are included as-is
  const result = strings.reduce((acc, string, i) => {
    acc.push(string);
    if (i < values.length) {
      acc.push(values[i]);
    }
    return acc;
  }, []);
  return result.join("");
};

// Export for CommonJS
exports.h = h;
exports.escapeHtml = escapeHtml;