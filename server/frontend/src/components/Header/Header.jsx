import React from 'react';
import "../assets/style.css";
import "../assets/bootstrap.min.css";

const Header = () => {
  const logout = async (e) => {
    e.preventDefault();
    let logout_url = window.location.origin + "/djangoapp/logout";
    try {
      const res = await fetch(logout_url, {
        method: "GET",
      });
      const json = await res.json();
      let username = sessionStorage.getItem('username');
      sessionStorage.removeItem('username');
      sessionStorage.removeItem('firstname');
      sessionStorage.removeItem('lastname');
      alert("Logging out " + (username || "") + "...");
      window.location.href = window.location.origin;
    } catch (err) {
      sessionStorage.clear();
      window.location.href = window.location.origin;
    }
  };

  let curr_user = sessionStorage.getItem('username');
  let home_page_items;

  if (curr_user !== null && curr_user !== "") {
    home_page_items = (
      <div className="input_panel" style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <span className='username fw-bold' style={{ color: "#0b5368", fontSize: "1rem" }}>{curr_user}</span>
        <a className="btn btn-outline-danger btn-sm" href="/djangoapp/logout" onClick={logout}>Logout</a>
      </div>
    );
  } else {
    home_page_items = (
      <div className="input_panel" style={{ display: "flex", alignItems: "center", gap: "10px" }}>
        <a className="btn btn-outline-primary btn-sm" href="/login">Login</a>
        <a className="btn btn-primary btn-sm" href="/register">Register</a>
      </div>
    );
  }

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light" style={{ backgroundColor: "darkturquoise", minHeight: "1in" }}>
        <div className="container-fluid">
          <a className="navbar-brand fw-bold fs-3" href="/" style={{ paddingRight: "3%" }}>Dealerships</a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarText">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <a className="nav-link" style={{ fontSize: "larger" }} href="/">Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" style={{ fontSize: "larger" }} href="/dealers">Dealerships</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" style={{ fontSize: "larger" }} href="/about">About Us</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" style={{ fontSize: "larger" }} href="/contact">Contact Us</a>
              </li>
            </ul>
            <span className="navbar-text">
              <div className="loginlink" id="loginlogout">
                {home_page_items}
              </div>
            </span>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Header;
