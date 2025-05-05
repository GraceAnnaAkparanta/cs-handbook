async function getSuggestions(resumetext) {
    const response = await fetch('https://<YOUR_CLOUD_FUNCTION_URL>', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ resume: resumetext })
    });
    const data = await response.json();
    return data.suggestions; // Adjust based on backend output
  }
  