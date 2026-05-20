import { APP_VERSION } from "../../constants";

export function Footer() {
  return (
    <footer className="border-t py-3 text-center text-xs text-gray-400">
      v{APP_VERSION}
    </footer>
  );
}