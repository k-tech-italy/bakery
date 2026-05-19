import "@testing-library/jest-dom";

// Vitest 3.x passes `--localstorage-file` to worker threads on Node.js 25+,
// enabling a built-in localStorage that lacks `.clear()`. Replace it with a
// minimal in-memory Storage implementation so all tests work correctly.
if (typeof globalThis.localStorage?.clear !== "function") {
  const store = new Map<string, string>();
  Object.defineProperty(globalThis, "localStorage", {
    configurable: true,
    enumerable: true,
    value: {
      get length() {
        return store.size;
      },
      clear() {
        store.clear();
      },
      getItem(key: string) {
        return store.get(key) ?? null;
      },
      setItem(key: string, value: string) {
        store.set(String(key), String(value));
      },
      removeItem(key: string) {
        store.delete(key);
      },
      key(index: number) {
        return [...store.keys()][index] ?? null;
      },
    },
  });
}