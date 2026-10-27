import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);

  let dealer_url = "/djangoapp/get_dealers";

  const filterDealers = async (state) => {
    if (state === "All") {
      get_dealers();
      return;
    }
    const res = await fetch(`/djangoapp/get_dealers/${state}`, {
      method: "GET"
    });
    const retobj = await res.json();
    if (retobj.status === 200) {
      let state_dealers = Array.from(retobj.dealers);
      setDealersList(state_dealers);
    }
  };

  const get_dealers = async () => {
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();
    if (retobj.status === 200) {
      let all_dealers = Array.from(retobj.dealers);
      let states_found = [];
      all_dealers.forEach((dealer) => {
        if (dealer.state) states_found.push(dealer.state);
      });
      setStates(Array.from(new Set(states_found)).sort());
      setDealersList(all_dealers);
    }
  };

  useEffect(() => {
    get_dealers();
  }, []);

  let isLoggedIn = sessionStorage.getItem("username") != null;

  return (
    <div>
      <Header />
      <div style={{ padding: "20px" }}>
        <h2 className="mb-4 text-center fw-bold" style={{ color: "#0b5368" }}>Authorized Car Dealerships</h2>
        <table className='table table-striped table-hover shadow-sm rounded'>
          <thead className="table-dark">
            <tr>
              <th>ID</th>
              <th>Dealer Name</th>
              <th>City</th>
              <th>Address</th>
              <th>Zip</th>
              <th>
                <select
                  name="state"
                  id="state"
                  className="form-select form-select-sm"
                  style={{ width: "auto", display: "inline-block" }}
                  defaultValue=""
                  onChange={(e) => filterDealers(e.target.value)}
                >
                  <option value="" disabled hidden>State Filter</option>
                  <option value="All">All States</option>
                  {states.map((st) => (
                    <option key={st} value={st}>{st}</option>
                  ))}
                </select>
              </th>
              {isLoggedIn ? (
                <th>Review Dealer</th>
              ) : null}
            </tr>
          </thead>
          <tbody>
            {dealersList.map((dealer) => (
              <tr key={dealer.id}>
                <td>{dealer.id}</td>
                <td>
                  <a href={`/dealer/${dealer.id}`} className="fw-bold text-decoration-none" style={{ color: "#006699" }}>
                    {dealer.full_name}
                  </a>
                </td>
                <td>{dealer.city}</td>
                <td>{dealer.address}</td>
                <td>{dealer.zip}</td>
                <td><span className="badge bg-info text-dark">{dealer.state}</span></td>
                {isLoggedIn ? (
                  <td>
                    <a href={`/postreview/${dealer.id}`} title="Write a review">
                      <img src={review_icon} className="review_icon" alt="Post Review" style={{ width: "32px", cursor: "pointer" }} />
                    </a>
                  </td>
                ) : null}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dealers;
