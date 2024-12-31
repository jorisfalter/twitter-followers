import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Fetch the data from the backend API
    fetch("http://127.0.0.1:5000/api/followers")
      .then((response) => response.json())
      .then((data) => {
        // Use only the top 5 entries
        setData(data.slice(0, 10));
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

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
      <h1>Top 5 Twitter Followers</h1>
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
                dangerouslySetInnerHTML={makeLinksClickable(
                  follower.description || "N/A"
                )}
              ></td>
              <td style={styles.cell}>{follower.location || "N/A"}</td>
            </tr>
          ))}
        </tbody>
      </table>
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
