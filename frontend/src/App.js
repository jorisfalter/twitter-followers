import React, { useEffect, useState } from "react";

// this is the react frontend

function App() {
  const [twitterHandle, setTwitterHandle] = useState(""); // State for the entered Twitter handle
  const [followerCount, setFollowerCount] = useState(null); // State for follower count
  const [data, setData] = useState([]); // State for followers data
  const [loading, setLoading] = useState(false); // State for loading
  const [error, setError] = useState(""); // State for errors

  // Fetch data from the backend
  const fetchData = () => {
    if (!twitterHandle) {
      setError("Twitter handle cannot be empty.");
      return;
    }

    setLoading(true);
    setError("");
    setFollowerCount(null);
    console.log("fetching data");
    fetch(`http://127.0.0.1:5000/api/fetch_followers?handle=${twitterHandle}`) // Replace with your backend URL
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
        console.log(response);
        return response.json();
      })
      .then((data) => {
        console.log(data);
        if (data.error) {
          throw new Error(data.error);
        }
        setFollowerCount(data.sub_count);
        setLoading(false);
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

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      {/* Show landing page if no handle is entered */}
      {!data.length && (
        <div>
          <h1>Find Twitter Followers</h1>
          <form onSubmit={handleFormSubmit} style={{ marginTop: "20px" }}>
            <input
              type="text"
              value={twitterHandle}
              onChange={(e) => setTwitterHandle(e.target.value)}
              placeholder="Enter Twitter Handle"
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
              Search
            </button>
          </form>
          {loading && <p>Loading...</p>}
          {error && <p style={{ color: "red" }}>{error}</p>}
          {followerCount !== null && (
            <p>
              The Twitter handle <strong>@{twitterHandle}</strong> has{" "}
              <strong>{followerCount.toLocaleString()}</strong> followers.
            </p>
          )}
        </div>
      )}
      {/* Render followers table if data is available */}
      {data.length > 0 && (
        <div>
          <h1>Followers for @{twitterHandle}</h1>
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
                  <td
                    style={styles.cell}
                    dangerouslySetInnerHTML={{
                      __html: follower.description || "N/A",
                    }}
                  ></td>
                  <td style={styles.cell}>{follower.location || "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
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
