import { APP_VERSION } from "../../constants";

export function Footer() {
  return <footer className="footer-bar">v{APP_VERSION}</footer>;
}