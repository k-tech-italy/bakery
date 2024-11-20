import { BrowserRouter, Route, Routes } from "react-router-dom";
import LoginScreen from "./screens/Login";
import Home from "./screens/Home";
import { getToken } from "./service/auth";

function AppRouting() {
  const token = getToken();

  const isAuthenticated = token !== "";

  const HomeRoute = isAuthenticated ? Home : LoginScreen;
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomeRoute />} />
        <Route path="/login" element={<LoginScreen />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRouting;
