import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(null);

  let { id } = useParams();
  let root_url = window.location.origin;
  let dealer_url = `${root_url}/djangoapp/dealer/${id}`;
  let reviews_url = `${root_url}/djangoapp/reviews/dealer/${id}`;
  let post_review_url = `/postreview/${id}`;

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200) {
        let dealerobjs = Array.from(retobj.dealer);
        if (dealerobjs.length > 0) {
          setDealer(dealerobjs[0]);
        }
      }
    } catch (err) {
      console.error("Error fetching dealer:", err);
    }
  };

  const get_reviews = async () => {
    try {
      const res = await fetch(reviews_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200) {
        if (retobj.reviews && retobj.reviews.length > 0) {
          setReviews(retobj.reviews);
          setUnreviewed(false);
        } else {
          setUnreviewed(true);
        }
      } else {
        setUnreviewed(true);
      }
    } catch (err) {
      console.error("Error fetching reviews:", err);
      setUnreviewed(true);
    }
  };

  const senti_icon = (sentiment) => {
    let icon = sentiment === "positive" ? positive_icon : sentiment === "negative" ? negative_icon : neutral_icon;
    return icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={post_review_url} title="Add Review" className="ms-3">
          <img src={review_icon} style={{ width: '48px', verticalAlign: 'middle' }} alt='Post Review' />
        </a>
      );
    }
  }, [id]);

  return (
    <div>
      <Header />
      <div style={{ margin: "25px 40px" }}>
        <div className="p-3 border rounded bg-light mb-4 shadow-sm">
          <h1 className="fw-bold" style={{ color: "#0b5368" }}>
            {dealer.full_name || "Dealership"}
            {postReview}
          </h1>
          <h5 className="text-secondary">
            {dealer.city ? `${dealer.city}, ${dealer.address}, Zip: ${dealer.zip}, ${dealer.state}` : "Loading dealer information..."}
          </h5>
        </div>

        <h3 className="fw-bold mb-3" style={{ color: "#0b5368" }}>Customer Reviews & Sentiment</h3>
        <div className="reviews_panel">
          {reviews.length === 0 && unreviewed === false ? (
            <div className="text-muted p-3">Loading Reviews....</div>
          ) : unreviewed === true || reviews.length === 0 ? (
            <div className="alert alert-info">No reviews yet for this dealership! Be the first to post a review.</div>
          ) : (
            reviews.map((rev, index) => (
              <div key={rev.id || index} className='review_panel card shadow-sm mb-3 p-3'>
                <div className="d-flex align-items-center mb-2">
                  <img src={senti_icon(rev.sentiment)} className="emotion_icon me-3" alt={rev.sentiment || 'Sentiment'} style={{ width: "36px", height: "36px" }} />
                  <div>
                    <span className="badge bg-secondary text-uppercase">{rev.sentiment || 'neutral'}</span>
                    <strong className="ms-2">{rev.name}</strong>
                  </div>
                </div>
                <div className='review fst-italic mb-2' style={{ fontSize: "1.05rem" }}>"{rev.review}"</div>
                <div className="reviewer text-muted small">
                  <strong>Vehicle:</strong> {rev.car_make} {rev.car_model} ({rev.car_year})
                  {rev.purchase ? <span className="ms-2 badge bg-success">Verified Purchase</span> : null}
                  {rev.purchase_date ? <span className="ms-2 text-secondary">Date: {rev.purchase_date}</span> : null}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Dealer;
