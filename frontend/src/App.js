import React, { useEffect, useState } from "react";

// this is the react frontend

function App() {
  const [twitterHandle, setTwitterHandle] = useState(""); // State for the entered Twitter handle
  const [followerCount, setFollowerCount] = useState(null); // State for follower count
  const [data, setData] = useState([]); // State for followers data
  const [loading, setLoading] = useState(false); // State for loading
  const [error, setError] = useState(""); // State for errors
  const [isSubmitted, setIsSubmitted] = useState(false); // State to track form submission
  const [showPopup, setShowPopup] = useState(false); // State for controlling popup visibility
  const [email, setEmail] = useState(""); // State for the user's email
  const [showEmailPopup, setShowEmailPopup] = useState(false); // State for controlling email popup visibility
  const [paymentSucceeded, setPaymentSucceeded] = useState(false); // State for payment success message

  // Fetch follower count and follower list
  const fetchData = () => {
    if (!twitterHandle) {
      setError("Twitter handle cannot be empty.");
      return;
    }

    setLoading(true);
    setError("");
    setFollowerCount(null);
    setData([]); // Clear previous data

    // Fetch the follower count
    fetch(`http://127.0.0.1:5000/api/fetch_followers?handle=${twitterHandle}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
        return response.json();
      })
      .then((followerData) => {
        if (followerData.error) {
          throw new Error(followerData.error);
        }
        setFollowerCount(followerData.sub_count);

        // Fetch a preview version of the followers list
        return fetch("http://127.0.0.1:5000/api/followers");
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
        return response.json();
      })
      .then((followersList) => {
        setData(followersList);
        setLoading(false);
        setIsSubmitted(true); // Mark form as submitted
        // Do not reset isSubmitted here to keep the input disabled
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault(); // Prevent page reload
    fetchData(); // Fetch data when the user submits
  };

  const formatFollowers = (count) => {
    if (count >= 1e6) {
      return (count / 1e6).toFixed(1) + "M Followers";
    } else if (count >= 1e3) {
      return (count / 1e3).toFixed(1) + "K Followers";
    }
    return count + " Followers";
  };

  const makeLinksClickable = (text) => {
    // Convert URLs into clickable links
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const twitterHandleRegex = /@(\w+)/g;

    const linkedText = text
      ?.replace(
        urlRegex,
        (url) =>
          `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`
      )
      ?.replace(
        twitterHandleRegex,
        (handle) =>
          `<a href="https://twitter.com/${handle.slice(
            1
          )}" target="_blank" rel="noopener noreferrer">${handle}</a>`
      );

    return { __html: linkedText };
  };

  const handlePopupClose = () => {
    setShowPopup(false); // Function to close the main popup
  };

  const handlePayNowClick = () => {
    setShowEmailPopup(true); // Show email popup when "Go To Payment" is clicked
  };

  const handleEmailSubmit = (e) => {
    e.preventDefault(); // Prevent default form submission
    console.log("Email submitted:", email);
    setShowEmailPopup(false); // Close email popup after submission
    setEmail(""); // Reset email input
    setPaymentSucceeded(true); // Set payment succeeded state to true
  };

  const calculatePrice = (count) => {
    if (count <= 10000) {
      return 4.99; // Price for 10,000 followers or less
    } else if (count <= 100000) {
      return 48.3; // Price for 100,000 followers or less
    } else if (count <= 1000000) {
      return 497.23; // Price for 1,000,000 followers or less
    } else {
      return "please contact us, there are probably better solutions than this app ...";
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Find Your X Followers with Large Followings</h1>
      <form style={{ marginTop: "20px" }}>
        <input
          type="text"
          value={twitterHandle}
          onChange={(e) => setTwitterHandle(e.target.value)}
          placeholder="Enter X Handle"
          disabled={isSubmitted} // Keep input disabled after submission
          style={{
            padding: "10px",
            width: "300px",
            fontSize: "16px",
            border: "1px solid #ddd",
            borderRadius: "5px",
          }}
        />
        <button
          type="button" // Always set as "button" to avoid default form submission behavior
          disabled={loading} // Disable button while loading
          onClick={() => {
            if (isSubmitted) {
              // Reset logic when the form is already submitted
              setTwitterHandle("");
              setFollowerCount(null);
              setData([]);
              setIsSubmitted(false); // Allow new submissions
              setShowPopup(false);
            } else {
              // Only trigger submission logic if not in reset mode
              fetchData(); // Fetch the data directly
            }
          }}
          style={{
            padding: "10px 20px",
            marginLeft: "10px",
            fontSize: "16px",
            backgroundColor: isSubmitted ? "#007bff" : "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            cursor: loading ? "not-allowed" : "pointer", // Change cursor based on loading
          }}
        >
          {isSubmitted ? "Reset" : "Search"}
        </button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {followerCount !== null && (
        <div>
          <p>
            The Twitter handle <strong>@{twitterHandle}</strong> has{" "}
            <strong>{followerCount.toLocaleString()}</strong> followers.
          </p>
          {data.length > 0 && (
            <div>
              <h2>Here Are Your Last 25 Followers</h2>
              <h3>Highest Number of Followers First</h3>
              <button
                type="button"
                onClick={() => setShowPopup(true)} // Show popup on button click
                style={{
                  padding: "10px 20px",
                  marginLeft: "10px",
                  fontSize: "16px",
                  backgroundColor: "#007bff",
                  color: "#fff",
                  border: "none",
                  borderRadius: "5px",
                  cursor: "pointer",
                }}
              >
                Fetch Your Full List of Followers
              </button>
              <table
                style={{
                  width: "100%",
                  borderCollapse: "collapse",
                  marginTop: "20px",
                }}
              >
                <thead>
                  <tr>
                    <th style={styles.header}>Profile Image</th>
                    <th style={styles.header}>Name</th>
                    <th style={styles.header}>Followers</th>
                    <th style={styles.header}>Description</th>
                    <th style={styles.header}>Location</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((follower, index) => (
                    <tr key={index} style={styles.row}>
                      <td style={styles.cell}>
                        <img
                          src={follower.profile_image_url_https}
                          alt={follower.name}
                          style={{
                            width: "50px",
                            height: "50px",
                            borderRadius: "50%",
                          }}
                        />
                      </td>
                      <td style={styles.cell}>
                        <a
                          href={`https://twitter.com/${follower.screen_name}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{ textDecoration: "none", color: "blue" }}
                        >
                          {follower.name}
                        </a>
                      </td>
                      <td style={styles.cell}>
                        {formatFollowers(follower.followers_count)}
                      </td>
                      <td style={styles.cell}>
                        {follower.description || "N/A"}
                      </td>
                      <td style={styles.cell}>{follower.location || "N/A"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Popup Component */}
      {showPopup && (
        <div
          style={{
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            backgroundColor: "white",
            padding: "20px",
            boxShadow: "0 0 10px rgba(0,0,0,0.5)",
            zIndex: 1000,
          }}
        >
          <h2>See All Your {followerCount.toLocaleString()} Followers</h2>
          <p>
            The price is variable depending on the amount of followers. The more
            followers, the more expensive for us it is to fetch them (the price
            of popularity ...)
          </p>
          <p>
            The Price Is <strong>${calculatePrice(followerCount)}</strong>
          </p>
          <button
            onClick={() => {
              handlePopupClose();
              handlePayNowClick();
            }}
          >
            Go to payment
          </button>
        </div>
      )}
      {/* Overlay */}
      {showPopup && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            zIndex: 999,
          }}
        />
      )}

      {/* Email Popup Component */}
      {showEmailPopup && (
        <div
          style={{
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            backgroundColor: "white",
            padding: "20px",
            boxShadow: "0 0 10px rgba(0,0,0,0.5)",
            zIndex: 1000,
          }}
        >
          <h2>Payment Details</h2>
          <p>
            The Price Is <strong>${calculatePrice(followerCount)}</strong>
          </p>
          <form onSubmit={handleEmailSubmit}>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
              style={{
                padding: "10px",
                width: "300px",
                fontSize: "16px",
                border: "1px solid #ddd",
                borderRadius: "5px",
              }}
            />
            <button
              type="submit"
              style={{
                padding: "10px 20px",
                marginLeft: "10px",
                fontSize: "16px",
                backgroundColor: "#007bff",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Pay Now
            </button>
          </form>
          <button onClick={() => setShowEmailPopup(false)}>Cancel</button>
        </div>
      )}

      {/* Popup for payment success */}
      {paymentSucceeded && (
        <div
          style={{
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            backgroundColor: "white",
            padding: "20px",
            boxShadow: "0 0 10px rgba(0,0,0,0.5)",
            zIndex: 1000,
          }}
        >
          <h2>Payment Succeeded</h2>
          <p>Fetching all followers (this might take a while)...</p>
        </div>
      )}
    </div>
  );
}

const styles = {
  header: {
    background: "#f4f4f4",
    padding: "10px",
    textAlign: "left",
    borderBottom: "1px solid #ddd",
  },
  row: {
    borderBottom: "1px solid #ddd",
  },
  cell: {
    padding: "10px",
    textAlign: "left",
  },
};

export default App;
