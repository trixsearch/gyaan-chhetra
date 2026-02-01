import Navbar from "../components/Navbar";

export default function MainLayout({ children }) {
  return (
    <>
      <Navbar />
      <main className="container">
        {children}
      </main>
    </>
  );
}
