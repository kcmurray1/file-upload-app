


const getChannels = async () => {
    console.log("getting files..")
    try {
        const response = await fetch('/api/files')
        if (response.ok) {
            const data = await response.json()
            console.log(data)
            let content = '';
            data.forEach(channel => {
                content += `<tr><td>${channel.name}</td><td>${channel.size}</td><td>${channel.time_uploaded}</td></tr>`
            });

            document.getElementById("file-table").innerHTML = content;
        
        }
        else
        {
            console.log('failed to fetch files..')
        }
    }
    catch (error) {
        console.log('failed to fetch channels' + error)
    }
}


document.addEventListener("DOMContentLoaded", () => {
  console.log("index loaded");
  const form = document.getElementById("uploadForm");
  const fileInput = document.getElementById("fileInput");
  const statusDiv = document.getElementById("uploadStatus");

  form.addEventListener("submit", async (e) => {
    console.log("uploading...");
    e.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
      statusDiv.textContent = "Please select a file first.";
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/files", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();

        statusDiv.innerHTML = `
            Uploaded <b>${data.name}</b><br>
            Uploaded at: ${new Date(data.time_uploaded).toLocaleString()}`;
      } else {
        const err = await response.json();
        statusDiv.textContent = `Error: ${err.detail || "Upload failed"}`;
      }
    } catch (error) {
      console.error("Upload error:", error);
      statusDiv.textContent = "Network error";
    }
  });
});

document.addEventListener('DOMContentLoaded', getChannels);

