const formData = new FormData();
formData.append("resume", uploadedPdfFile);  // from file input
formData.append("desired_role", roleInputValue);  // from text input

fetch("http://localhost:8000/improve-resume", {
  method: "POST",
  body: formData
})
.then(res => res.json())
.then(data => {
  document.getElementById("results").innerText = data.improved_bullets;
})
.catch(err => console.error(err));
