import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  let { id } = useParams();
  let root_url = window.location.origin;
  let dealer_url = `${root_url}/djangoapp/dealer/${id}`;
  let review_url = `${root_url}/djangoapp/add_review`;
  let carmodels_url = `${root_url}/djangoapp/get_cars`;

  const postreview = async () => {
    let firstName = sessionStorage.getItem("firstname");
    let lastName = sessionStorage.getItem("lastname");
    let username = sessionStorage.getItem("username");
    let name = (firstName && lastName) ? `${firstName} ${lastName}` : (username || "Anonymous Customer");

    if (!model || review.trim() === "" || !date || !year) {
      alert("All fields are mandatory. Please fill in all details before submitting.");
      return;
    }

    let model_split = model.split(" ");
    let make_chosen = model_split[0];
    let model_chosen = model_split.slice(1).join(" ");

    let jsoninput = JSON.stringify({
      "name": name,
      "dealership": parseInt(id, 10),
      "review": review,
      "purchase": true,
      "purchase_date": date,
      "car_make": make_chosen,
      "car_model": model_chosen,
      "car_year": parseInt(year, 10),
    });

    try {
      const res = await fetch(review_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: jsoninput,
      });

      const json = await res.json();
      if (json.status === 200) {
        alert("Review posted successfully!");
        window.location.href = `${window.location.origin}/dealer/${id}`;
      } else {
        alert("Failed to submit review: " + (json.message || "Unknown error"));
      }
    } catch (err) {
      console.error("Error submitting review:", err);
      alert("Network error while submitting review.");
    }
  };

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200) {
        let dealerobjs = Array.from(retobj.dealer);
        if (dealerobjs.length > 0) setDealer(dealerobjs[0]);
      }
    } catch (err) {
      console.error("Error getting dealer:", err);
    }
  };

  const get_cars = async () => {
    try {
      const res = await fetch(carmodels_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.CarModels) {
        setCarmodels(Array.from(retobj.CarModels));
      }
    } catch (err) {
      console.error("Error getting car models:", err);
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, [id]);

  return (
    <div>
      <Header />
      <div className="container my-5" style={{ maxWidth: "700px" }}>
        <div className="card shadow p-4">
          <h2 className="fw-bold mb-3" style={{ color: "#0b5368" }}>
            Write a Review for {dealer.full_name || "Dealership"}
          </h2>
          <p className="text-muted">Share your car purchase and servicing experience to help other drivers.</p>

          <div className="mb-3">
            <label className="form-label fw-bold">Your Review</label>
            <textarea
              id='review'
              className="form-control"
              rows='5'
              placeholder="Describe your customer experience, sales process, and vehicle condition..."
              value={review}
              onChange={(e) => setReview(e.target.value)}
              required
            ></textarea>
          </div>

          <div className="row g-3 mb-3">
            <div className="col-md-6">
              <label className="form-label fw-bold">Purchase Date</label>
              <input
                type="date"
                className="form-control"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
              />
            </div>
            <div className="col-md-6">
              <label className="form-label fw-bold">Car Make & Model</label>
              <select
                name="cars"
                id="cars"
                className="form-select"
                defaultValue=""
                onChange={(e) => setModel(e.target.value)}
                required
              >
                <option value="" disabled hidden>Choose Car Make and Model</option>
                {carmodels.map((carmodel, idx) => (
                  <option key={idx} value={carmodel.CarMake + " " + carmodel.CarModel}>
                    {carmodel.CarMake} {carmodel.CarModel}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="mb-4">
            <label className="form-label fw-bold">Car Year</label>
            <input
              type="number"
              className="form-control"
              placeholder="e.g. 2022"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              max={2023}
              min={2015}
              required
            />
          </div>

          <div>
            <button className='btn btn-primary px-4 py-2 fw-bold w-100' onClick={postreview} style={{ backgroundColor: "#0b5368", borderColor: "#0b5368" }}>
              Submit Review
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
