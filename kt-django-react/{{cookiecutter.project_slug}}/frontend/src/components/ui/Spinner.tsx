export function Spinner() {
  return (
    <output aria-label="Loading" className="flex items-center justify-center">
      <span
        role="status"
        className="h-6 w-6 animate-spin rounded-full border-2 border-gray-200 border-t-blue-600"
      >
        <span className="sr-only">Loading...</span>
      </span>
    </output>
  );
}