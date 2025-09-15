
const getFiles = async () => {
    console.log("getting files..")
    try {
        const response = await fetch('/api/files')
        if (response.ok) {
            const data = await response.json()
            console.log(data)

            let content = '';
            data.forEach(file => {
                content += `
                  <tr data-filename="${file.name}" class="file-row" style="cursor:pointer;">
                    <td>${file.name}</td>
                    <td>${file.size}</td>
                    <td>${file.time_uploaded}</td>
                  </tr>`;
            });

            document.getElementById("file-table").innerHTML = content;

            // make each row clickable
            document.querySelectorAll(".file-row").forEach(row => {
                row.addEventListener("click", async () => {
                    const filename = row.getAttribute("data-filename");
                    try {
                        const presignRes = await fetch(`/api/files/${filename}/download`);
                        if (!presignRes.ok) throw new Error("Failed to get presigned URL");

                        const { url } = await presignRes.json();
                        window.open(url, "_blank"); // open in new tab
                    } catch (err) {
                        console.error("Error fetching file:", err);
                    }
                });
            });

        } else {
            console.log('failed to fetch files..')
        }
    } catch (error) {
        console.log('failed to fetch files ' + error)
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

document.addEventListener('DOMContentLoaded', getFiles);

