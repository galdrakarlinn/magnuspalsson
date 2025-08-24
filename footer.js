document.addEventListener("DOMContentLoaded", () => {
    fetch("footer.html")
      .then(response => {
        if (!response.ok) throw new Error("HTTP error " + response.status);
        return response.text();
      })
      .then(data => {
        document.getElementById("footer-placeholder").innerHTML = data;
      })
      .catch(error => console.error("Error loading footer:", error));
  });
  