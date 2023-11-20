import "bootstrap/dist/css/bootstrap.min.css";
import { Container } from "react-bootstrap";
import { Routes, Route, Navigate } from "react-router-dom";
import { HomePage } from "./HomePage";
import UserProfile from "./UserProfile";
import LoginPage from "./LoginPage";
import { LikesDislikesProvider } from "./LikesDislikesContext";
import "./PageTransition.css"; // Import the CSS file

function App() {
  return (
    <Container className="my-6">
      <LikesDislikesProvider>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/user" element={<UserProfile />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </LikesDislikesProvider>
    </Container>
  );
}

export default App;