export function Spinner() {
  return (
    <output aria-label="Loading" className="flex items-center justify-center">
      <span role="status" className="spinner">
        <span className="sr-only">Loading...</span>
      </span>
    </output>
  );
}